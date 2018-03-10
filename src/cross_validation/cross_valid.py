#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import csv

class CV:
    def cross_validation(self):
        #import pdb; pdb.set_trace()
        pre_data = {}
        for row_number, line in enumerate(self.data):
            for index, item in pre_data:
                qtty = len(index)
                part_qtty = qtty / 10
                print(qtty)
                print(part_qtty)
        # 1)Dividir o conjunto de dados em 10 partes
        # 2)erro amostral é a media dos erros obtidos