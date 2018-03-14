#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
sys.path.append('../kNN')
from knn import KNN


class CrossValidation(object):
    """Técnica para avaliar a capacidade de generalização de um modelo."""
    def __init__(self, file_name, iter_count=0, metric=-1, skippable_indexes=[0]):
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
        self.metric_column = metric if metric is not None else -1
        self.skippable_indexes = skippable_indexes if skippable_indexes is not None else [0]

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
        erro_amostral = []
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
                        if line[self.metric_column] not in self.classes:
                            self.classes.append(line[self.metric_column])
            knn_obj = KNN(
                self.__get_neighbour_qtd(
                    self.iter_count, file_lenght), trainning)

            for jndex, test in enumerate(test_fold):
                knn_obj.find_knn(test, metric=self.metric_column, skippable_indexes=self.skippable_indexes)
                test_predict = knn_obj.get_prediction()
                if str(index) not in hits:
                    length = len(self.classes)
                    hits[str(index)] = [[0 for x in range(length)] for y in range(length)]
                else:
                    predicted_class = self.get_class_int_value(test_predict['class'])
                    real_class = self.get_class_int_value(float(test_fold[jndex][self.metric_column]))
                    hits[str(index)][real_class][predicted_class] += 1
                # if test_predict['class'] == float(test_fold[jndex][self.metric_column]):
                #     hits[str(index)] += 1
                aux += 1
            qtty_test = len(test_fold)
            qtty_correct = 0
            for i in range(len(self.classes)): # sempre a matriz vai ter self.classes x self.classes
                # os acertos sao sempre os valores onde os indices da matriz sao iguais
                qtty_correct += hits[str(index)][i][i]
            # Erro amostral = qnt de erros / pela qnt de instancias de teste
            erro_amostral.append((qtty_test - qtty_correct) / round(qtty_test, 5))
        print hits
        return erro_amostral # array de erro amostral por fold
    
    def __get_neighbour_qtd(self, iter_index, file_lenght):
        """Processa as informações do arquivo com as 4 formas de knn

        Este método utiliza as separações do 10-fold para classificar as classes
        das instâncias pertencentes a partição de teste.
        É feita uma classificação para cada forma do knn, cada forma possui sua regra:
        1) Considera apenas o primeiro vizinho mais próximo;
        2) Considera a quantidade de classes + 2 vizinhos mais próximos;
        3) Considera a quantidade de classes * 10 + 1 vizinhos mais próximos;
        4) Considera a quantidade de instâncias / 2 vizinhos mais próximos.

        Args:
            iter_index (int): Identifica qual forma de knn a ser aplicada (1-4).
            file_lenght (int): Quantidade de instâncias do arquivo a ser lido.

        Atributos:
            classes_qtd (int): Calcula a quantidade de classes total no arquivo.
            m(int): Calculo da quantidade de classes + 1 para uso nas formas de knn.

        """
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

    def get_class_int_value(self, number):
        """ Transforma o valor da classe normalizada em inteiro

        O método consiste em transformar o valor das classes em inteiro.
        É feito esse tratamento pois, no mometo em que estamos normalizando os dados para o intervalo de [0,1]
        os valores das classes tambem são normalizados e se essa classe possuir mais de 2 valores
        diferentes ela assumira um número não inteiro na normalização.
        
        Args:
            number (int): Valor da classe normalizada.

        Atributos:
            length (int): Quantidade de categorias da classe.

        """
        length = len(self.classes)
        return int(number * (length - 1) - 1)

    def generate_confusion_matrix(self):
        """ Gerando Matrizes de Confusão

        O método consiste em receber o arquivo e gerar a matriz de confusão respectiva ao mesmo.
        Vericamos se quantidade de categorias da clase é igual a 2, se sim a matriz gerada
        será a Matriz de confusão binária.
        Se a quantidade de categoria da classe for maior que 2, será gerada a Matriz de confusão multi-nível.

        """
        if len(self.classes) == 2:
            self.__get_confusion_matrix()
        else:
            self.__get_multi_level_matrix()


def cross_validation_error(arr):
    # cve = cross_validation_error
    """ Calculo erro de validação cruzada

    O método consiste em calcular o erro de validação cruzada de cada arquivo.
    Sendo ele a média da soma dos erros amostrais.

    Args:
        arr(Array<{[x: int]:float}>): array com cada indice represetando o número da execução do k-fold.
            O valor referente ao indice corresponde ao resultado do erro amostral.
    Atributos:
        _sum (int): Soma dos erros amostrais.
    """
    _sum = 0
    for error in arr:
        _sum += error
    return _sum / len(arr)

if __name__ == '__main__':
    # files = [
    #     'iris', 'abalone', 'wine',
    #     'adult', 'breast-cancer',
    #     'winequality-red', 'winequality-white'
    # ]
    files = [
        { 'name': 'wine', 'metric': 1 },
        { 'name': 'winequality-red', 'skip': []}
    ]
    for file_info in files:
        for i in range(4):
            cv = CrossValidation('%s_result.csv' % file_info.get('name'), i, file_info.get('metric'), file_info.get('skip'))
            errors = cv.k_fold(10)
            print('CVE: %.5lf' % cross_validation_error(errors))
            
    # print('Erro de validação cruzada: %.5lf' % cross_validation_error(amostral_errors))
