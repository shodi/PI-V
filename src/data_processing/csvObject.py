#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import os
import math

class CSVObject:
    def __init__(self, do_have_headers, file_name):
        self.data = []
        self.statistic = {}
        self.do_have_headers = do_have_headers
        self.set_data(file_name)
        self.categorization = None

    def set_null_notation(self, null_notation):
        self.null_notation = null_notation

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
        with open('./resources/spreadsheets/{}'.format(
                file_name)) as csv_file:
            self.lines = csv.reader(csv_file, delimiter=';')
            [(lambda x: self.data.append(x))(line) for line in self.lines]

    def remove_null_columns(self):
        """Método para remover colunas nulas

        Se a quantidades de itens nulos for maior que 1/3 da
        quantidade de linhas, então a coluna deve ser retirada.

        Atributos:
            null_qtty(dict): Estrutura onde chave é armazenada o número da
                coluna e o valor uma lista com o número das linhas que contém
                valores nulos.
            line_qtty(int): Quantidade total de linhas com valores.
            categorization(array<dict>): cada indice representa uma coluna.
                Cada coluna terá a categorização de seus dados não numéricos.

        Args:

        Returns:

        Todo:
        """
        null_qtty = {}  # por coluna
        line_qtty = 0
        for row_number, line in enumerate(self.data):
            if row_number == 0:
                # inicializa array. A quantidade de elementos
                # indica a quantidade de colunas que essa tabela possui
                self.categorization = [None] * len(self.data[0])
                if self.do_have_headers:
                    continue
            for index, item in enumerate(line):
                if item.strip() in self.null_notation:
                    if str(index) in null_qtty:
                        null_qtty[str(index)].append(row_number)
                    else:
                        null_qtty[str(index)] = [row_number]
                    continue
                # Tenta transformar o dado em float, caso o dado não for
                # algo numérico, deverá ser categorizado
                if 'sum_{}'.format(str(index)) in self.statistic:
                    value = self._get_item_value(item, index)
                    self.statistic['sum_%s' % str(index)] += value
                else:
                    self.statistic['sum_%s' % str(index)] = self. \
                        _get_item_value(item, index)
            line_qtty += 1
        self.statistic['total_rows'] = line_qtty
        sorted_arr = [int(index) for index in list(null_qtty)]
        for index in sorted(sorted_arr, reverse=True):
            if len(null_qtty[str(index)]) >= line_qtty / 3:
                for line in self.data:
                    del line[index]
                    if 'sum_%s' % str(index) in self.statistic:
                        del self.statistic['sum_%s' % str(index)]
        for subarray in self.data:
            if '' in subarray:
                self.data.remove(subarray)
        # self.calculate_statistics()

    counter = 0

    def _get_item_value(self, item, idx):
        """
            Método para retornar o valor numerico ou caso não seja um número
            retornar categorizar um item não numérico

            Atributos:
                item(float || string): valor a ser analizado e
                    categorizado, caso necessário.
                categorization(Array<{[x: string]: int}>): array com cada
                    indice representando uma coluna da planilha
                idx(int): indice do arr_obj correspondente a coluna que está
                    sendo analizada.
        """
        try:
            return float(item)
        except Exception:
            if self.categorization[idx] is None:
                self.categorization[idx] = {}
            if item not in self.categorization[idx]:
                self.categorization[idx][item] = float(self.counter)
                self.counter += 1
            return self.categorization[idx][item]

    def data_normalization(self):
        max_and_min_by_row = {}
        for line_number, line in enumerate(self.data):
            for index, item in enumerate(line):
                self.data[line_number][index] = self._get_item_value(
                    item, index)
                if index not in max_and_min_by_row:
                    max_and_min_by_row[index] = [self.data[line_number][index],
                                                 self.data[line_number][index]]

                if max_and_min_by_row[index]:
                    if self.data[line_number][index] > \
                            max_and_min_by_row[index][0]:
                        max_and_min_by_row[index][0] = \
                            self.data[line_number][index]

                    elif self.data[line_number][index] < \
                            max_and_min_by_row[index][1]:
                        max_and_min_by_row[index][1] = \
                            self.data[line_number][index]
        for line_number, line in enumerate(self.data):
            for index, item in enumerate(line):
                self.data[line_number][index] = (
                    (item - max_and_min_by_row[index][1]) /
                    (max_and_min_by_row[index][0] -
                     max_and_min_by_row[index][1]))
        # (item - menor_item)/(maior_item - menor_item )

    def remove_outliers(self):
        pre_data = {}
        for row_number, line in enumerate(self.data):
            if self.do_have_headers and row_number == 0:
                continue
            for index, item in enumerate(line):
                if self.categorization[index] is not None:
                    continue
                str_idx = str(index)
                float_item = float(item)
                if str_idx in pre_data:
                    pre_data[str_idx].append(float_item)
                else:
                    pre_data[str_idx] = [float_item]
        pos_data = {}
        for key in pre_data:
            aux = sorted(pre_data[key][:])
            length = len(aux)
            pos_data[key] = {}
            # pos_data[key]['average'] = fortran.average(aux, length)
            pos_data[key]['average'] = sum(aux) / length
            k_q1 = (length - 1) / 4
            int_part_q1 = int(k_q1 - (k_q1 - int(k_q1)))
            float_part_q1 = k_q1 - int(k_q1)
            pos_data[key]['q1'] = aux[int_part_q1] + (
                float_part_q1 * (aux[int_part_q1] - aux[int_part_q1 + 1]))
            # q2 = (N[int(len(N) / 2)] + N[int(len(N) / 2 - 1)]) / 2
            # if len(N) % 2 == 0 else N[int(len(N) /2)]
            k_q3 = 3 * (length - 1) / 4
            int_part_q3 = int(k_q3 - (k_q3 - int(k_q3)))
            float_part_q3 = k_q3 - int(k_q3)
            pos_data[key]['q3'] = aux[int_part_q3] + (
                float_part_q3 * (aux[int_part_q3] - aux[int_part_q3 + 1]))
            pos_data[key]['IQR'] = pos_data[key]['q3'] - pos_data[key]['q1']
            pos_data[key]['up_limit'] = pos_data[key]['average'] + 1.5 * \
                pos_data[key]['IQR']
            pos_data[key]['down_limit'] = pos_data[key]['average'] - 1.5 * \
                pos_data[key]['IQR']
            for item in aux:
                if item < pos_data[key]['down_limit']:
                    aux.remove(item)
                if item > pos_data[key]['up_limit']:
                    aux.remove(item)
            print(aux)

    def generate_result(self,
                        result_file_name,
                        path="./resources/spreadsheets/result"):
        """
            Método para gerar o resultado do csv processado

            Atributos:
                result_file_name(string): Nome do arquivo que será armazenada a
                    informação processada.
                path(string): Caminho para o local onde será armazenado
                    tal arquivo.
        """
        file_path = '%s/%s' %(path, result_file_name) 
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, mode="w+") as result_csv:
            for item in self.data:
                line = ';'.join(map(str, item))
                result_csv.writelines('%s\n' % line)
        # coloca isso para testar direto no terminal
        # import pdb; pdb.set_trace()

            lculate Euclidean distance in PythonPython

    def euclidean_distance(p, q, length):
        distance = 0
        for x in range(length):
            distance += (p[x] - q[x]) * (p[x] - q[x])
            # distance += pow((p[x] - q[x]), 2)
        return(distance ** (1/2)
        # return math.sqrt(distance)

# TODO: Implementar método que retira registros que ainda
# possuem dados nulos de colunas que não foram retiradas no método
# remove_null_columns
# if __name__ != '__main__':
# import fortran
