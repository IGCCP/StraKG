import os
import torch
import torch.nn as nn
from seqeval.metrics import precision_score, recall_score, f1_score
from ..misc import save_as_pickle, load_pickle
import logging
from tqdm import tqdm

def load_state(model, optimizer, model_num, load_best=True):
    """
    Load saved model and optimizer states if they exist.
    """
    if load_best:
        checkpoint = torch.load(f'model_best_{model_num}.pt')
    else:
        checkpoint = torch.load(f'model_checkpoint_{model_num}.pt')
    
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    
    return model, optimizer

def load_results(model_num):
    """
    Load saved results (losses, accuracy, and F1 scores) for a given model number if they exist.
    """
    results = torch.load(f'results_{model_num}.pt')
    return results

def evaluate_(true_labels, pred_labels, ignore_index=-100):
    """
    Evaluate the model's output against the true labels.
    """
    true_labels = true_labels[true_labels != ignore_index]
    pred_labels = pred_labels[true_labels != ignore_index]
    accuracy = accuracy_score(true_labels, pred_labels)
    return accuracy

def evaluate_results(true_labels, pred_labels):
    """
    Evaluate the model on test samples.
    """
    accuracy = accuracy_score(true_labels, pred_labels)
    precision = precision_score(true_labels, pred_labels, average='macro')
    recall = recall_score(true_labels, pred_labels, average='macro')
    f1 = f1_score(true_labels, pred_labels, average='macro')
    
    return accuracy, precision, recall, f1
