#!/usr/bin/env python
# encoding: utf-8
'''
Create on 2017年4月18日 下午11:10:59

@author:     wang

@version v1.0

@copyright:  2017 wang. All rights reserved.

'''
from present import RepresentationLayer


max_len = 120
word_vec_dim = 50
position_vec_dim = 10
epoch_size = 10
rep = RepresentationLayer(wordvec_file='/home/wang/PythonProjects/data/zhwiki_2017_03.sg_50d.word2vec',
                          frequency = 500000, max_sent_len=max_len)



