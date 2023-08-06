# -*- coding: utf-8 -*-

from py2neo import Graph, Node, Relationship, NodeMatcher
import csv

# Connect to neo4j database, enter address, username, password
graph = Graph("bolt://localhost:7687", auth=("neo4j", '123456'))
graph.delete_all()

## Concept layer
# Geographic ontology
with open('./location_res/location.csv', 'r', encoding='utf-8') as f1:
    reader1 = csv.reader(f1)
    data1 = list(reader1)
    print(len(data1))

noden = Node(DM='GeoLocation', cn='中国地名', yn='Chinese Geographical Names', bz='China Administrative Units')
graph.create(noden)

for i in range(0, len(data1)):
    node = Node('Province', code=data1[i][0], cfn=data1[i][1], cn=data1[i][2],
                bn=data1[i][3], qy=data1[i][5], yn=data1[i][6])
    node_ = Node('Capital', sh=data1[i][4])
    graph.create(node)
    graph.create(node_)
    relation = Relationship(noden, 'hasProvince', node)
    relation_ = Relationship(node, 'isCapital', node_)
    graph.create(relation)
    graph.create(relation_)

# Rock ontology  Relationship type: subclassOf; Node label: Rock
nodeRock = Node('Rock', DM='YSEB', HZM='岩石', YYM='rock', BZ='Petrology')

with open('./chaifen_res/rock.csv', 'r', encoding='utf-8') as fR:
    readerR = csv.reader(fR)
    dataR = list(readerR)

for i in range(0, len(dataR)):
    nodeR = Node('Rock', DM=dataR[i][0], HZM=dataR[i][1], YYM=dataR[i][2], BZ=dataR[i][3])
    graph.create(nodeR)
    relationshipR = Relationship(nodeR, 'isInstance', nodeRock)
    graph.create(relationshipR)

# Geologic time ontology  Relationship type: subclassOf; Node label: Geotime
with open('./geotime.csv', 'r', encoding='utf-8') as ft:
    readert = csv.reader(ft)
    datat = list(readert)
    print(len(datat))

Node1 = Node('Geotime', cn='元古宇', yn='Proterozoic Eonothem')
Node2 = Node('Geotime', cn='太古宇', yn='Archean Eonothem')
Node3 = Node('Geotime', cn='古生界', yn='Paleozoic')
Node4 = Node('Geotime', cn='中生界', yn='Mesozoic Erathem')
Node5 = Node('Geotime', cn='新生界', yn='Cenozoic Erathem')
graph.create(Node1)
graph.create(Node2)
graph.create(Node3)
graph.create(Node4)
graph.create(Node5)

for i in range(0, len(datat)):
    node1 = Node('Geotime', cn=datat[i][1], code=datat[i][2])
    graph.create(node1)
    if i < 6:
        rel = Relationship(node1, 'subclass', Node1)
        graph.create(rel)
        for j in range(3,12):
            if datat[i][j]:
                node0 = Node('Geotime', code=datat[i][j])
                rel0 = Relationship(node0, 'subclass', node1)
                graph.create(node0)
                graph.create(rel0)
    elif i==6:
        rel = Relationship(node1, 'subclass', Node2)
        graph.create(rel)
        for j in range(3,12):
            if datat[i][j]:
                node0 = Node('Geotime', code=datat[i][j])
                rel0 = Relationship(node0, 'subclass', node1)
                graph.create(node0)
                graph.create(rel0)
    elif 6<i<15:
        rel = Relationship(node1, 'subclass', Node3)
        graph.create(rel)
        for j in range(3,12):
            if datat[i][j]:
                node0 = Node('Geotime', code=datat[i][j])
                rel0 = Relationship(node0, 'subclass', node1)
    elif 14<i<18:
        rel = Relationship(node1, 'subclass', Node4)
        graph.create(rel)
        for j in range(3,12):
            if datat[i][j]:
                node0 = Node('Geotime', code=datat[i][j])
                rel0 = Relationship(node0, 'subclass', node1)
                graph.create(node0)
                graph.create(rel0)
    else:
        rel = Relationship(node1, 'subclass', Node5)
        graph.create(rel)
        for j in range(3,12):
            if datat[i][j]:
                node0 = Node('Geotime', code=datat[i][j])
                rel0 = Relationship(node0, 'subclass', node1)
                graph.create(node0)
                graph.create(rel0)

## Instance layer; link the different ontology in the concept layer
with open('./baike/mergeRock.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    data = list(reader)
    print(len(data))

NodeS = Node('Strata', yn = 'Strata')
for i in range(1, len(data)):
    node1 = Node('Strata', cn=data[i][1], yn=data[i][2], alias=data[i][4],
                distribution=data[i][5], bz=data[i][6], code=data[i][0])
    graph.create(node1)
    reltionshipS = Relationship(node1, 'isInstance', NodeS)

    # Determine whether the node already exists
    for j in range(7, 21):
        nodelocation = graph.evaluate('match (x:Province) where x.yn="' + data[i][j] + '" return(x)')
        if nodelocation:
            Node_name = nodelocation
            relation1 = Relationship(node1, 'islocated', Node_name)
            graph.create(relation1)

    # Determine whether the node already exists
    nodegeotime = graph.evaluate('match (x:Geotime) where x.code="' + data[i][3] + '" return(x)')
    if nodegeotime:
        Node_name1 = nodegeotime
        relation2 = Relationship(node1, 'hasGeotime', Node_name1)
        graph.create(relation2)
    else:
        node3 = Node('Geotime', code=data[i][3])
        print(data[i][3])
        graph.create(node3)
        relation2 = Relationship(node1, 'hasGeotime', node3)
        graph.create(relation2)

    # Determine whether the node already exists
    for j in range(22, 74):
        noderock_ = graph.evaluate('match (x:Rock) where x.HZM="' + data[i][j] + '" return(x)')
        if noderock_:
            Node_nameR = noderock_
            relation3 = Relationship(node1, 'contain', Node_nameR)
            graph.create(relation3)

print('over')
