from keras.layers import Conv2D
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import GlobalMaxPooling2D
from keras.layers import LeakyReLU
from keras.layers import MaxPooling2D
from keras.models import Sequential

def conv_layer(n_filters):
  return Conv2D(n_filters, 3,  padding="same", activation=LeakyReLU(alpha=0.33))

def pool_layer():
  return MaxPooling2D(pool_size=(3,3), stride=1)


model = Sequential()
model.add(conv_layer(32))
model.add(conv_layer(32))
model.add(pool_layer())
model.add(Dropout(0.25)
model.add(conv_layer(64))
model.add(conv_layer(64))
model.add(pool_layer())
model.add(Dropout(0.25)
model.add(conv_layer(128))
model.add(conv_layer(128))
model.add(pool_layer())
model.add(Dropout(0.25)
model.add(conv_layer(256))
model.add(conv_layer(256))
model.add(GlobalMaxPooling2D()) # this is where we should take embeddings
model.add(Flatten())
model.add(Dense(1024, activation=LeakyReLU(alpha=0.33))
model.add(Dropout(0.5))
model.add(Dense(11, activation='sigmoid'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy', 'kullback_leibler_divergence'])
