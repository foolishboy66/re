#!/usr/bin/env python
# encoding: utf-8
'''
Create on 2017年4月11日 下午1:33:23

@author:     wang

@version v1.0

@copyright:  2017 wang. All rights reserved.

'''
from util.Constant import THREE, ONE, TWO


# 读取文件
def readFile(input_file):
    fp = open(input_file, 'r')
    lines = fp.readlines()
    fp.close()
    return lines
    
# 写入文件
def writeFile(output_file, lines):
    fp = open(output_file, 'w')
    for line in lines:
        fp.write(line)
        fp.write('\n')
    fp.close()

# 写入文件，无需换行
def writeFileOldLine(output_file, lines):
    fp = open(output_file, 'w')
    for line in lines:
        fp.write(line)
    fp.close()

# 获取'|'出现的第num个下标    
def find_content_begin_index(s, num=THREE):
    index = -1
    for i in range(num):
        index = s.find('|', index+1)
        i += 1
    return index 

# 获取'||'出现的下标
def find_content_end_index(s):
    return s.find('||')   

# 获取第一个实体的起始位置
def find_first_entity_begin_index(s):
    return s.find('{') 

# 获取第一个实体的结束位置
def find_first_entity_end_index(s):
    return s.find('}') - 1  

# 获取第二个实体的起始位置
def find_second_entity_begin_index(s):
    return s.rfind('{') - 2 

# 获取第二个实体的结束位置
def find_second_entity_end_index(s):
    return s.rfind('}') - 3   

# 获取句子内容
def getContent(line):
    begin_index = find_content_begin_index(line)
    end_index = find_content_end_index(line)
    content = line[begin_index + 1:end_index]
    return content

# 获取位置信息
def getPos(line):
    begin_index1 = find_content_begin_index(line, ONE)
    begin_index2 = find_content_begin_index(line, TWO)
    pos_str = line[begin_index1+1:begin_index2].split(' ')
    pos = map(int, pos_str)
    return pos

# 获取两个实体
def getEntity(line):
    pos = getPos(line)
    content = getContent(line)
    entity1 = content[pos[0]:pos[1]]
    entity2 = content[pos[2]:pos[3]]
    return entity1, entity2  

# 获取类型信息
def getType(line):
    begin_index1 = find_content_begin_index(line, TWO)
    begin_index2 = find_content_begin_index(line)
    type_str = line[begin_index1+1:begin_index2]
    return type_str  