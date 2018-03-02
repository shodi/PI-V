#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess

class bcolors:
    SUCCESS = '\033[92m'
    ERROR = '\033[91m'

if __name__=='__main__':
    from src.data_processing.processing import init_process
    if subprocess.call([
        "f2py", "-c", "-m", "fortran", 
        "./src/fortran_routines/average.f90", "--quiet"
    ]) == 0:
        print(bcolors.SUCCESS + 'Success: Fortran compiled successfully\n')
        files = [
            { 'name': 'teste.csv', 'headers': True }
            # { 'name': 'winequality-red.csv', 'headers': True },
            # { 'name': 'winequality-white.csv', 'headers': True },
        ]
        for i in files:
            init_process(i.get('name'), i.get('headers'))
    else:
        print(bcolors.ERROR + "Error: Failed to compile Fortran routines")
else:
    print('Não deve ser utilizado como um módulo')