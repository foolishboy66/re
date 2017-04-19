#!/usr/bin/env python
# encoding: utf-8
'''
Create on 2017年4月11日 下午12:20:07

@author:     wang

@version v1.0

@copyright:  2017 wang. All rights reserved.

'''



from util.FileUtils import readFile
import jieba
input_file = '../../data/corpus.txt'
output_file = '../../data/corpusSegDone.txt'
dict_file = '../../data/dictionary.txt'

jieba.load_userdict(dict_file)
lines = readFile(input_file)

segLines = []
for line in lines:
    segLines.append(' '.join(list(jieba.cut(line, cut_all=False))))
    
fp = open(output_file, 'w')
for i in range(len(segLines)):
    fp.write(segLines[i].encode('utf-8'))
fp.close()