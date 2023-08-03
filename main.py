# -*- coding: utf-8 -*-
import xlrd
from py2neo import Graph, Node, Relationship, NodeMatcher
import csv

# Connect to neo4j database, enter address, username, password
graph = Graph("bolt://localhost:7687", username="neo4j", password='123456')
graph.delete_all()

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

with open('./baike/mergeRock.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    data = list(reader)
    print(len(data))


for i in range(1, len(data)):
    # print(i)
    node1 = Node('Strata', cn=data[i][1], yn=data[i][2], alias=data[i][4],
                 distribution=data[i][5], bz=data[i][6], code=data[i][0])
    # print(data[i][1])
    graph.create(node1)

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

