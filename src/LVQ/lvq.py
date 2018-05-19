#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import math

class LVQ(object):
    def __init__(self, data_set, classes_qtd, radius, qtd_attr, skippable_indexes=[], metric=-1):
        self.data_set = data_set
        self.data_set_size = len(data_set)
        self.classes_qtd = classes_qtd
        self.desvio_padrao = radius
        # self.const_t1 = 1000 / math.log(self.desvio_padrao)
        self.taxa_aprendizado = 0.1
        self.decaimento_aprendizado = 1000
        self.skippable_indexes = skippable_indexes
        self.quantidade_atributos = qtd_attr
        self.metric = metric

    @staticmethod
    def get_random_value(init=0.1, final=1):
        return random.uniform(init, final)

    def get_initial_matrix(self, size):
        length = int(round(math.sqrt(self.classes_qtd * size)))
        matrix = [
            [LVQ.get_random_value() if i != self.quantidade_atributos - 1 else None for i in range(self.quantidade_atributos)] 
            for i in range(length)]
        self.matrix = matrix

    def get_learning_rate(self, iteration):
        self.taxa_aprendizado = self.taxa_aprendizado * math.exp(-(0.1 / 1000.0))
        return self.taxa_aprendizado

    def get_best_matching_unit(self, data_set, row_test):
        distances = []
        for instance in data_set:
            dist = self.euclidean_distance(instance, row_test)
            distances.append((instance, dist))
        distances.sort(key=lambda distance: distance[1])
        return distances[0][0]

    def train(self, epochs=500):
        self.get_initial_matrix(10)
        for epoch in range(epochs + 1):
            rate = self.get_learning_rate(epoch)
            for row in self.data_set:
                bmu = self.get_best_matching_unit(self.matrix, row)
                for i in range(len(row) - 1):
                    if i == self.metric or i in self.skippable_indexes:
                        continue
                    self.update_neighbours(bmu, row, i, rate)
                print('>iteracao=%d, taxa=%f' % (epoch, rate))
        return self.matrix

    def update_neighbours(self, bmu, row, index, rate):
        # matched é um booleando que diz se a instancia de 
        # teste é da mesma classe que o neuronio gerado aleatoriamente
        if bmu[self.metric] is None:
            bmu[self.metric] = row[self.metric]
        elif bmu[self.metric] == row[self.metric]:
            bmu[index] = bmu[index] + (rate * (float(row[index]) - float(bmu[index])))
        elif bmu[self.metric] != row[self.metric]:
            bmu[index] = bmu[index] - (rate * (float(row[index]) - float(bmu[index])))
            bmu[self.metric] = row[self.metric]

    def euclidean_distance(self, p, q):
        _sum = 0
        for index, item in enumerate(q):
            if index in self.skippable_indexes:
                continue
            _sum += (float(item) - float(p[index])) ** 2
        return math.sqrt(_sum)

if __name__ == '__main__':
    import csv
    files = [
        {'name': 'iris_result', 'skippable': [5, 0], 'attr_qtd': 6, 'classes_qtd': 3}
    ]
    for _file in files:
        with open('../../resources/spreadsheets/result/%s.csv' % _file.get('name'), 'rb') as csv_file:
            data_set = []
            data_set_size = 0
            lines = csv.reader(csv_file, delimiter=';')
            for line in lines:
                aux = []
                for attr in line:
                    aux.append(float(attr))
                data_set.append(aux)
                data_set_size += 1
            lvq = LVQ(data_set, _file.get('classes_qtd'), 1, _file.get('attr_qtd'), _file.get('skippable') or [], _file.get('metric') or -1)
            print(lvq.train())
