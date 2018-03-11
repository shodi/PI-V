#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
sys.path.append('../kNN')
from knn import KNN


class CrossValidation(object):
    def __init__(self, file_name):
        self.data_set = []
        self.__set_data(file_name)

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

    def k_fold(self, k):
        """
        Atributos:

        Args:
            k(int): Quantidade de sublistas a ser dividido.

        Returns:

        Todo:
        """
        # dividir o arquivo em pedaços
        self.fold = {}
        row_qtty = sum(1 for row in self.data_set)
        print row_qtty
        aux = 1
        for index in range(0, row_qtty):
            if aux == k + 1:
                aux = 1
            if str(aux) not in self.fold:
                self.fold[str(aux)] = []
            self.fold[str(aux)].append(self.data_set[index])
            aux += 1

        # comparar testes e trainamentos
        aux = 0
        test_number = {}
        test_fold = None
        for index in range(1, 11):
            test_fold = self.fold[str(index)]
            trainning = []
            for key, sublist in self.fold.iteritems():
                if key == 0:
                    continue
                else:
                    for line in sublist:
                        trainning.append(line)
            knn_obj = KNN(
                int(sys.argv[1]) if len(sys.argv) > 1 else 3, trainning)

            for jndex, test in enumerate(test_fold):
                knn_obj.find_knn(test)
                test_predict = knn_obj.get_prediction()
                if test_predict['class'] == float(test_fold[jndex][-1]):
                    if str(index) not in test_number:
                        test_number[str(index)] = 0

                    test_number[str(index)] += 1
                aux += 1
        print test_number


if __name__ == '__main__':
    file_name = 'winequality-white_result.csv'
    # try:
    cv = CrossValidation(file_name)
    cv.k_fold(10)
    # except Exception as error:
    #     print('DEU ERRO: {}'.format(error))
