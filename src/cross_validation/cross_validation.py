#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
sys.path.append('../kNN')
from knn import KNN


class CrossValidation(object):
    """Técnica para avaliar a capacidade de generalização de um modelo."""
    def __init__(self, file_name, iter_count=0):
        """
        Args:
            file_name (str): Nome do arquivo gerado após o tratamento e
                processamento dos dados.
            iter_count (int): ...

        Atributos:
            data_set (list): Iniciação da lista que receberá toda a massa de
                dados a ser trabalhada.
            __set_data: Chamada de execução do método para leitura do arquivo.

        """

        self.data_set = []
        self.__set_data(file_name)
        self.iter_count = iter_count
        self.classes = None

    def __set_data(self, file_name):
        """Método de leitura e armazenamento do arquivo a ser processado

        Este método faz a leitura do arquivo e o armazena através de uma função
        anônima numa variável, para que possa ser processado sequencialmente
        pelos demais métodos.

        Args:
            file_name (str): Nome do arquivo a ser lido.

        Atributos:
            lines (_csv.reader): Contém toda os dados do arquivo passado
                separado por linhas.
            data_set (list): Armazena toda a massa de dados do
                determinado arquivo passado como parâmetro.

        """
        with open('./../../resources/spreadsheets/result/{}'.format(
                file_name)) as csv_file:
            lines = csv.reader(csv_file, delimiter=';')
            [(lambda x: self.data_set.append(x))(line) for line in lines]

    def k_fold(self, k):
        """Calcula a acurácia sobre os erros encontrados em k iterações.

        O método de validação cruzada denominado k-fold consiste em dividir o
        conjunto total de dados em k subconjuntos mutuamente exclusivos do
        mesmo tamanho e, a partir disto, um subconjunto é utilizado para teste
        e os k-1 restantes são utilizados para estimação dos parâmetros e
        calcula-se a acurácia do modelo.

        Atributos:
            fold (dict): Variável de chave-valor que armazena as k divisões do
                arquivo. Onde chave é o número da divisão, que vai de 1 à k, e
                o valor é uma matriz (i por j), o i são as linhas do arquivo e
                j é as colunas.
            line_qtty (int): Calcula a quantidade total de linhas no arquivo.
            hits (dict): Estrutura de dados chave-valor usado para calcular a
                quantidade de acertos em cada uma k rodadas.
            test_fold (list): Armazena o conjunto de dados, 1/k, usado para a
                rodada de teste da vez.
            trainning (list): ...

        Args:
            k (int): Quantidade de sublistas a ser dividido.

        No Longer Returned:
        """
        self.fold = {}
        line_qtty = sum(1 for row in self.data_set)
        # print(row_qtty) # colocando com parentesis pra mantes a compatibilidade com outras versoes do python
        aux = 1
        for index in range(0, line_qtty):
            if aux == k + 1:
                aux = 1
            if str(aux) not in self.fold:
                self.fold[str(aux)] = []
            self.fold[str(aux)].append(self.data_set[index])
            aux += 1

        aux = 0
        hits = {}
        test_fold = None
        for index in range(1, 11):
            test_fold = self.fold[str(index)]
            trainning = []
            file_lenght = 0
            self.classes = []
            for key, sublist in self.fold.iteritems():
                if int(key) == index:
                    continue
                else:
                    for line in sublist:
                        trainning.append(line)
                        file_lenght += 1
                        if line[-1] not in self.classes:
                            self.classes.append(line[-1])
            knn_obj = KNN(
                self.__get_neighbour_qtd(
                    self.iter_count, file_lenght), trainning)

            for jndex, test in enumerate(test_fold):
                knn_obj.find_knn(test)
                test_predict = knn_obj.get_prediction()
                if test_predict['class'] == float(test_fold[jndex][-1]):
                    if str(index) not in hits:
                        hits[str(index)] = 0
                    hits[str(index)] += 1
                aux += 1

            qtty_test = len(test_fold)
            qtty_correct = hits[str(index)]
            # Erro amostral = qnt de erros / pela qnt de instancias de teste
            erro_amostral = ((qtty_test - qtty_correct) / round(qtty_test, 5))
            # Porcentagem de erro por k-fold
            print (erro_amostral * 100)
            # print(test_fold)
            # print("---------------------------------------------------------------")
        print hits
    
    def __get_neighbour_qtd(self, iter_index, file_lenght):
        classes_qtd = len(self.classes)
        m = classes_qtd + 1 if classes_qtd % 2 == 0 else classes_qtd
        if iter_index == 0:
            return 1
        if iter_index == 1:
            return m + 2
        if iter_index == 2:
            return m * 10 + 1
        if iter_index == 3:
            if (file_lenght / 2) % 2 == 0:
                return (file_lenght / 2) + 1
            else:
                return (file_lenght / 2)

    def __get_confusion_matrix(self):
        pass

    def __get_multi_level_matrix(self):
        pass

    def generate_confusion_matrix(self):
        if len(self.classes) == 2:
            self.__get_confusion_matrix()
        else:
            self.__get_multi_level_matrix()


if __name__ == '__main__':
    # files = [
    #     'iris', 'abalone', 'wine',
    #     'adult', 'breast-cancer',
    #     'winequality-red', 'winequality-white'
    # ]
    files = ['wine']
    for _file in files:
        for i in range(4):
            cv = CrossValidation('%s_result.csv' % _file, i)
            cv.k_fold(10)
