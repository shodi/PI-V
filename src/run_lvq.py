import csv
from LVQ import lvq
from sklearn.model_selection import cross_validate
from sklearn import datasets, linear_model

if __name__ == '__main__':
    files = ['iris', 'abalone', 'adult', 'breast-cancer', 'wine', 'winequality-red', 'winequality-white']
    for file_name in files:
        with open('../resources/spreadsheets/result/%s_result.csv' % file_name) as csv_file:
            lines = csv.reader(csv_file, delimiter=';')
            lasso = linear_model.Lasso()
            data = []
            [(lambda x: data.append(x))(line) for line in lines]
            cv_result = cross_validate(lasso, data, y=data, cv=10)