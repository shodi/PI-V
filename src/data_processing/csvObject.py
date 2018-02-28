#!/usr/bin/python
# -*- coding: utf-8 -*-


class CSVObject:
    def __init__(self, do_have_headers):
        self.data = []
        self.headers = []
        self.statistic = {}
        self.do_have_headers = do_have_headers

    def set_data(self, data_lines):
        [(lambda x: self.data.append(x))(line) for line in data_lines]

    def remove_null_columns(self):
        null_qtty = {}  # por coluna
        line_qtty = 0
        for row_number, line in enumerate(self.data):
            if self.do_have_headers and row_number == 0:
                continue
            for index, item in enumerate(line):
                if item is None:
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
            # se a quantidades de itens nulos for maior
            # que 1/3 da quantidade de linhas, então
            # a coluna deve ser retirada.
            if len(null_qtty[str(index)]) >= line_qtty / 3:
                for line in self.data:
                    del line[index]
                    del self.statistic['sum_%s' % str(index)]
        self.calculate_statistics()

    def calculate_statistics(self):
        # TODO: Com base nos dados obtidos pelo método remove_null_columns
        # podemos calcular valores como a média, desvio padrão e a variância.
        # Tal atividade deverá ser implementada no método na qual este comentário reside.
        pass

    def remove_outliers(self):
        N = [6, 7, 15, 36, 39, 40, 41, 42, 43, 47, 200]
        average = sum(N) / len(N)
        q1 = N[round(0.25 * (len(N) + 1))]
        # q2 = (N[int(len(N) / 2)] + N[int(len(N) / 2 - 1)]) / 2
        # if len(N) % 2 == 0 else N[int(len(N) /2)]
        q3 = N[round(0.75 * (len(N) + 1))]
        IQR = q3 - q1
        up_limit = average + IQR * 1.5
        down_limit = average - IQR * 1.5

        for value in N:
            if value <= down_limit or value >= up_limit:
                N.remove(value)

# TODO: Implementar método que retira registros que ainda 
# possuem dados nulos de colunas que não foram retiradas no método 
# remove_null_columns