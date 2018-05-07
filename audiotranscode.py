import subprocess
import re
import os

subprocess.call(['./ffmpeg_verify.sh'])

folder = subprocess.check_output(['ls', './audios']).split('\n')
new_name = []
for file in folder:
    new_name = re.sub('(.mpeg|.mp4|.ogg)$', '.wav', file)
    subprocess.call(
        'ffmpeg -i {0} -c:a pcm_f32le {1}'.format(file, new_name),
        shell=True,
        cwd='./audios')
    os.remove('./audios/{0}'.format(file))
