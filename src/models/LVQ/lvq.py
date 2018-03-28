#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math

class LVQ(object):
    def __init__(self, data_set, data_set_size, classes_qtd, radius):
        self.data_set = data_set
        self.data_set_size = data_set_size
        self.classes_qtd = classes_qtd
        self.desvio_padrao = radius
        # self.const_t1 = 1000 / math.log(self.desvio_padrao)
        self.taxa_aprendizado = 0.1
        self.decaimento_aprendizado = 1000

    @staticmethod
    def get_random_value(init=0.1, final=1):
        return random.uniform(init, final)

    def get_initial_matrix(self, size):
        length = int(round(math.sqrt(self.classes_qtd * size)))
        matrix = [[LVQ.get_random_value() for i in range(length)] for i in range(length)]
        self.matrix = matrix

    def get_best_matching_unit(self, data_set, row_test):
        distances = []
        for instance in data_set:
            dist = self.euclidean_distance(instance, row_test, 5, [5])
            distances.append((instance, dist))
        distances.sort(key=lambda distance: distance[1])
        return distances[0][0]

    def train(self, epochs=10):
        self.get_initial_matrix(10)
        for epoch in range(epochs):
            rate = self.taxa_aprendizado * (1.0 - (epoch/float(epochs)))
            sum_error = 0.0
            for row in self.data_set:
                bmu = self.get_best_matching_unit(self.matrix, row)
                for i in range(len(row) - 1):
                    error = row[i] - bmu[i]
                    sum_error += error**2
                    if bmu[-1] == row[-1]:
                        bmu[i] = bmu[i] + rate * (row[i] - bmu[i])
                    else:
                        bmu[i] = bmu[i] - rate * (row[i] - bmu[i])
            print('>iteracao=%d, taxa=%.3f, error=%.3f' % (epoch, rate, sum_error))
        return self.matrix


    def euclidean_distance(self, p, q, metric, skippable_indexes):
        _sum = 0
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
            lvq.train()

