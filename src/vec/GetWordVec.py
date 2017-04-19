#!/usr/bin/env python
# encoding: utf-8
'''
Create on 2017年4月11日 下午1:50:37

@author:     wang

@version v1.0

@copyright:  2017 wang. All rights reserved.

'''
import word2vec


input_file = '../../data/corpusSegDone.txt'
output_file = '../../data/corpusWordVec.emb'

word2vec.word2vec(input_file, output_file, size=50, cbow=0, window=7, 
         min_count=1, negative=0, hs=1, threads=12, binary=0, verbose=True);

