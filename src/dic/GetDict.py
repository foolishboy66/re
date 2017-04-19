#!/usr/bin/env python
# encoding: utf-8
'''
Create on 2017年4月11日 下午3:43:23

@author:     wang

@version v1.0

@copyright:  2017 wang. All rights reserved.

'''
from pre.GetData import getContent
from util.Constant import E1_B, E1_E, E2_B, E2_E, GENE, DISEASE
from util.FileUtils import readFile, getPos, writeFile


input_file = '../../data/new_GAD1-1000.txt'
output_file = '../../data/dic.txt'

# def getPos(line):
#     begin_index1 = find_content_begin_index(line, ONE)
#     begin_index2 = find_content_begin_index(line, TWO)
#     pos_str = line[begin_index1+1:begin_index2].split(' ')
#     pos = map(int, pos_str)
#     return pos
#    
# def getContent(line):
#     begin_index = find_content_begin_index(line)
#     end_index = find_content_end_index(line)
#     content = line[begin_index + 1:end_index]
#     return content

def setEntity(entity, dicts):
    if entity in dicts:
        dicts[entity] += 1
    else:
        dicts[entity] = 1

lines = readFile(input_file)
dicts = {}
print('开始构建词典...')
for line in lines:
    pos = getPos(line)
    content = getContent(line)
    
    entity1 = content[pos[0]:pos[1]]
    entity2 = content[pos[2]:pos[3]]
    setEntity(entity1, dicts)
    setEntity(entity2, dicts)

dicts[E1_B] = len(lines)
dicts[E1_E] = len(lines)
dicts[E2_B] = len(lines)
dicts[E2_E] = len(lines)
dicts[GENE] = len(lines)
dicts[DISEASE] = len(lines)
    
contents = []
for name in dicts:
    content = name + ' ' + str(dicts[name])
    contents.append(content)
    
writeFile(output_file, contents)
print('恭喜，词典构建成功！')