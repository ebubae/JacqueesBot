from glob import glob
from os import listdir, makedirs, getcwd
from os.path import exists, join
from json import dump
from random import randint, random, choice

def random_ees():
  final_ee = ""
  for _ in range(randint(3, 50)):
    final_ee += "e" if random() < 0.5 else "E"
  return final_ee

def set_inspiration():
  '''
  Returns a valid  user-generated inspiration song filepath
  '''
  inspiration = input("First things first. What song do you want to Jacqu{}s? ".format(random_ees()))
  song_added = False

  while not exists(inspiration) and inspiration.endswith('.wav'):
    print('\'{}\' is not a valid file path. Try again pl{}ase!'.format(inspiration, random_ees()))
    inspiration = input("What song do you want to Jacqu{}s? ".format(random_ees()))

  return inspiration

def set_samples():
  samples = []
  files_dir = 'samples/nsynth-valid/audio/'
  all_files = listdir(files_dir)
  instruments = {'elec_bass': "bass_electronic", 'syn_bass': 'bass_synthetic',
                 'brass': 'brass_acoustic', 'flute': 'flute_acoustic', 'syn_flute': 'flute_synthetic',
                 'ac_guitar': 'guitar_acoustic', 'ele_guitar': 'guitar_electronic',
                 'ac_keyboard': 'keyboard_acoustic', 'ele_keyboard': 'keyboard_electronic', 'syn_keyboard': 'keyboard_synthetic',
                 'mallet': 'mallet_acoustic', 'organ': 'organ_electronic', 'reed': 'reed_acoustic',
                 'strings': 'string_acoustic', 'ac_vocal': 'vocal_acoustic', 'syn_vocal': 'vocal_synthetic'}
  done_adding = False
  while not done_adding:
    print("all the instruments are:\n" + "\t".join(instruments.keys()))
    inst = input("\n Add an instrument, insert a file path, or type \'done\' to exit: ")
    if inst.lower() == 'done':
      done_adding = True
      break
    if exists(inst):
      s_path = inst
      inst_name = input('instrument name: ')
      pitch = input('pitch: ')
      data = {"instrument": inst_name, "pitch": pitch, "path": s_path}
      samples.add(data)
    elif inst not in instruments:
      print('\'{}\' is not an instrument. try again pl{}ase'.format(inst, random_ees()))
    else:
      for p in range(0, 128):
        possible_samples = glob('{}{}*-{:03}-*.wav'.format(files_dir, instruments[inst], p))
        if possible_samples:
          s = choice(possible_samples)
          data = {"instrument": instruments[inst], "pitch": p, "path": getcwd() + '/' + s}
          samples.append(data)
      print("samples added")
      instruments.pop(inst)
      
  return samples

def name_experiment():
  print("\noh yeah you have to name the experiment too")
  exp_name = input("what are you calling it? ")
  return exp_name

def set_tracks():
  tracks_set = False
  while not tracks_set:
    track_str = input("how many concurrent tracks? ")
    if track_str.isdigit():
      return int(track_str)

  return int(tracks_str)

def set_hyperparameters():
  print("epsilon represents the smallest distance between insert times (in seconds)")
  eps_set = False
  while not eps_set:
    e_str = input("eps = ")
    try:
      eps = float(e_str)
      eps_set = True
    except ValueError:
      print("{} is not a number. Try again pl{}ase".format(e_str, random_ees()))

  print("delta represents the max distance you can add after the input song (in seconds)")
  delta_set = False
  while not delta_set:
    d_str = input("delta = ")
    try:
      delta = float(d_str)
      delta_set = True
    except ValueError:
      print("{} is not a number. Try again pl{}ase".format(d_str, random_ees()))

  return eps, delta

def setup():
  print("Welcome to JacqueesBot. {}!".format(random_ees()))

  inspiration = set_inspiration()
  samples = set_samples()
  exp_name = name_experiment()
  eps, delta = set_hyperparameters()
  num_tracks = set_tracks()
  exp_dir = join('experiments', exp_name)
  makedirs(exp_dir)
  dump({"export_path": join(getcwd(), exp_dir), "project_name": exp_name, "num_tracks": num_tracks, "samples": samples, "inspiration": inspiration, "eps": eps, "delta": delta}, open(join(exp_dir, "config.json"), 'w'))

  return exp_dir

