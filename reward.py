import keras.backend as K
import numpy as np

from librosa.core import get_duration
from librosa.core import load

from preprocess import process_loaded_audio

from keras.models import load_model
from keras.models import Model

from sys import argv

music_model = load_model('music_model.h5')
embed_model = Model(inputs=music_model.input, outputs=music_model.get_layer('embed').output)
K.set_learning_phase(0)

def partition_audio(aud_path, block_size=3):
  '''
  Partition preprocessed into (3 second by default) long blocks

  Return a generator of all ready to be processed audio blocks
  '''
  aud, _ = load(aud_path)
  duration = get_duration(aud)
  return (load(aud_path, offset=i, duration=block_size)[0] for i in xrange(int(duration) - block_size + 1))


def get_reward(i_path, o_path):
  input_blocks  = partition_audio(i_path)
  output_blocks = partition_audio(o_path)
  input_audio  = np.array([process_loaded_audio(a) for a in input_blocks])
  output_audio = np.array([process_loaded_audio(a) for a in output_blocks])
  i_embed = embed_model.predict(input_audio)
  o_embed = embed_model.predict(output_audio)
  print(i_embed.shape)
  print(o_embed.shape)
  # TODO: length correction to input and 
  return np.linalg.norm(i_embed - o_embed)

if __name__ == '__main__':
  i_path = argv[1]
  o_path = argv[2]
  print(get_reward(i_path, o_path))

