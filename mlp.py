import numpy as np
import pandas
import subprocess

def f(net):
    return (1 / (1 + np.exp(-net)))


def df_dnet(f_net):
    return (f_net * (1 - f_net))


def architecture(input_length=2,
                 hidden_length=2,
                 output_length=1,
                 activation=f,
                 d_activation=df_dnet):

    model = dict()
    model['input_length'] = input_length
    model['hidden_length'] = hidden_length
    model['output_length'] = output_length

    model['hidden'] = np.random.uniform(
        low=-0.5,
        high=0.5,
        size=(hidden_length,
              input_length + 1))

    model['output'] = np.random.uniform(
        low=-0.5,
        high=0.5,
        size=(output_length,
              hidden_length + 1))

    model['f'] = activation
    model['df_dnet'] = d_activation

    return model

# XOR
# 0 0 0
# 0 1 1
# 1 0 1
# 1 1 0

# Xp = [0, 1]



def backpropagation(model,
                    dataset,
                    eta=0.5,
                    threshold=1e-4):

    squaredError = 2 * threshold
    counter = 0

    while(squaredError > threshold):
        squaredError = 0

        for row in dataset:
            Xp = row[:model['input_length']]
            Yp = row[-2]
            results = forward(model, Xp)
            Op = results['f_net_o_p']

            # Calculando erro
            error = Yp - Op

            squaredError = squaredError + sum(error**2)

            delta_o_p = error * model['df_dnet'](results['f_net_o_p'])

            w_o_k_j = np.squeeze(model['output'])[:model['hidden_length']]
            delta_h_p = model['df_dnet'](
                np.asarray(results['f_net_h_p']).reshape(-1)) * \
                delta_o_p[0] * w_o_k_j

            model['output'] = model['output'] + \
                eta * np.dot(delta_o_p[0], np.append(np.asarray(
                    results['f_net_h_p']).reshape(-1), 1))
            model['hidden'] = model['hidden'] + eta * np.transpose(
                np.asmatrix(delta_h_p)) * np.append(Xp, 1)

        squaredError = squaredError / len(dataset)

        print(squaredError)

        counter += 1

    ret = dict()
    ret['model'] = model
    ret['counter'] = counter

    return ret


def forward(hidden, output, Xp):
    # Hidden layer
    net_h_p = np.dot(
        np.asmatrix(hidden),
        np.append(np.asarray(Xp), 1))
    f_net_h_p = f(net_h_p)

    # Output layer
    net_o_p = np.dot(
        output,
        np.append(np.asarray(f_net_h_p), 1))
    f_net_o_p = f(net_o_p)

    result = dict()
    result['net_h_p'] = net_h_p
    result['net_o_p'] = net_o_p
    result['f_net_h_p'] = f_net_h_p
    result['f_net_o_p'] = f_net_o_p

    return result


if __name__ == '__main__':
    '''dataset = pandas.read_csv("__data.csv")
    dataset = dataset[['std', 'minfun', 'meanfun',
                       'skew', 'maxfreq', 'iq1', 'iq3',
                       'median', 'centroid', 'minfreq',
                       'meanfreq', 'peak',
                       'kurtosis', 'maxfun', 'label']]

    dataset = dataset.values
    model = architecture(input_length=14, output_length=1, hidden_length=15)
    trained = backpropagation(model=model, dataset=dataset)
    print(dataset[0, 0:15])
    print(forward(model=trained['model'], Xp=dataset[0, 0:14]))'''
    dataset = pandas.read_csv("__data.csv")
    dataset = dataset[['std', 'minfun', 'meanfun',
                       'skew', 'maxfreq', 'iq1', 'iq3',
                       'median', 'centroid', 'minfreq',
                       'duration', 'meanfreq', 'peak',
                       'kurtosis', 'maxfun', 'label']]

    dataset = dataset.values
    hidden = pandas.read_csv("hidden.csv")
    output = pandas.read_csv("output.csv")
    import pdb; pdb.set_trace()
    result = forward(hidden=hidden, output=output, Xp=dataset[0, 0:15])
    pass
