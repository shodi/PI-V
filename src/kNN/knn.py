#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import csv


class KNN:
    def __init__(self, k, data_set):
        # Quantidade de vizinhos mais próximos
        # a considerar
        self.k = k
        self.kNN = None
        self.instance_qtd = 0  # quantidade de linhas do arquivo
        self.data_set = data_set

    def __set_data(self, file_name):
        """Método de leitura e armazenamento do arquivo a ser processado

        Este método faz a leitura do arquivo para armazena-lo para que possa
        ser processado pelos demais métodos.

        Atributos:
            self.data_set(list):

        Args:
            file_name(str): Nome do arquivo a ser lido.

        Returns:

        Todo:
        """
        with open('./../../resources/spreadsheets/result/{}'.format(
                file_name)) as csv_file:
            lines = csv.reader(csv_file, delimiter=';')
            [(lambda x: self.data_set.append(x))(line) for line in lines]

    def __build_obj(self, distance, obj_class):
        return {'distance': distance, 'class': obj_class}

    def get_prediction(self):  # chave   valor
        class_occurrences = {}  # {classe: Array<distancias>}
        for prediction in self.kNN:
            if prediction['class'] not in class_occurrences:
                class_occurrences[prediction['class']] = {}
                class_occurrences[prediction['class']][
                    'distances'] = [prediction['distance']]
            else:
                obj = class_occurrences[prediction['class']]['distances']
                obj.append(prediction['distance'])
        predicted = {'class': None, 'min_distance': -1, 'occurrences': -1}
        for item in class_occurrences:
            current_item = class_occurrences[item]
            if len(current_item['distances']) > predicted['occurrences']:
                predicted['class'] = float(item)
                predicted['min_distance'] = min(current_item['distances'])
                predicted['occurrences'] = len(current_item['distances'])
            else:
                if len(current_item['distances']) == predicted['occurrences']:
                    current_min_distance = min(current_item['distances'])
                    if predicted['min_distance'] > current_min_distance:
                        predicted['class'] = float(item)
                        predicted['min_distance'] = current_min_distance
                        predicted['occurences'] = len(
                            current_item['distances'])
        return predicted

    def find_knn(self, value, metric=-1, skippable_indexes=[]):
        prediction = []
        for neighbour_to_check in self.data_set:
            distance = self.__euclidean_distance(neighbour_to_check,
                                                 value,
                                                 metric,
                                                 skippable_indexes)
            if len(prediction) < self.k:
                obj = self.__build_obj(distance, neighbour_to_check[metric])
                prediction.append(obj)
                continue
            for index in range(len(prediction)):
                if prediction[index]['distance'] > distance:
                    del prediction[index]
                    obj = self.__build_obj(distance,
                                           neighbour_to_check[metric])
                    prediction.append(obj)
        self.kNN = prediction
        return prediction

    def __euclidean_distance(self, p, q, metric, skippable_indexes):
        # P e Q são instâncias de uma mesma classe
        _sum = 0
        try:
            # if len(p) != (len(skippable_indexes) + 1):
            #     print('len: {}, len: {}'.format(len(p), len(q)))
            #     raise ValueError('Inconsistência nos dados.')
            for index, item in enumerate(q):
                if index in skippable_indexes or index == metric:
                    continue
                _sum += (float(item) - float(p[index])) ** 2
            return math.sqrt(_sum)
        except Exception as error:
            raise error
