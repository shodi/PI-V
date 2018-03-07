#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import csv

class KNN:
    def __init__(self, k):
        # Quantidade de vizinhos mais próximos
        # a considerar
        self.k = k

    def find_knn(self, data_set, value, metric=-1):
        prediction = {'value': None}
        for neighbour_to_check in data_set:
            distance = self.__euclidean_distance(neighbour_to_check, value, metric)
            if prediction.get('value') is None or distance < prediction.get('value'):
                prediction['value'] = distance
                prediction['class'] = neighbour_to_check[metric]
        return prediction

    def __euclidean_distance(self, p, q, metric):
        # P e Q são instâncias de uma mesma classe
        sum = 0
        try:
            if len(p) != (len(q) + 1):
                print('len: {}, len: {}'.format(len(p), len(q)))
                raise ValueError('Inconsistência nos dados.')
            for index, item in enumerate(q):
                sum += (float(item) - float(p[index])) ** 2
            return math.sqrt(sum)
        except Exception as error:
            raise error

if __name__ == '__main__':
    knn_obj = KNN(3)
    file_path = './../../resources/spreadsheets/result/iris_result.csv'
    plauzinho = ['0.2','0.3','0.4','0.5','0.6']
    try:
        with open(file_path, 'rb') as csv_file:
            lines = csv.reader(csv_file, delimiter=";")
            print(knn_obj.find_knn(lines, plauzinho))
    except Exception as error:
        print(error)