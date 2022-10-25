# Stratigraphic Knowledge Graph (StraKG)

## Overview
The background of this work is the increasing amount of geoscience literature data shared online, including those from governmental agencies, research institutions, and the crowdsourcing encyclopedia. Knowledge graph is an effective way to explore and analyze the open text data. In this work, we designed and constructed a knoweldge graph for the field of stratigraph, called StraKG, to help process records in the Baidu Encyclopedia, a big open text data resource in Chinese. The files shared in this repository are code for building the layered structure of the StraKG and extracting instance records and relationships from open text. 

StraKG has a two-layer structure, representing ontologies and instances, respectively. At the top is the schema layer for classes and properties of the ontologies. Community-level geological dictionaries were used as a foundation to build the ontologies. At the bottom is the instance layer. Text mining techniques were used to to analyze open text from Baidu Encyclopedia, extracting instances of strata, rocks, locations and relationships between them. In our work we also established mapping between the schema layer and instance layer and implemented a list of experments to test the utility of the resulting StraKG.

## Requirements
Requirements: Python (3.6+), PyTorch (1.2.0+), Spacy (2.1.8+), py2neo (4.3.0)

Pre-trained BERT models courtesy of HuggingFace.co (https://huggingface.co)   
Visualization Platform: Neo4j (https://neo4j.com)

## Methods

* RESULT-EXAMPLE.csv   # Sample data for stratigraphic instance
* location.py   # Associated location information with strata in the instance layer
* main.py    # StraKG construction
* main_task.py   # Relationship extraction with BERT (Pre-training of Deep Bidirectional Transformers for Language Understanding)

## Data
* res copy.csv   # The data obtained from Baidu Encyclopedia (https://baike.baidu.com/)
* location.csv    # Chinese administrative division names and abbreviations
