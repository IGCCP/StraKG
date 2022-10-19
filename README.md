# Stratigraphic Knowledge Graph (StraKG)

## Overview
Our work designed and constructed a Stratigraphic Knowledge Graph (StraKG) to explore some novel approach in geoscience data mining and understanding. StraKG provides a new approach to analyze the open and big literature data in geoscience in the form of knowledge graphs.

In our work, StraKG has two layers: schema layer and instance layer. In the schema layer, we used community-recognized terminology from geological dictionaries. In the instance layer, we used natural language processing techniques to analyze open data (Baidu Encyclopedia) and obtained relationships between strata and entities such as rocks and spatial locations.

## Requirements
Requirements: Python (3.6+), PyTorch (1.2.0+), Spacy (2.1.8+), py2neo (4.3.0)

Pre-trained BERT models courtesy of HuggingFace.co (https://huggingface.co)   

## Methods

* RESULT-EXAMPLE.csv   # Sample data for stratigraphic instance
* location.py   # Associated Location Information with strata in the Instance Layer
* main.py    # StraKG construction


## Data
* res copy.csv   # The data obtained from Baidu's encyclopedia
* location.csv    # Chinese administrative division names and abbreviations
