#!/usr/bin/python

import sys
import csv
from csvObject import CSVObject

def main(file_name, have_headers=False):
    csv_obj = CSVObject()
    with open('./../../resources/{}'.format(file_name)) as csv_file:
        lines = csv.reader(csv_file, delimiter=';')
        csv_obj.remove_null_columns(lines)

if __name__ == '__main__':
    if len(sys.argv):
        main('winequality-white.csv')
    else:
        print('Passe o nome do arquivo a ser processado.')