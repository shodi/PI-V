import csv
from LVQ import lvq
from cross_validation import CrossValidation

if __name__ == '__main__':
    suffix = '_result.csv'
    path = '../resources/spreadsheets/result/'
    files = ['iris', 'abalone', 'breast-cancer', 'wine', 'winequality-red', 'winequality-white', 'adult']
    for file in files:
        with open(path + file + suffix) as csv:
            print('abriu')