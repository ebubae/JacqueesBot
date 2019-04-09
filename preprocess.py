from librosa.core import load
from librosa.feature import melspectrogram
from os.path import isdir, join
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import numpy as np
import os
import subprocess


label_list = ['cel', 'cla', 'flu', 'gac', 'gel', 'org', 'pia', 'sax', 'tru', 'vio', 'voi']
config = {
  'train_dir': 'IRMAS-TrainingData'
}

if not isdir(config['train_dir']):
  subprocess.call(["sh", "download_nn_data.sh", "."])

train_dir = config['train_dir']


def preprocess():
  print("beginning preprocessing")
  all_data = []
  all_labels = []
  
  for idx, label in enumerate(label_list):
    data_dir = join(train_dir, label)
    all_files = os.listdir(data_dir)
    # you live with your mother ayy
    for f in tqdm(all_files):
      f_path = join(data_dir, f)
      raw, _ = load(f_path)
      raw /= max(abs(raw.min()), raw.max())
      mel = melspectrogram(raw, n_mels=128, n_fft=1024).T
      mel = np.expand_dims(mel, axis=2)
      all_data.append(np.log(mel))
      all_labels.append(idx)
  all_data = np.array(all_data)
  #all_data = np.expand_dims(all_data, axis=0)
  # creating one-hot labels 
  all_labels = np.array(all_labels)
  all_labels = np.eye(len(label_list))[all_labels]
  print("before split target shape = " + str(all_labels.shape))
  train_data, test_data, train_labels, test_labels = train_test_split(all_data, all_labels, test_size=0.2, shuffle=True)
  print("completed preprocessing")
  return train_data, train_labels, test_data, test_labels
