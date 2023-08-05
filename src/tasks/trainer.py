#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn.utils import clip_grad_norm_
from .preprocessing_funcs import load_dataloaders
from .train_funcs import load_state, load_results, evaluate_, evaluate_results
from ..misc import save_as_pickle, load_pickle
import matplotlib.pyplot as plt
import time
import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', \
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger(__file__)

def train_and_fit(args):
    if args.fp16:    
        from apex import amp
    else:
        amp = None
    
    cuda = torch.cuda.is_available()
    train_loader, test_loader, train_len, test_len = load_dataloaders(args)
    logger.info("Loaded %d Training samples." % train_len)
    
    from ..model.BERT.modeling_bert import BertModel as Model
    model = args.model_size
    lower_case = True
    model_name = 'BERT'
    net = Model.from_pretrained(model, force_download=False, \
                                model_size=args.model_size,
                                task='classification',\
                                n_classes_=args.num_classes)
    
    tokenizer = load_pickle("%s_tokenizer.pkl" % model_name)
    net.resize_token_embeddings(len(tokenizer))
    e1_id = tokenizer.convert_tokens_to_ids('[E1]')
    e2_id = tokenizer.convert_tokens_to_ids('[E2]')
    assert e1_id != e2_id != 1
    
    if cuda:
        net.cuda()
        
    logger.info("FREEZING MOST HIDDEN LAYERS...")
    unfrozen_layers = ["classifier", "pooler", "encoder.layer.11", \
                       "classification_layer", "blanks_linear", "lm_linear", "cls"]
        
    for name, param in net.named_parameters():
        if not any([layer in name for layer in unfrozen_layers]):
            print("[FROZE]: %s" % name)
            param.requires_grad = False
        else:
            print("[FREE]: %s" % name)
            param.requires_grad = True
    
    criterion = nn.CrossEntropyLoss(ignore_index=-1)
    optimizer = optim.Adam([{"params":net.parameters(), "lr": args.lr}])
    scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=[2,4,6,8,12,15,18,20,22,\
                                                                      24,26,30], gamma=0.8)
    start_epoch, best_pred, amp_checkpoint = load_state(net, optimizer, scheduler, args, load_best=False)  
    
    if args.fp16 and amp is not None:
        logger.info("Using fp16...")
        net, optimizer = amp.initialize(net, optimizer, opt_level='O2')
        if amp_checkpoint is not None:
            amp.load_state_dict(amp_checkpoint)
        scheduler = optim.lr_scheduler.MultiStepLR(optimizer, milestones=[2,4,6,8,12,15,18,20,22,\
                                                                          24,26,30], gamma=0.8)
    
    losses_per_epoch, accuracy_per_epoch, test_f1_per_epoch = load_results(args.model_no)
    logger.info("Starting training process...")
    pad_id = tokenizer.pad_token_id
    mask_id = tokenizer.mask_token_id
    update_size = len(train_loader)//10
    for epoch in range(start_epoch, args.num_epochs):
        start_time = time.time()
        net.train()
        total_loss = 0.0
        losses_per_batch = []
        total_acc = 0.0
        accuracy_per_batch = []
        for i, data in enumerate(train_loader, 0):
            x, e1_e2_start, labels, _,_,_ = data
            attention_mask = (x != pad_id).float()
            token_type_ids = torch.zeros((x.shape[0], x.shape[1])).long()

            if cuda:
                x = x.cuda()
                labels = labels.cuda()
                attention_mask = attention_mask.cuda()
                token_type_ids = token_type_ids.cuda()
                
            classification_logits = net(x, token_type_ids=token_type_ids, attention_mask=attention_mask, Q=None,\
                          e1_e2_start=e1_e2_start)
            
            loss = criterion(classification_logits, labels.squeeze(1))
            loss = loss/args.gradient_acc_steps
            
            if args.fp16:
                with amp.scale_loss(loss, optimizer) as scaled_loss:
                    scaled_loss.backward()
            else:
                loss.backward()
            
            if args.fp16:
                grad_norm = torch.nn.utils.clip_grad_norm_(amp.master_params(optimizer), args.max_norm)
            else:
                grad_norm = clip_grad_norm_(net.parameters(), args.max_norm)
            
            if (i % args.gradient_acc_steps) == 0:
                optimizer.step()
                optimizer.zero_grad()
            
            total_loss += loss.item()
            total_acc += evaluate_(classification_logits, labels, \
                                   ignore_idx=-1)[0]
            
            if (i % update_size) == (update_size - 1):
                losses_per_batch.append(args.gradient_acc_steps*total_loss/update_size)
                accuracy_per_batch.append(total_acc/update_size)
                print('[Epoch: %d, %5d/ %d points] total loss, accuracy per batch: %.3f,
