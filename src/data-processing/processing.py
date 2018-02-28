#!/usr/bin/python

import sys
import csv
from csvObject import CSVObject


def main(file_name, headers=True):
    with open('./../../resources/%s' %(file_name)) as csv_file:
        lines = csv.reader(csv_file, delimiter=';')
        csv_obj = CSVObject(headers) 
        csv_obj.set_data(lines)
        csv_obj.remove_null_columns()

if __name__ == '__main__':
    if len(sys.argv):
        main('winequality-white.csv')
    else:
        print('Passe o nome do arquivo a ser processado.')
