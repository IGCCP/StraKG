#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from transformers import BertTokenizer

from transformers import BertTokenizer
from tqdm import tqdm
import torch

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
        mask_id = [1] * len(token_id) + padding
        segment_id = [0] * max_len
        token_id += padding
        token_ids.append(token_id)
        mask_ids.append(mask_id)
        segment_ids.append(segment_id)

    label_ids = labels
    return torch.tensor(token_ids), torch.tensor(mask_ids), torch.tensor(segment_ids), torch.tensor(label_ids)

label_map = {"named_by": 0, "year_named": 1, "isLocatedIn": 2, "hasThickness": 3, "contains": 4}
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
