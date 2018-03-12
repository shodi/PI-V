#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
sys.path.append('../kNN')
from knn import KNN


class CrossValidation(object):
    def __init__(self, file_name, iter_count=0):
        self.data_set = []
        self.__set_data(file_name)
        self.iter_count = iter_count

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
        print(row_qtty) # colocando com parentesis pra mantes a compatibilidade com outras versoes do python
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
        hits = {}
        test_fold = None
        for index in range(1, 11):
            test_fold = self.fold[str(index)]
            trainning = []
            file_lenght = 0
            classes = []
            for key, sublist in self.fold.iteritems():
                if int(key) == index:
                    continue
                else:
                    for line in sublist:
                        trainning.append(line)
                        file_lenght += 1
                        if line[-1] not in classes:
                            classes.append(line[-1]) 
            knn_obj = KNN(self.__get_neighbour_qtd(self.iter_count, file_lenght, len(classes)), trainning)

            for jndex, test in enumerate(test_fold):
                knn_obj.find_knn(test)
                test_predict = knn_obj.get_prediction()
                if test_predict['class'] == float(test_fold[jndex][-1]):
                    if str(index) not in hits:
                        hits[str(index)] = 0
                    hits[str(index)] += 1
                aux += 1
            qtty_test = len(test_fold)
            qtty_correct = hits[str(index)]
            # Erro amostral = qnt de erros / pela qnt de instancias de teste
            erro_amostral = ((qtty_test - qtty_correct)/round(qtty_test,5))
            # Porcentagem de erro por k-fold
            print (erro_amostral * 100)
            # print(test_fold)
            # print("---------------------------------------------------------------")
        print hits

    def __get_neighbour_qtd(self, iter_index, file_lenght, classes_qtd):
        m = classes_qtd + 1 if classes_qtd % 2 == 0 else classes_qtd
        if iter_index == 0:
            return 1
        if iter_index == 1:
            return m + 2
        if iter_index == 2:
            return m * 10 + 1
        if iter_index == 3:
            if (file_lenght / 2) % 2 == 0:
                return (file_lenght / 2) + 1
            else:
                return (file_lenght / 2)


if __name__ == '__main__':
    files = ['winequality-red_result.csv']
    for file_index, _file in enumerate(files):
        for i in range(4):
            cv = CrossValidation(_file, i)
            cv.k_fold(10)
