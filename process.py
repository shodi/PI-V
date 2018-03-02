#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess

class bcolors:
    SUCCESS = '\033[92m'
    ERROR = '\033[91m'
    END = '\033[0m'

if __name__=='__main__':
    from src.data_processing.processing import init_process
    print('{}Success: Fortran compiled successfully\n{}'.format(bcolors.SUCCESS, bcolors.END))
    files = [
        { 'name': 'iris.csv', 'headers': False }
        # { 'name': 'winequality-red.csv', 'headers': True },
        # { 'name': 'winequality-white.csv', 'headers': True },
    ]
    for i in files:
        init_process(i.get('name'), i.get('headers'))
else:
    print('Não deve ser utilizado como um módulo')