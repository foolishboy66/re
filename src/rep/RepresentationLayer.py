#!/usr/bin/env python
# encoding: utf-8
'''
Create on 2017年4月15日 下午4:03:50

@author:     wang

@version v1.0

@copyright:  2017 wang. All rights reserved.

'''

import numpy as np
from util.Constant import DISEASE, CHEMICAL, GENE, TRUE, FALSE, PADDING, SPARSE, \
    E1_B, E1_E, E2_B, E2_E

class RepresentationLayer(object):
    
    def __init__(self, wordvec_file=None, frequency=500000, scale=1
                 , max_sent_len=120, output_size=2):
        '''
        vec_size        :    the dimension size of word vector

        frequency       :    the threshold for the words left according to
                             their frequency appeared in the text
                             for example, when frequency is 10000, the most
                             frequent appeared 10000 words are considered
        
        scale           :    the scaling for the vectors' each real value
                             when the vectors are scaled up it will accelerate
                             the training process

        max_sent_len    :   all sentences will be cuted or padded to the max_sent_len size
        
        vec_talbe        :    a matrix each row stands for a vector of a word

        word_index        :    the map from word to corresponding index in vec_table
        
        distance_2_index    : the map from a word's relative distance to corresponding vector's index

        '''
        self.frequency = frequency
        self.scale = scale
        self.max_sent_len = max_sent_len

        self.vec_table, self.word_2_index, self.index_2_word, self.vec_size = self.load_wordvecs(wordvec_file)

        self.entity_type_2_index = {DISEASE:0, GENE:1, CHEMICAL:2}

        self.label_2_index = {TRUE:[1,0], FALSE:[0,1]}

        self.distance_2_index = self.load_dis_index_table()

        self.y_dim = output_size
        
    def load_dis_index_table(self):
        distance_2_index = {}
        index = 1
        for i in range(-self.max_sent_len, self.max_sent_len):
            distance_2_index[i] = index
            index += 1
        return distance_2_index

    def load_wordvecs(self, wordvec_file):
        file = open(wordvec_file)
        first_line = file.readline()
        word_count = int(first_line.split()[0])
        dimension = int(first_line.split()[1])
        vec_table = np.zeros((word_count, dimension))
        word_2_index = {PADDING:0}
        index_2_word = {0:PADDING}
        padding_vector = np.zeros(dimension)
        for col in xrange(dimension):
            vec_table[0][col] = padding_vector[col]

        row = 1
        for line in file:
            if row < self.frequency:
                line_split = line[:-1].split()
                word_2_index[line_split[0]] = row
                index_2_word[row] = line_split[0]
                for col in xrange(dimension):
                    vec_table[row][col] = float(line_split[col + 1])
                row += 1
            else:
                break
        
        word_2_index[SPARSE] = row
        index_2_word[row] = SPARSE
        sparse_vectors = np.zeros(dimension)
        for line in file:
            line_split = line[:-1].split()[1:]
            for i in xrange(dimension):
                sparse_vectors[i] += float(line_split[i])

        sparse_vectors /= (word_count - self.frequency)

        for col in xrange(dimension):
            vec_table[row][col] = sparse_vectors[col]
        vec_table *= self.scale
        
        file.close()

        return vec_table, word_2_index, index_2_word, dimension

    def generate_distance_features(self, left_part, e1, middle_part, e2, right_part):
        distance_e1 = []
        distance_e2 = []
        len_left = len(left_part)
        len_middle = len(middle_part)
        len_right = len(right_part)

        ### left part
        for i in range(len_left):
            # simplify of -(len_left - i)
            # for position feature about entry1
            distance_e1.append(i - len_left)

            # simplify of -(len_left - i + 1 + len_middle)
            # for position feature about entry2 where 1 stand for len of entry1
            distance_e2.append(i - len_left - 1 - len_middle)

        ### entry1 part
        for e in e1:
            # for position feature about entry1
            distance_e1.append(-self.max_sent_len)

            # for position feature about entry2
            distance_e2.append(-len_middle)

        ### middle part
        for i in range(len_middle):
            # for position feature about entry1
            distance_e1.append(i + 1)

            # simplify of -(len_middle - i)
            # for position feature about entry2
            distance_e2.append(i - len_middle)

        ### entry2 part
        for e in e2:
            # for position feature about entry1
            distance_e1.append(len_middle)

            # for position feature about entry2
            distance_e2.append(-self.max_sent_len)

        ### right part
        for i in range(len_right):
            if right_part[i] == PADDING:
                distance_e1.append(0)
                distance_e2.append(0)
            else:
                # for position feature about entry1
                # where the first 1 stand for the len of entry2
                distance_e1.append(len_middle + 1 + i + 1)
    
                # for position feature about entry2
                distance_e2.append(i + 1)

        return distance_e1, distance_e2


    def represent_instances(self, instances):

        label_list = []
        word_index_list = []
        distance_e1_index_list = []
        distance_e2_index_list = []
        for instance in instances:
            label, word_indexs, distance_e1_indexs, distance_e2_indexs = self.represent_instance(instance)
            if label == None:
                continue
            label_list.extend(self.label_2_index[label])
            word_index_list.extend(word_indexs)
            distance_e1_index_list.extend(distance_e1_indexs)
            distance_e2_index_list.extend(distance_e2_indexs)

        label_array = np.array(label_list)
        label_array = label_array.reshape((len(label_array)/self.y_dim, self.y_dim))

        word_array = np.array(word_index_list)
        word_array = word_array.reshape((word_array.shape[0]/self.max_sent_len, self.max_sent_len))

        dis_e1_array = np.array(distance_e1_index_list)
        dis_e1_array = dis_e1_array.reshape((dis_e1_array.shape[0]/self.max_sent_len, self.max_sent_len))

        dis_e2_array = np.array(distance_e2_index_list)
        dis_e2_array = dis_e2_array.reshape((dis_e2_array.shape[0]/self.max_sent_len, self.max_sent_len))

        return label_array, word_array, dis_e1_array, dis_e2_array

    def represent_instance(self, instance):

        splited = instance.split(' ')
        label = splited[0]
        sent = splited[3: 3 + self.max_sent_len + 4]

        index_e1_b, index_e1_e, index_e2_b, index_e2_e = -1, -1, -1, -1
        padding_num = 0

        # the extra 4 stands for the 4 words,
        # including entity1begin, entity1end,entity2begin, entity2end
        for index in range(self.max_sent_len + 4):
            if index > len(sent) - 1:
                padding_num += 1
                continue
            if sent[index] == E1_B:
                index_e1_b = index
            elif sent[index] == E1_E:
                index_e1_e = index
            elif sent[index] == E2_B:
                index_e2_b = index
            elif sent[index] == E2_E:
                index_e2_e = index

        # the max length sentence won't contain the
        # two entities
        if index_e2_e == -1:
            return None,None,None,None

        left_part = sent[:index_e1_b]
        e1 = sent[index_e1_b + 1: index_e1_e]
        middle_part = sent[index_e1_e + 1: index_e2_b]
        e2 = sent[index_e2_b + 1:index_e2_e]
        right_part = sent[index_e2_e + 1:] + [PADDING for i in range(padding_num)]

        distance_e1, distance_e2 = self.generate_distance_features(left_part, e1, middle_part, e2, right_part)

        distance_e1_index_list = self.replace_distances_with_indexs(distance_e1)
        distance_e2_index_list =  self.replace_distances_with_indexs(distance_e2)

        word_list = left_part + e1 + middle_part + e2 + right_part
        word_index_list = self.replace_words_with_indexs(word_list)

        return label, word_index_list, distance_e1_index_list, distance_e2_index_list

    '''
        replace word list with corresponding indexs
        
    '''
    def replace_words_with_indexs(self, words):
        word_indexs = []
        for word in words:
            if self.word_2_index.has_key(word):
                word_indexs.append(self.word_2_index[word])
            else:
                word_indexs.append(self.word_2_index[SPARSE])
        
        return word_indexs

    '''
        replace distance list with corresponding indexs

    '''
    def replace_distances_with_indexs(self, distances):
        distance_indexs = []
        for distance in distances:
            if distance == 0:
                distance_indexs.append(0)
                continue
            if self.distance_2_index.has_key(distance):
                distance_indexs.append(self.distance_2_index[distance])
            else:
                print 'Impossible! This program will stop!'
                # sys.exit(0)

        return distance_indexs

if __name__ == '__main__':
    rep = RepresentationLayer(wordvec_file='/home/wang/PythonProjects/data/zhwiki_2017_03.sg_50d.word2vec',
                              frequency=50000)
    
    instance = 'false 基因  疾病 这些 结果表明 entity1begin HIF - 1 α entity1end 中 的 C1772T 多态性 与 entity2begin 结肠直肠癌 entity2end 的 发展 或 转移 无关 。'
    label, word_index_list, distance_e1_index_list, distance_e2_index_list = rep.represent_instance(instance)
    print instance
    print label
    print word_index_list
    print distance_e1_index_list
    print distance_e2_index_list