#!/usr/bin/python


class CSVObject:
    def __init__(self):
        self.headers = []
        self.data = []

    '''
    def set_headers(self, headers):
        self.headers

    '''

    def process_line(self, line):
        self.data.push(line)

    @classmethod
    def remove_null_columns(self, lines):
        null_qtty = {}  # por coluna
        line_qtty = 0
        for line in lines:
            for index, item in enumerate(line):
                if item is None:
                    if str(index) in null_qtty:
                        null_qtty[str(index)] += 1
                    else:
                        null_qtty[str(index)] = 0
            line_qtty += 1

        for index in null_qtty:
            # se a quantidades de itens nulos for maior
            # que 1/3 da quantidade de linhas, então
            # a coluna deve ser retirada.
            if null_qtty[index] >= line_qtty / 3:
                print(null_qtty[index])
                pass
