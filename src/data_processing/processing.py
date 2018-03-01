#!/usr/bin/python

import sys
from .csvObject import CSVObject


def init_process(file_name, headers=False):
    csv_obj = CSVObject(headers, file_name)
    csv_obj.remove_null_columns()
    csv_obj.remove_outliers()

if __name__ == '__main__':
    if len(sys.argv):
        init_process('winequality-white.csv')
    else:
        print('Passe o nome do arquivo a ser processado.')
