#!/usr/bin/python
# -*- coding: utf-8 -*-

if __name__=='__main__':
    from src.data_processing.processing import init_process
    files = [
        { 'name': 'winequality-red.csv', 'headers': True },
        { 'name': 'winequality-white.csv', 'headers': True }
    ]
    for i in files:
        init_process(i.get('name'), i.get('headers'))
else:
    print('Não deve ser utilizado como um módulo')