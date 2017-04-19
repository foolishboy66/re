#!/usr/bin/env python
# encoding: utf-8
'''
Created on 2017年4月12日 上午9:46:10
 
@author: wang

@version v1.0

@copyright:  2017 wang. All rights reserved.

'''

from util.Constant import ONE, TWO
from util.FileUtils import readFile, find_content_begin_index, \
    find_first_entity_begin_index, find_first_entity_end_index, \
    find_second_entity_begin_index, find_second_entity_end_index, \
    writeFileOldLine, getContent


# def getContent(line):
#     begin_index = find_content_begin_index(line)
#     end_index = find_content_end_index(line)
#     content = line[begin_index + 1:end_index]
#     return content

def getPos(content):
    pos1 = find_first_entity_begin_index(content)
    pos2 = find_first_entity_end_index(content)
    pos3 = find_second_entity_begin_index(content)
    pos4 = find_second_entity_end_index(content)
    return [pos1, pos2, pos3, pos4]

def getNewPos(content):
    pos = getPos(content)
    return ' '.join([str(p) for p in pos])

def getOldPos(line):
    begin_index1 = find_content_begin_index(line, ONE)
    begin_index2 = find_content_begin_index(line, TWO)
    return line[begin_index1 + 1:begin_index2]

def trim(content):
#     print(content)
    content = content.strip('{}')
    index1 = content.find('{') 
    index2 = content.find('}') 
    index3 = content.rfind('{') 
    index4 = content.rfind('}')
    indexs = set([index1, index2, index3, index4])
    nums = []
    for num in indexs:
        nums.append(num)
    nums.sort()
    size = len(nums)
    newContent = content[:nums[0]]
    for i in range(size - 1):
        newContent += content[nums[i] + 1:nums[i + 1]]
    
    newContent += content[nums[size - 1] + 1:]
#     print(newContent)
    return newContent

input_file = '../../data/GAD1-1000.txt'
output_file = '../../data/new_GAD1-1000.txt'

file_lines = readFile(input_file)
lines = []

for line in file_lines:
    content = getContent(line)
    newPos = getNewPos(content)
    oldPos = getOldPos(line)
    newContent = trim(content)
    line = line.replace(oldPos, newPos)
    line = line.replace(content, newContent)
    lines.append(line)
    
writeFileOldLine(output_file, lines)
    
