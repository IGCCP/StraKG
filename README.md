# Stratigraphic Knowledge Graph (StraKG)

## Overview
The background of this work is the increasing amount of geoscience literature data shared online, including those from governmental agencies, research institutions, and the crowdsourcing encyclopedia. The knowledge graph is an effective way to explore and analyze open-text data. In this work, we designed and constructed a knowledge graph for the field of the Stratigraphic Knowledge Graph, called StraKG, to help process records in the Baidu Encyclopedia, a big open-text data resource in Chinese. The files shared in this repository are code for building the layered structure of the GUKG and extracting instance records and relationships from the open text.

StraKG has a two-layer structure, representing ontologies and instances, respectively. At the top is the schema layer for classes and properties of the ontologies. Community-level geological dictionaries were used as a foundation to build ontologies. At the bottom is the instance layer. Text mining techniques were used to analyze open text from Baidu Encyclopedia, extracting instances of strata, rocks, and locations, as well as the relationships between those entities. In our work, we also established mapping between the schema layer and instance layer and implemented a list of experiments to test the utility of the resulting StraKG.

![Untitled Diagram-概念层](https://github.com/IGCCP/StraKG/assets/39733492/b75e6360-de5d-4c6f-9b50-31a5341e5c79)


## Requirements
Requirements: Python (3.6+), PyTorch (1.2.0+), Spacy (2.1.8+), py2neo (4.3.0)

Pre-trained BERT models: HuggingFace.co (https://huggingface.co); https://github.com/plkmo/BERT-Relation-Extraction

Visualization Platform: Neo4j (https://neo4j.com)

## Methods

* location.py   # Associated location information with strata in the instance layer
* main.py    # StraKG construction
* main_task.py   # Relationship extraction with BERT (Pre-training of Deep Bidirectional Transformers for Language Understanding)
* * /src   # Documents related to the training model (All the changes in task)

## Data
* instance.csv   # data in the instance layer
  * *Note: The last character of the full name in Chinese (the last word of the name in English) indicates the unit of this lithological stratum.*
    * *Fm(组): Formation*
    * *Gr(群): Group*
    * *Mem(段): Member*
    * *Sub-Gr(亚群): sub-group*
    * *complex(杂岩)* *Complex is an informal lithostratigraphic unit that refers to a large set of massively thick and complexly composed sedimentary* *,* *ejecta* *,* *or metamorphic strata that* *,* *to the extent that they have been studied, cannot be classified as a definitive formal lithostratigraphic unit*
* res copy.csv   # The data obtained from Baidu Encyclopedia (https://baike.baidu.com/)
* location.csv    # Chinese administrative division names and abbreviations (schema layer)
* geologic time.rdf    # geologic time in the schema layer
