import subprocess
import re
import os

subprocess.call(['./ffmpeg_verify.sh'])

wav_directory = './audios/wav/'
original_directory = './audios/original/'

if not os.path.exists(wav_directory):
    os.makedirs(wav_directory)

if not os.path.exists(original_directory):
    os.makedirs(original_directory)

folder = subprocess.check_output(['ls', './audios']).split('\n')

new_file = []

for old_file in folder:
    new_file = re.sub('(.mpeg|.mp4|.ogg)$', '.wav', old_file)

    subprocess.call(
        'ffmpeg -i {0} -ac 2 {1}'.format(old_file, new_file),
        shell=True,
        cwd='./audios')

    if not old_file == 'original':
        os.rename('./audios/{0}'.format(new_file),
                  '{0}{1}'.format(wav_directory, new_file))
        os.rename('./audios/{0}'.format(old_file),
                  '{0}{1}'.format(original_directory, old_file))
