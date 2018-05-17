#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import time

class bcolors:
    SUCCESS = '\033[92m'
    ERROR = '\033[91m'
    END = '\033[0m'

if __name__=='__main__':
    from src.data_processing.processing import init_process
    files = [
        { 'name': 'iris' },
       # { 'name': 'winequality-red', 'headers': True },
       # { 'name': 'winequality-white', 'headers': True },
       # { 'name': 'adult', 'null_notation': ['?', '', None] },
       # { 'name': 'breast-cancer' },
       # { 'name': 'wine' },
       # { 'name': 'abalone' }
    ]
    for i in files:
        start_time = time.time()
        init_process(i.get('name'), i.get('headers'), i.get('null_notation'))
        print(bcolors.SUCCESS + \
            '[Success] Arquivo %s_result.csv gerado em %s%lf segundos%s' \
            %(i.get('name'), bcolors.ERROR, time.time() - start_time, bcolors.END))
else:
    print('Não deve ser utilizado como um módulo')