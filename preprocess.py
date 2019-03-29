from librosa.core import load
from librosa.feature import melspectrogram
from os.path import isdir, join
import os
import subprocess


label_list = ['cel', 'cla', 'flu', 'gac', 'gel', 'org', 'pia', 'sax', 'tru', 'vio', 'voi']
config = {
  'train_dir': 'IRMAS-TrainingData'
}

if not isdir(config['train_dir']):
  subprocess.call(["sh", "download_nn_data,sh"])

train_dir = config['train_dir']

train_data = []
train_labels = []

for idx, label in enumerate(label_list):
  data_dir = join(train_dir, label)
  all_files = os.listdir()
  # you live with your mother ayy
  for f in all_files:
    f_path = join(data_dir, f)
    raw, _ = load(f_path)
    mel = #TODO: fix shape stuff
