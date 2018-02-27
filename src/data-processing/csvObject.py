#!/usr/bin/python
# -*- coding: utf-8 -*-

class CSVObject:
    data = []
    def __init__(self):
        self.headers = []

    @classmethod
    def set_data(self, data_lines):
        [(lambda x: self.data.append(x))(line) for line in data_lines]

    @classmethod
    def remove_null_columns(self):
        null_qtty = {}  # por coluna
        line_qtty = 0
        for row_number, line in enumerate(self.data):
            for index, item in enumerate(line):
                if item is None: 
                    if str(index) in null_qtty:
                        null_qtty[str(index)].append(row_number)
                    else:
                        null_qtty[str(index)] = [row_number]
            line_qtty += 1
        sorted_arr = [int(index) for index in list(null_qtty)]
        for index in sorted(sorted_arr, reverse=True):
            # se a quantidades de itens nulos for maior
            # que 1/3 da quantidade de linhas, então
            # a coluna deve ser retirada.
            if len(null_qtty[str(index)]) >= line_qtty / 3:
                for line in self.data:
                    del line[index]

# TODO: Implementar método que retira registros que ainda 
# possuem dados nulos de colunas que não foram retiradas no método 
# remove_null_columns