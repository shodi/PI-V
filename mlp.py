from math import exp




class MLP(object):
    def __init__(self):
        pass

    def f(self, net):
        return (1 / 1 + exp(net))

    def df_dnet(self, f_net):
        return (f_net * (1 - fnet))

    def architecture(self):

        model = list()
        model