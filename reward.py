import keras.backend as K
import numpy as np

from librosa.core import get_duration
from librosa.core import load
from librosa.feature import chroma_cqt

from preprocess import process_loaded_audio

from keras.models import load_model
from keras.models import Model

from sys import argv

music_model = load_model('music_model.h5')
embed_model = Model(inputs=music_model.input, outputs=music_model.get_layer('embed').output)
K.set_learning_phase(0)

def partition_audio(aud, sr, eps, block_size=3):
  '''
  Partition preprocessed into (3 second by default) long blocks

  Return a generator of all ready to be processed audio blocks
  '''
  return (aud[off: block_size * sr + off] for off in range(0, len(aud), sr))
  #return (load(aud_path, offset=i, duration=block_size)[0] for i in xrange(int(duration) - block_size + 1))


def get_reward(i_path, o_path, eps, delta, alpha=0.5, beta=12.0):
  input_audio, sr = load(i_path)
  output_audio, _ = load(o_path)
  input_blocks  = partition_audio(i_path, sr, eps)
  output_blocks = partition_audio(o_path, sr, eps)
  processed_input  = [process_loaded_audio(a) for a in input_blocks]
  processed_output = [process_loaded_audio(a) for a in output_blocks]
  clip_len = min(len(processed_input), len(processed_output))
  processed_input = np.array(input_audio[:clip_len])
  processed_output = np.array(output_audio[:clip_len])
  i_embed = embed_model.predict(processed_input)
  o_embed = embed_model.predict(processed_output)
  i_chromo = chroma_cqt(input_audio, sr)
  o_chromo = chroma_cqt(output_audio, sr)
  #print(i_embed.shape)
  #print(o_embed.shape)
  # TODO: length correction to input and 
  return alpha * np.linalg.norm(i_embed - o_embed) + beta * np.linalg.norm(i_chromo - o_chromo)

if __name__ == '__main__':
  i_path = argv[1]
  o_path = argv[2]
  print(get_reward(i_path, o_path))

