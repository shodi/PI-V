#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math

class LVQ(object):
    def __init__(self, data_set, data_set_size, classes_qtd, radius):
        self.data_set = data_set
        self.data_set_size = data_set_size
        self.classes_qtd = classes_qtd
        self.radius = radius

    @staticmethod
    def get_random_value(init=0.1, final=1):
        return random.uniform(init, final)

    def get_initial_matrix(self, size):
        length = int(round(math.sqrt(self.classes_qtd * size)))
        matrix = [[LVQ.get_random_value() for i in range(length)] for i in range(length)]
        self.matrix = matrix

    def euclidean_distance(self, p, q, metric, skippable_indexes):
        for index, item in enumerate(q):
            if index in skippable_indexes or index == metric:
                continue
            _sum += (float(item) - float(p[index])) ** 2
        return math.sqrt(_sum)

if __name__ == '__main__':
    import csv
    files = ['iris_result']
    for _file in files:
        with open('../../../resources/spreadsheets/result/%s.csv' % _file, 'rb') as csv_file:
            data_set = []
            data_set_size = 0
            lines = csv.reader(csv_file, delimiter=';')
            for line in lines:
                aux = []
                for attr in line:
                    aux.append(float(attr))
                data_set.append(aux)
                data_set_size += 1
            lvq = LVQ(data_set, data_set_size, 3, 1)
            print(lvq.get_initial_matrix(10))

