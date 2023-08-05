#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import math
import spacy
import pandas as pd
from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader
import torch
from transformers import BertTokenizer
from ..misc import save_as_pickle, load_pickle

def process_text(text, mode='train'):
    sents, relations, comments, blanks = [], [], [], []
    for i in range(int(len(text)/4)):
        sent = text[4*i]
        relation = text[4*i + 1]
        comment = text[4*i + 2]
        blank = text[4*i + 3]
        
        # check entries
        if mode == 'train':
            assert int(re.match("^\d+", sent)[0]) == (i + 1)
        else:
            assert (int(re.match("^\d+", sent)[0]) - 8000) == (i + 1)
        assert re.match("^Comment", comment)
        assert len(blank) == 1
        
        sent = re.findall("\"(.+)\"", sent)[0]
        sent = re.sub('<e1>', '[E1]', sent)
        sent = re.sub('</e1>', '[/E1]', sent)
        sent = re.sub('<e2>', '[E2]', sent)
        sent = re.sub('</e2>', '[/E2]', sent)
        sents.append(sent); relations.append(relation), comments.append(comment); blanks.append(blank)
    return sents, relations, comments, blanks

def preprocess_data(data, label_map, tokenizer, max_len):
    sentences = data['sentence']
    labels = data['label']
    labels = [label_map[label] for label in labels]
    tokens = []
    token_ids = []
    mask_ids = []
    segment_ids = []
    label_ids = []

    for sentence in tqdm(sentences):
        text_tokens = tokenizer.tokenize(sentence)
        text_tokens = ["[CLS]"] + text_tokens + ["[SEP]"]
        tokens.append(text_tokens)
        token_id = tokenizer.convert_tokens_to_ids(text_tokens)
        padding = [0] * (max_len - len(token_id))
        token_id += padding
        mask_id = [1] * len(token_id) + padding
        segment_id = [0] * max_len
        token_ids.append(token_id)
        mask_ids.append(mask_id)
        segment_ids.append(segment_id)

    label_ids = labels
    return torch.tensor(token_ids), torch.tensor(mask_ids), torch.tensor(segment_ids), torch.tensor(label_ids)

def process_data(data_dict):
    sents = []
    labels = []
    for relation, dataset in data_dict.items():
        for data in dataset:
            # first, get & verify the positions of entities
            h_pos, t_pos = data['h'][-1], data['t'][-1]
                
            if not len(h_pos) == len(t_pos) == 1: # remove one-to-many relation mappings
                continue
                
            h_pos, t_pos = h_pos[0], t_pos[0]
                
            if len(h_pos) > 1:
                running_list = [i for i in range(min(h_pos), max(h_pos) + 1)]
                assert h_pos == running_list
                h_pos = [h_pos[0], h_pos[-1] + 1]
            else:
                h_pos.append(h_pos[0] + 1)
                
            if len(t_pos) > 1:
                running_list = [i for i in range(min(t_pos), max(t_pos) + 1)]
                assert t_pos == running_list
                t_pos = [t_pos[0], t_pos[-1] + 1]
            else:
                t_pos.append(t_pos[0] + 1)
            if (t_pos[0] <= h_pos[-1] <= t_pos[-1]) or (h_pos[0] <= t_pos[-1] <= h_pos[-1]): # remove entities not separated by at least one token 
                    continue
                
            if do_lower_case: data['tokens'] = [token.lower() for token in data['tokens']]
                
            # add entity markers
            if h_pos[-1] < t_pos[0]:
                tokens = data['tokens'][:h_pos[0]] + ['[E1]'] + data['tokens'][h_pos[0]:h_pos[1]]\
                + ['[/E1]'] + data['tokens'][h_pos[1]:t_pos[0]] + ['[E2]'] + \
                data['tokens'][t_pos[0]:t_pos[1]] + ['[/E2]'] + data['tokens'][t_pos[1]:]
            else:
                tokens = data['tokens'][:t_pos[0]] + ['[E2]'] + data['tokens'][t_pos[0]:t_pos[1]]\
                + ['[/E2]'] + data['tokens'][t_pos[1]:h_pos[0]] + ['[E1]'] + \
                data['tokens'][h_pos[0]:h_pos[1]] + ['[/E1]'] + data['tokens'][h_pos[1]:]
                
            assert len(tokens) == (len(data['tokens']) + 4)
            sents.append(tokens)
        labels.append(relation)
    return sents, labels

def load_dataloaders(args, max_length=50000):
    
    if not os.path.isfile("./data/D.pkl"):
        logger.info("Loading pre-training data...")
        with open(args.pretrain_data, "r", encoding="utf8") as f:
            text = f.readlines()
        
        text = process_textlines(text)
        
        logger.info("Length of text (characters): %d" % len(text))
        num_chunks = math.ceil(len(text)/max_length)
        logger.info("Splitting into %d max length chunks of size %d" % (num_chunks, max_length))
        text_chunks = (text[i*max_length:(i*max_length + max_length)] for i in range(num_chunks))
        
        D = []
        logger.info("Loading Spacy NLP...")
        nlp = spacy.load("en_core_web_lg")
        
        for text_chunk in tqdm(text_chunks, total=num_chunks):
            D.extend(create_pretraining_corpus(text_chunk, nlp, window_size=40))
            
        logger.info("Total number of relation statements in pre-training corpus: %d" % len(D))
        save_as_pickle("D.pkl", D)
        logger.info("Saved pre-training corpus to %s" % "./data/D.pkl")
    else:
        logger.info("Loaded pre-training data from saved file")
        D = load_pickle("D.pkl")
        
    train_set = pretrain_dataset(args, D, batch_size=args.batch_size)
    train_length = len(train_set)

    return train_set

label_map = {"named_by": 0, "year_named": 1, "isLocatedIn": 2, "hasThickness": 3, "contains": 4}
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
