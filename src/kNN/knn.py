#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import csv

class KNN:
    def __init__(self, k):
        # Quantidade de vizinhos mais próximos
        # a considerar
        self.k = k

    def find_knn(self, neighbour_to_check, value):
        a = self.__euclidean_distance(neighbour_to_check, value)
        print(a)
        return

    def __euclidean_distance(self, p, q):
        # P e Q são instâncias de uma mesma classe
        sum = 0
        try:
            if len(p) != len(q):
                print('len: {}, len: {}'.format(len(p), len(q)))
                raise ValueError('Inconsistência nos dados.')
            for index, item in enumerate(p):
                sum += (float(item) - float(q[index])) ** 2 
            return math.sqrt(sum)
        except Exception as error:
            raise error

if __name__ == '__main__':
    knn_obj = KNN(3)
    file_path = './../../resources/spreadsheets/result/abalone_result.csv'
    plauzinho = ['0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','0.01','0.0011']
    try:
        with open(file_path, 'rb') as csv_file:
            lines = csv.reader(csv_file, delimiter=";")
            for line in lines:
                knn_obj.find_knn(line, plauzinho)
    except Exception as error:
        print(error)