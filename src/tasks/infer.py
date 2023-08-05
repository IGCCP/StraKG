#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn import functional as F

def infer(sentence, model_path, device):
    # Load pre-trained model and tokenizer
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model.to(device)
    model.eval()

    # Tokenize input sentence and obtain output logits
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=128)
    inputs = inputs.to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs[0]
    probs = F.softmax(logits, dim=1)
    return probs
