#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from transformers import BertTokenizer

def preprocess_data(data_path, tokenizer_path):
    # Load data and tokenizer
    data = pd.read_csv(data_path)
    tokenizer = BertTokenizer.from_pretrained(tokenizer_path)

    # Tokenize sentences
    tokenized_data = data['sentence'].apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))
    return tokenized_data

