#!/usr/bin/python

import sys
import csv
from csvObject import CSVObject


def main(file_name, headers=False):
    with open('./../../resources/%s' %(file_name)) as csv_file:
        lines = csv.reader(csv_file, delimiter=';')
        CSVObject.set_data(lines)
        CSVObject.remove_null_columns()

if __name__ == '__main__':
    if len(sys.argv):
        main('winequality-white.csv')
    else:
        print('Passe o nome do arquivo a ser processado.')
