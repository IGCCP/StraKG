# -*- coding: utf-8 -*-

from src.tasks.trainer import train_and_fit
from src.tasks.infer import infer_from_trained
import logging
from argparse import ArgumentParser

logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger('__file__')

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--task", type=str, default='semeval', help='semeval')
    parser.add_argument("--train_data", type=str, default='./data/train.txt', help="training.txt file path") 
    parser.add_argument("--test_data", type=str, default='./data/test.txt', help="test.txt file path")
    parser.add_argument("--use_pretrained_blanks", type=int, default=0, help="0: Don't use pre-trained blanks model, 1: use pre-trained blanks model")
    parser.add_argument("--num_classes", type=int, default=19, help='number of relation classes')
    parser.add_argument("--batch_size", type=int, default=32, help="Training batch size")
    parser.add_argument("--gradient_acc_steps", type=int, default=2, help="No. of steps of gradient accumulation")
    parser.add_argument("--max_norm", type=float, default=1.0, help="Clipped gradient norm")
    parser.add_argument("--fp16", type=int, default=0, help="1: use mixed precision ; 0: use floating point 32")
    parser.add_argument("--num_epochs", type=int, default=11, help="No of epochs")
    parser.add_argument("--lr", type=float, default=0.00007, help="learning rate")
    parser.add_argument("--model_no", type=int, default=0, help='''Model ID: 0 - BERT''')
    parser.add_argument("--model_size", type=str, default='bert-base-uncased', help="For BERT: 'bert-base-uncased'")
    parser.add_argument("--train", type=int, default=1, help="0: Don't train, 1: train")
    parser.add_argument("--infer", type=int, default=1, help="0: Don't infer, 1: Infer")
    
    args = parser.parse_args()
    
    if args.train == 1:
        net = train_and_fit(args)
        
    if args.infer == 1:
        inferer = infer_from_trained(args, detect_entities=True)
        test = "[E1]苇子峪组[/E1]本组以[E2]石榴透辉角闪斜长片麻岩[/E2]、角闪辉石麻粒岩为主"
        inferer.infer_sentence(test, detect_entities=False)
        test2 = "大梨沟组命名山西地矿局二一四队，1993年命名。"
        inferer.infer_sentence(test2, detect_entities=True)
        
        while True:
            sent = input("Type input sentence ('quit' or 'exit' to terminate):\n")
            if sent.lower() in ['quit', 'exit']:
                break
            inferer.infer_sentence(sent, detect_entities=False)
