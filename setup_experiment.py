from glob import glob
from os import listdir, makedirs
from os.path import join
from json import dump
from random import randint, random, choice

def random_ees():
  final_ee = ""
  for _ in range(randint(3, 50)):
    final_ee += "e" if random() < 0.5 else "E"
  return final_ee

def setup():
  print("Welcome to JacqueesBot. {}!".format(random_ees()))
  ("What song do you want to Jacquees? ")
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
    inst = raw_input("\n Add an instrument: (or type \'done\' to exit) ")
    if inst.lower() == 'done':
      done_adding = True
      break
    if inst not in instruments:
      print('\'{}\' is not an instrument. try again pl{}ase'.format(inst, random_ees()))
    else:
      for p in range(0, 128):
        possible_samples = glob('{}{}*-{:03}-*.wav'.format(files_dir, instruments[inst], p))
        if possible_samples:
          s = choice(possible_samples)
          data = {"instrument": instruments[inst], "pitch": p, "path": s}
          samples.append(data)
      print("samples added")
      instruments.pop(inst)

  print("\noh yeah you have to name the experiment too")
  exp_name = raw_input("what are you calling it? ")
  exp_dir = join('experiments', exp_name)
  makedirs(exp_dir)
  dump({"samples": samples}, open(join(exp_dir, "config.json"), 'w'))




