#!/usr/bin/python

import sys
import csv
from .csvObject import CSVObject

def init_process(file_name, headers=False):
    with open('./resources/spreadsheets/%s' %(file_name)) as csv_file:
        lines = csv.reader(csv_file, delimiter=';')
        csv_obj = CSVObject(headers) 
        csv_obj.set_data(lines)
        csv_obj.remove_null_columns()

if __name__ == '__main__':
    if len(sys.argv):
        init_process('winequality-white.csv')
    else:
        print('Passe o nome do arquivo a ser processado.')
