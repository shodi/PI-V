#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv


class CrossValidation(object):
    def __init__(self, file_name):
        self.data_set = []
        self.set_data(file_name)

    def set_data(self, file_name):
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
        chunks = {}
        row_qtty = sum(1 for row in self.data_set)
        aux = 1
        for index in range(0, row_qtty):
            if aux == k + 1:
                aux = 1
            if str(aux) not in chunks:
                chunks[str(aux)] = []
            chunks[str(aux)].append(self.data_set[index])
            aux += 1
        # 1)Dividir o conjunto de dados em 10 partes
        # 2)erro amostral é a media dos erros obtidos


if __name__ == '__main__':
    file_name = 'iris_result.csv'
    # try:
    cv = CrossValidation(file_name)
    cv.k_fold(10)
    # except Exception as error:
    #     print('DEU ERRO: {}'.format(error))
