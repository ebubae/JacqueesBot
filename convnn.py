import keras.backend as K

from keras.layers import Conv2D
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import GlobalMaxPooling2D
from keras.layers import LeakyReLU
from keras.layers import Activation
from keras.layers import MaxPooling2D
from keras.layers import ZeroPadding2D
from keras.models import Sequential
from keras.optimizers import Adam

from preprocess import preprocess

def conv_layer(n_filters, **kwargs):
  return Conv2D(n_filters, (3,3),  padding="same", activation='relu', data_format='channels_last', **kwargs)

def pool_layer():
  return MaxPooling2D(pool_size=(3,3))

train_data, train_labels, test_data, test_labels = preprocess()
print("labels = " + str(train_labels.shape))
print(train_data.shape)

K.set_learning_phase(1)
model = Sequential()
#model.add(ZeroPadding2D(1, input_shape=train_data.shape[1:]))
model.add(conv_layer(32, input_shape=train_data.shape[1:]))
#model.add(LeakyReLU(alpha=0.33))
#model.add(ZeroPadding2D(1))
model.add(conv_layer(32))
#model.add(LeakyReLU(alpha=0.33))
model.add(pool_layer())
model.add(Dropout(rate=0.25))
#model.add(ZeroPadding2D(1))
model.add(conv_layer(64))
#model.add(LeakyReLU(alpha=0.33))
#model.add(ZeroPadding2D(1))
model.add(conv_layer(64))
#model.add(LeakyReLU(alpha=0.33))
model.add(pool_layer())
model.add(Dropout(rate=0.25))
#model.add(ZeroPadding2D(1))
model.add(conv_layer(128))
#model.add(LeakyReLU(alpha=0.33))
#model.add(ZeroPadding2D(1))
model.add(conv_layer(128))
#model.add(LeakyReLU(alpha=0.33))
model.add(pool_layer())
model.add(Dropout(rate=0.25))
#model.add(ZeroPadding2D(1))
model.add(conv_layer(256))
#model.add(LeakyReLU(alpha=0.33))
#model.add(ZeroPadding2D(1))
model.add(conv_layer(256))
#model.add(LeakyReLU(alpha=0.33))
model.add(GlobalMaxPooling2D(name='embed')) # this is where we should take embeddings
#for l in model.layers:
#  print(l.output_shape)
model.add(Dense(1024, activation='relu'))
#model.add(LeakyReLU(alpha=0.33))
model.add(Dropout(rate=0.5))
model.add(Dense(11, activation='sigmoid'))

adam = Adam(lr=0.001)#, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy',])# 'kullback_leibler_divergence'])

model.fit(train_data, train_labels, epochs=60, batch_size=32, shuffle=True)
model.save("music_model.h5")
#loss_metrics = model.evaluate(test_data, test_labels, batch_size=128)
