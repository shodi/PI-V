#!/bin/bash

f2py -c -m fortran ./src/fortran_routines/average.f90 --fcompiler=gnu95 --compiler=unix --quiet
mv $(ls | grep fortran | grep .so) ./src/data_processing/fortran.so
python2.7 process.py
