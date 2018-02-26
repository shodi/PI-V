#!/usr/bin/python
# -*- coding: utf-8 -*-

class CSVObject:
    def __init__(self):
        self.headers = []
        self.data = []

    '''
    def set_headers(self, headers):
        self.headers

    '''

    def process_line(self, line):
        self.data.append(line)

    @classmethod
    def remove_null_columns(self, lines):
        null_qtty = {}  # por coluna
        line_qtty = 0
        for idx, line in enumerate(lines):
            for index, item in enumerate(line):
                # not utilizado pois na massa de dados utilizada
                # nao possuem valores nulos
                if item is not None: 
                    if str(index) in null_qtty:
                        null_qtty[str(index)].append(idx)
                    else:
                        null_qtty[str(index)] = [idx]
            line_qtty += 1

        print(null_qtty)
        for index in null_qtty:
            # se a quantidades de itens nulos for maior
            # que 1/3 da quantidade de linhas, então
            # a coluna deve ser retirada.
            if len(null_qtty[index]) >= line_qtty / 3:
                pass
