#!/usr/bin/env python
# encoding: utf-8
'''
Create on 2017年4月18日 下午9:58:16

@author:     wang

@version v1.0

@copyright:  2017 wang. All rights reserved.

'''
import jieba

from util.Constant import E1_B, E1_E, E2_B, E2_E
from util.FileUtils import readFile, getType, getContent


def getLabel(line):
    index = line.find('(')
    return line[:index]

def replaceWithE(content):
    index1 = content.find('{') 
    index2 = content.find('}') 
    index3 = content.rfind('{') 
    index4 = content.rfind('}')
    newContent = content[:index1] + E1_B + content[index1 + 1:index2] + \
        E1_E + content[index2 + 1:index3] + E2_B + content[index3 + 1:index4] + \
        E2_E + content[index4 + 1:]
    return newContent

input_file = '../../data/GAD1-1000.txt'
input_file_eng = '../../data/GAD1-1000_lab.txt'
output_file = '../../data/newCropusSegment.txt'
dict_file = '../../data/dic.txt'

lines = readFile(input_file)
lab_lines = readFile(input_file_eng)

jieba.load_userdict(dict_file)

newLines = []
for i in range(len(lines)):
    label = getLabel(lab_lines[i])
    type = getType(lines[i])
    content = getContent(lines[i])
    newContent = replaceWithE(content)
    
    newLine = label + type + newContent
    
    newLines.append(' '.join(list(jieba.cut(newLine, cut_all=False))))
    
fp = open(output_file, 'w')
for i in range(len(newLines)):
    fp.write(newLines[i].encode('utf-8'))
    fp.write('\n')
fp.close()
