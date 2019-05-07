import keras.backend as K
import numpy as np

from librosa.core import get_duration
from librosa.core import load
from librosa.feature import chroma_cqt

from preprocess import process_loaded_audio

from keras.models import load_model
from keras.models import Model

from sys import argv, maxsize

music_model = load_model('music_model.h5')
embed_model = Model(inputs=music_model.input, outputs=music_model.get_layer('embed').output)
K.set_learning_phase(0)

def partition_audio(aud, sr, eps, block_size=3):
  '''
  Partition preprocessed into (3 second by default) long blocks

  Return a generator of all ready to be processed audio blocks
  '''
  off = 0
  while len(aud[off:]) > block_size * sr:
    yield aud[off:off + block_size * sr]
    off += sr
  #return (aud[off: block_size * sr + off] for off in range(0, sr * round(len(aud)/sr), sr))
  #return (load(aud_path, offset=i, duration=block_size)[0] for i in xrange(int(duration) - block_size + 1))


def length_coeff(i_size, o_size, delta):
  return abs(-0.5 / i_size * o_size + 1) if o_size < i_size + delta else maxsize

def get_reward(i_path, o_path, eps, delta, alpha=0.5, beta=12.0):
  input_audio, sr = load(i_path)
  output_audio, _ = load(o_path)
  i_size = len(input_audio)
  o_size = len(output_audio)
  coeff = length_coeff(i_size, o_size, delta)
  
  input_blocks  = partition_audio(input_audio, sr, eps)
  output_blocks = partition_audio(output_audio, sr, eps)
  processed_input  = [process_loaded_audio(a) for a in input_blocks]
  processed_output = [process_loaded_audio(a) for a in output_blocks]
  clip_len = min(len(processed_input), len(processed_output))
  processed_input = np.array(processed_input[:clip_len])
  processed_output = np.array(processed_output[:clip_len])
  i_embed = embed_model.predict(processed_input)
  o_embed = embed_model.predict(processed_output)
  clip_len = min(len(input_audio), len(output_audio))
  i_chromo = chroma_cqt(input_audio[:clip_len], sr)
  o_chromo = chroma_cqt(output_audio[:clip_len], sr)
  timbre_reward = 0#alpha * np.linalg.norm(i_embed - o_embed)
  pitch_reward = beta * np.linalg.norm(i_chromo - o_chromo)
  print("timbre cost: {}".format(timbre_reward))
  print("pitch cost: {}".format(pitch_reward))
  return -(timbre_reward + pitch_reward) * coeff

if __name__ == '__main__':
  i_path = argv[1]
  o_path = argv[2]
  print(get_reward(i_path, o_path))

