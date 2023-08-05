#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn import functional as F

def infer(model_path, tokenizer, sentence):
    model = BertForSequenceClassification.from_pretrained(model_path, num_labels=5)
    tokenized_sentence = tokenizer.encode(sentence)
    input_ids = torch.tensor([tokenized_sentence])
    with torch.no_grad():
        output = model(input_ids)
    label_indices = torch.argmax(output[0], axis=1)
    labels = ["named_by", "year_named", "isLocatedIn", "hasThickness", "contains"]
    predicted_label = labels[label_indices[0]]
    return predicted_label
