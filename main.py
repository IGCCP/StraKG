# -*- coding: utf-8 -*-
import xlrd
from py2neo import Graph, Node, Relationship, NodeMatcher
import csv

# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph("bolt://localhost:7687", username="neo4j", password='123456')
graph.delete_all()

'''
nodeRock = Node('Rock', DM='YSEB', HZM='岩石', YYM='rock', BZ='Petrology')
with open('./chaifen_res/rock.csv', 'r', encoding='utf-8') as fR:
    readerR = csv.reader(fR)
    dataR = list(readerR)

for i in range(0, len(dataR)):
    # print(dataR[i])
    nodeR = Node('Rock', DM=dataR[i][0], HZM=dataR[i][1], YYM=dataR[i][2], BZ=dataR[i][3])
    graph.create(nodeR)
    relationshipR = Relationship(nodeR, 'isInstance', nodeRock)
    # relationshipR_ = Relationship(nodeRock, 'hasInstance', nodeR)
    graph.create(relationshipR)
    # graph.create(relationshipR_)
    '''
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

'''
for j in range(22, 74):
        noderock_ = graph.evaluate('match (x:Rock) where x.HZM="' + data[i][j] + '" return(x)')
        if noderock_:
            Node_nameR = noderock_
            relation3 = Relationship(node1, 'contain', Node_nameR)
            graph.create(relation3)'''


'''
readbook = xlrd.open_workbook('./chaifen_res/rock.xls', 'r')
# 获取读入的文件的sheet
sheet = readbook.sheet_by_index(0)  #索引的方式，从0开始
# 获取sheet的最大行数和列数
nrows = sheet.nrows #行
ncols = sheet.ncols #列
#print(nrows,ncols)  # 5147 4
'''

'''
# 获取某个单元格的值
lng = sheet.cell(i,1).value#获取i行1列的表格值
lat = sheet.cell(i,2).value#获取i行2列的表格值
'''
'''
# ROCK
nodeRock = Node('Rock', DM='YSEB', cn='岩石', yn='rock', bz='Petrology')

with open('./chaifen_res/rock.csv', 'r', encoding='utf-8') as fR:
    readerR = csv.reader(fR)
    dataR = list(readerR)

for i in range(0, len(dataR)):
    #print(dataR[i])
    nodeR = Node('Rock', DM=dataR[i][0], HZM=dataR[i][1], YYM=dataR[i][2], BZ=dataR[i][3])
    graph.create(nodeR)
    relationshipR = Relationship(nodeR, 'isInstance', nodeRock)
    relationshipR_ = Relationship(nodeRock, 'hasInstance', nodeR)
    graph.create(relationshipR)
    graph.create(relationshipR_)'''

print('down')

