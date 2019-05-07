from librosa.core import load
from librosa.feature import melspectrogram
from multiprocessing import Pool
from os.path import isdir, join, exists
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import numpy as np
import os
import pickle
import subprocess


label_list = ['cel', 'cla', 'flu', 'gac', 'gel', 'org', 'pia', 'sax', 'tru', 'vio', 'voi']
config = {
  'train_dir': 'IRMAS-TrainingData'
}

if not isdir(config['train_dir']):
  subprocess.call(["sh", "download_nn_data.sh", "."])

train_dir = config['train_dir']


def process_audio(f_path):
  """Return preprocessed audio file (normalized mel spectrogram)"""
  raw, _ = load(f_path)
  return process_loaded_audio(raw)

def process_loaded_audio(raw, preshape=(52, 128, 1)):
  #print("raw is: {}".format(raw))
  raw[raw != 0] /= max(abs(raw.min()), raw.max())
  mel = melspectrogram(raw, n_mels=128, n_fft=1024).T
  mel = np.expand_dims(mel, axis=2) # add extra channel
  return np.log(mel)

def append_data(x):
  data, label = x
  all_data.append(data)
  all_labels.append(label)

def preprocess():
  #files_ready = exists('train_data.pkl') and exists('test_data.pkl') and exists('train_labels.pkl') and exists('test_labels.pkl')
  files_ready = exists('all_data.pkl') and exists('all_labels.pkl')

  if files_ready:
    print("pre-packaged preprocessing...")
    all_data   = pickle.load(open('all_data.pkl', 'r'))
    all_labels = pickle.load(open('all_labels.pkl', 'r'))
    train_data, test_data, train_labels, test_labels = train_test_split(all_data, all_labels)
    #train_data   = pickle.load(open('train_data.pkl', 'r'))
    #train_labels = pickle.load(open('train_labels.pkl', 'r'))
    #test_data    = pickle.load(open('test_data.pkl', 'r'))
    #test_labels  = pickle.load(open('test_labels.pkl', 'r'))
    return train_data, train_labels, test_data, test_labels

  #global all_data
  #global all_labels

  all_data= []
  all_labels= [] # yikes let this breathe

  #threads = []
  print("beginning preprocessing")
  for idx, label in enumerate(tqdm(label_list)):
    #pool = Pool(4)
    data_dir = join(train_dir, label)
    all_files = os.listdir(data_dir)
    # you live with your mother ayy
    for f in all_files:
      f_path = join(data_dir, f)
      proc = process_audio(f_path)
      all_data.append(proc)
      all_labels.append(idx)
      #r = pool.apply_async(process_audio, args=(f_path, idx), callback=append_data)
      #r.wait()
    #pool.close()
    #pool.join()
    print("processed " + label)
  all_data = np.array(all_data)
  # creating one-hot labels 
  all_labels = np.array(all_labels)
  print(all_labels)
  all_labels = np.eye(len(label_list))[all_labels]
  print("before split target shape = " + str(all_labels.shape))
  print("before split data shape = " + str(all_data.shape))
  print("completed preprocessing")
  return all_data, all_labels
