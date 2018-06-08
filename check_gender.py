import csv
import subprocess
import re

import numpy as np
import pandas

from listener import Listener


class CheckGender(object):
    def __init__(self, audio):
        self.audio_name = self.transcode_2_wav(audio)
        received_audio_data = self.get_audio_information(self.audio_name)
        self.calculate_foward(received_audio_data)

    def transcode_2_wav(self, old_audio):
        new_audio = re.sub('(.mpeg|.mp4|.ogg)$', '.wav', old_audio)

        try:
            # TODO: Mudar para diretorio apropriado
            subprocess.call(['rm', "./audios/{}".format(new_audio)])
        except Exception:
            pass

        subprocess.call(
            'ffmpeg -i {0} -ac 2 {1}'.format(old_audio, new_audio),
            shell=True,
            cwd='./audios')
        return new_audio
        # subprocess.call(['./ffmpeg_verify.sh'])

    def normalize(self, path, audio_data, received_data):
        obj = []
        min_and_max = []
        with open(path, 'rb') as csv_file:
            file = csv.reader(csv_file, delimiter=',', lineterminator='\n')
            for indx, row in enumerate(file):
                if not indx:
                    min_and_max = [None for i in range(len(row))]
                    obj.append(row)
                    continue
                for index, cell in enumerate(row):
                    if not min_and_max[index]:
                        min_and_max[index] = {'min': 0, 'max': 0}
                    value = float(cell)
                    if value < min_and_max[index]['min']:
                        min_and_max[index]['min'] = value
                    elif value > min_and_max[index]['max']:
                        min_and_max[index]['max'] = value
        normalize_data = []
        with open(received_data, 'rb') as csv_file:
            file = csv.reader(
                csv_file, delimiter=',', lineterminator='\n')
            for indx, row in enumerate(file):
                for idx, cell in enumerate(row):
                    difference = min_and_max[idx]['max'] - \
                        min_and_max[idx]['min']
                    normalize_data.append(
                        (float(cell) - min_and_max[idx]['min']) / difference)
        return normalize_data

    def get_audio_information(self, audio):
        # TODO: Mudar para diretorio apropriado
        directory = './audios/'
        audio_data = Listener("{}{}".format(directory, audio),
                              option="gender",
                              save_into="./received_audio_data.csv")
        return self.normalize(
            'dataset.csv', audio_data, 'received_audio_data.csv')

    def f(self, net):
        return (1 / (1 + np.exp(-net)))

    def forward(self, hidden, output, Xp):
        # Hidden layer
        net_h_p = np.dot(
            np.asmatrix(hidden),
            np.append(np.asarray(Xp), 1))
        f_net_h_p = self.f(net_h_p)

        # Output layer
        net_o_p = np.dot(
            output,
            np.append(np.asarray(f_net_h_p), 1))
        f_net_o_p = self.f(net_o_p)

        result = dict()
        result['net_h_p'] = net_h_p
        result['net_o_p'] = net_o_p
        result['f_net_h_p'] = f_net_h_p
        result['f_net_o_p'] = f_net_o_p

        return result

    def calculate_foward(self, received_audio_data):
        dataset = pandas.read_csv("__data.csv")
        dataset = dataset[['std', 'minfun', 'meanfun',
                           'skew', 'maxfreq', 'iq1', 'iq3',
                           'median', 'centroid', 'minfreq',
                           'meanfreq', 'peak',
                           'kurtosis', 'maxfun', 'label']]
        dataset = dataset.values
        hidden = pandas.read_csv("hidden.csv")
        output = pandas.read_csv("output.csv")
        self.result = self.forward(
            hidden=hidden, output=output, Xp=received_audio_data)
        print(self.result)


if __name__ == '__main__':
    # TODO: Change file name
    x = CheckGender('cm_1.ogg')
