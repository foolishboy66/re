#!/usr/bin/env python
# encoding: utf-8
'''
Create on 2017年4月18日 下午10:49:56

@author:     wang

@version v1.0

@copyright:  2017 wang. All rights reserved.

'''
from util.FileUtils import readFile, writeFile

input_file = '../../data/newCropusSegment.txt'
output_file = '../../data/final_corpus.txt'

lines = readFile(input_file)
newLines = []
max_sent_len = 0
index = 0
for i in range(len(lines)):
    newLine = lines[i].strip().replace(' ', ' ')\
                          .replace('  ', ' ')\
                          .replace('   ', ' ')\
                          .replace('    ', ' ')\
                          .replace('     ', ' ')
    newLines.append(newLine)
    if len(newLine.split()) > max_sent_len:
        index = i
        max_sent_len = len(newLine.split())

print(max_sent_len, index)  
writeFile(output_file, newLines)
    