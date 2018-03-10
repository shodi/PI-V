#!/usr/bin/python

import sys
from .csvObject import CSVObject


def init_process(file_name, headers, null_notation):
    if null_notation is None:
        null_notation = ['', None]
    if headers is None:
        headers = False
    csv_obj = CSVObject(headers, '%s.csv' % file_name)
    csv_obj.set_null_notation(null_notation)
    csv_obj.remove_null_columns()
    csv_obj.data_normalization()
    csv_obj.cross_validation()
    csv_obj.generate_result('%s_result.csv' % file_name)

if __name__ == '__main__':
    if len(sys.argv):
        init_process('winequality-white')
    else:
        print('Passe o nome do arquivo a ser processado.')
