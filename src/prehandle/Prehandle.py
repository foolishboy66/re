#!/usr/bin/env python
# encoding: utf-8
'''
Create on 2017年4月11日 下午12:22:13

@author:     wang

@version v1.0

@copyright:  2017 wang. All rights reserved.

'''

from util.FileUtils import readFile, writeFile, find_content_begin_index, find_content_end_index

input_file = '../../data/new_GAD1-1000.txt'
output_file = '../../data/corpus.txt'

file_lines = readFile(input_file)
lines = []
for line in file_lines:
    begin_index = find_content_begin_index(line)
    end_index = find_content_end_index(line)
    lines.append(line[begin_index+1:end_index])

writeFile(output_file, lines)