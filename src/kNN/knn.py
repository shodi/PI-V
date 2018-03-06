#!/usr/bin/python
# -*- coding: utf-8 -*-
import math

class KNN:
    def __init__(self, k):
        # Quantidade de vizinhos mais próximos
        # a considerar
        self.k = k
    
    def find_knn(self):
        a = self.__euclidean_distance([1,2,3], [4,5,6])
        print(a)
        return

    def __euclidean_distance(self, p, q):
        # P e Q são instancias de uma mesma classe
        sum = 0
        if len(p) != len(q):
            print('Inconsistência nos dados.')
            return
        for index, item in enumerate(p):
            sum += (item - q[index]) ** 2 
        return math.sqrt(sum)

if __name__ == '__main__':
    teste = KNN(3).find_knn()