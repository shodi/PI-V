#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv


class CSVObject:
    def __init__(self, do_have_headers, file_name):
        self.data = []
        self.headers = []
        self.statistic = {}
        self.do_have_headers = do_have_headers
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
        with open('./resources/spreadsheets/{}'.format(
                file_name)) as csv_file:
            self.lines = csv.reader(csv_file, delimiter=';')
            [(lambda x: self.data.append(x))(line) for line in self.lines]

    def remove_null_columns(self):
        """Método para remover colunas nulas

        Se a quantidades de itens nulos for maior que 1/3 da
        quantidade de linhas, então a coluna deve ser retirada.

        Atributos:
            null_qtty(dict): Estrutura onde chave armazenadaé o número da
                coluna e o valor uma lista com o número das linhas que contém
                valores nulos.
            line_qtty(int): Quantidade total de linhas com valores.
            self.statistic(dict):

        Args:

        Returns:

        Todo:
        """
        null_qtty = {}  # por coluna
        line_qtty = 0
        for row_number, line in enumerate(self.data):
            if self.do_have_headers and row_number == 0:
                continue
            for index, item in enumerate(line):
                if item is None or item == '':
                    if str(index) in null_qtty:
                        null_qtty[str(index)].append(row_number)
                    else:
                        null_qtty[str(index)] = [row_number]
                    continue
                if 'sum_{}'.format(str(index)) in self.statistic:
                    self.statistic['sum_%s' % str(index)] += float(item)
                else:
                    self.statistic['sum_%s' % str(index)] = float(item)
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

    def calculate_statistics(self):
        """Método para calcular as estatisticas

        Todo: Com base nos dados obtidos pelo método
        remove_null_columns podemos calcular valores como a média, desvio
        padrão e a variância.

        Tal atividade deverá ser implementada no método na qual este
        comentário reside.
        """
        pass

    def remove_outliers(self):
        pre_data = {}
        self.data = [['A'], ['6', '7', '15', '36', '39', '40', '41', '42', '43', '47', '49']]
        for row_number, line in enumerate(self.data):
            if self.do_have_headers and row_number == 0:
                continue
            for index, item in enumerate(line):
                if str(index) in pre_data:
                        pre_data[str(index)].append(float(item))
                else:
                    pre_data[str(index)] = [float(item)]
                continue
        pos_data = {}
        for key in pre_data:
            import pdb; pdb.set_trace()
            pos_data[key] = {}
            pos_data[key]['average'] = sum(pre_data[key]) / len(pre_data[key])
            pos_data[key]['q1'] = pre_data[key][
                round(0.25 * (len(pre_data) + 1))]
                # q2 = (N[int(len(N) / 2)] + N[int(len(N) / 2 - 1)]) / 2
            # if len(N) % 2 == 0 else N[int(len(N) /2)]
            pos_data[key]['q3'] = pre_data[key][
                round(0.75 * (len(pre_data) + 1))]
            pos_data[key]['IQR'] = pos_data[key]['q3'] - pos_data[key]['q1']
            pos_data[key]['up_limit'] = pos_data[key]['average'] + \
                pos_data[key]['IQR'] * 1.5
            pos_data[key]['down_limit'] = pos_data[key]['average'] - \
                pos_data[key]['IQR'] * 1.5
        '''
        for key, value in self.all_values:
            if value <= down_limit or value >= up_limit:
                N.remove(value)'''

# TODO: Implementar método que retira registros que ainda
# possuem dados nulos de colunas que não foram retiradas no método
# remove_null_columns
