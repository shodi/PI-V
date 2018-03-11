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
            self.data(list):
            self.lines():

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
            data_set(array): Dados a serem trabalhados.

        Returns:

        Todo:
        """
        self.data_set = [[0], [1], [24], [22], [16], [2], [12], [8], [21], [3], [11]]
        divided_data = {}
        row_count = sum(1 for row in self.data_set)
        partition = 0
        for index, line in enumerate(self.data_set):
            if index % (row_count / 10) == 0:
                partition += 1
                divided_data[str(partition)] = []
            divided_data[str(partition)].append(line)
        import pdb; pdb.set_trace()
            # pass
        #for row_number, line in enumerate(self.data):
        # 1)Dividir o conjunto de dados em 10 partes
        # 2)erro amostral é a media dos erros obtidos


if __name__ == '__main__':
    file_name = 'iris_result.csv'
    # try:
    cv = CrossValidation(file_name)
    cv.k_fold(10)
    # except Exception as error:
    #     print('DEU ERRO: {}'.format(error))
