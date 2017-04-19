#!/usr/bin/env python
# encoding: utf-8
'''
Create on 2017年4月19日 下午12:30:15

@author:     wang

@version v1.0

@copyright:  2017 wang. All rights reserved.

'''
from keras.models import load_model

from rep.RepresentationLayer import RepresentationLayer
from util.FileUtils import readFile
import numpy as np

positive = 1
negtive = 0

max_len = 120
input_file = '../../data/final_corpus.txt'
word_vec_file = '/home/wang/PythonProjects/data/zhwiki_2017_03.sg_50d.word2vec'
model_path = '/home/wang/PythonProjects/data/LSTM.model'

def change_real2class(real_res_matrix):
    res_matrix = np.zeros_like(real_res_matrix, dtype=int)
    max_indexs = np.argmax(real_res_matrix, 1)
    for i in xrange(len(max_indexs)):
        res_matrix[i][max_indexs[i]] = 1
        
    return res_matrix

def eval_mulclass(ans_matrix, res_matrix, real=True):
    confuse_matrixs = np.zeros((ans_matrix.shape[1], 4))
    
    if real == True:
        res_matrix = change_real2class(res_matrix)
    
    class_indexs = np.argmax(ans_matrix, 1)
    for class_index in range(confuse_matrixs.shape[0]):
        for i in range(ans_matrix.shape[0]):
            if class_index == class_indexs[i]: #positive entry
                if res_matrix[i][class_index] == positive:
                    confuse_matrixs[class_index][0] += 1 #TP
                else:
                    confuse_matrixs[class_index][1] += 1 #FN
            else: #negtive entry
                if res_matrix[i][class_index] == positive:
                    confuse_matrixs[class_index][2] += 1 #FP
                else:
                    confuse_matrixs[class_index][3] += 1 #TN

    
    P, R = .0, .0    
    for i in range(confuse_matrixs.shape[0]-1):
#         print confuse_matrixs[i]
        p = confuse_matrixs[i][0]/(confuse_matrixs[i][0] + confuse_matrixs[i][2])
        r = confuse_matrixs[i][0]/(confuse_matrixs[i][0] + confuse_matrixs[i][1])
        P += p
        R += r
    P /= (confuse_matrixs.shape[0]-1)
    R /= (confuse_matrixs.shape[0]-1)
    F1 = 2*P*R/(P+R)
    print 'Evaluation for all the class'
    print 'P:    ', P
    print 'R:    ', R
    print 'F1:    ', F1
    print
    return F1

lines = readFile(input_file)
train_instances = [line.strip() for line in lines]
rep = RepresentationLayer(wordvec_file=word_vec_file, frequency=500000, max_sent_len=max_len)
label_array_t, word_array_t, dis_e1_array_t, dis_e2_array_t = rep.represent_instances(train_instances)

model = load_model(model_path)
label_array_ans = model.predict([word_array_t, dis_e1_array_t, dis_e2_array_t], batch_size=128)           

eval_mulclass(label_array_t, label_array_ans)
