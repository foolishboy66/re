#!/usr/bin/env python
# encoding: utf-8
'''
Create on 2017年4月18日 下午11:10:59

@author:     wang

@version v1.0

@copyright:  2017 wang. All rights reserved.

'''
from keras.engine.topology import Input
from keras.engine.training import Model
from keras.layers import merge
from keras.layers.core import Dropout, Dense
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.optimizers import RMSprop

from rep.RepresentationLayer import RepresentationLayer
from util.FileUtils import readFile

max_len = 120
word_vec_dim = 50
position_vec_dim = 10
epoch_size = 30
input_file = '../../data/final_corpus.txt'
word_vec_file = '/home/wang/PythonProjects/data/zhwiki_2017_03.sg_50d.word2vec'
output_file = '/home/wang/PythonProjects/data/LSTM.model'

lines = readFile(input_file)
rep = RepresentationLayer(wordvec_file=word_vec_file, frequency=500000, max_sent_len=max_len)

word = Input(shape=(max_len,), dtype='int32', name='word')
distance_e1 = Input(shape=(max_len,), dtype='int32', name='distance_e1')
distance_e2 = Input(shape=(max_len,), dtype='int32', name='distance_e2')

word_emb = Embedding(rep.vec_table.shape[0], rep.vec_table.shape[1],
                     weights = [rep.vec_table], mask_zero=True, input_length=max_len)
position_emb = Embedding(max_len * 2 + 1, position_vec_dim, mask_zero=True, input_length=max_len)

word_vec = word_emb(word)
distance1_vec = position_emb(distance_e1)
distance2_vec = position_emb(distance_e2)

# generate the input vector for LSTM
concatenated  = merge((word_vec, distance1_vec, distance2_vec), mode='concat')
dropouted = Dropout(0.5)(concatenated)

lstm = LSTM(100, activation='tanh')(dropouted)
dense = Dense(100, activation='tanh')(lstm)

#    cnn = Convolution1D(nb_filter=100, filter_length=3, activation='tanh')(concat_vec)
#    cnn = Convolution1D(nb_filter=100, filter_length=3, activation='tanh')(cnn)
#    flattened = Flatten()(cnn)
#    dense = Dense(100, activation='tanh')(flattened)

predict = Dense(2, activation='softmax')(dense)
model = Model(input=[word, distance_e1, distance_e2], output=predict)

opt = RMSprop(lr=0.001, rho=0.9, epsilon=1e-06)
#    opt = Adagrad(lr=0.01, epsilon=1e-06)
#    opt = Adadelta(lr=1.0, rho=0.95, epsilon=1e-06)
#    opt = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
#    opt = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=opt)
train_instances = [line.strip() for line in lines]
label_array_t, word_array_t, dis_e1_array_t, dis_e2_array_t = rep.represent_instances(train_instances)

model.fit([word_array_t, dis_e1_array_t, dis_e2_array_t],label_array_t, batch_size=128, epochs=epoch_size)
model.save(output_file)
label_array_ans = model.predict([word_array_t, dis_e1_array_t, dis_e2_array_t], batch_size=128)           
print(label_array_ans)
print("训练完成！！")
