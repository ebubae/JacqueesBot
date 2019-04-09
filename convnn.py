from keras.layers import Conv2D
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import GlobalMaxPooling2D
from keras.layers import LeakyReLU
from keras.layers import MaxPooling2D
from keras.layers import ZeroPadding2D
from keras.models import Sequential

from preprocess import preprocess

def conv_layer(n_filters, **kwargs):
  return Conv2D(n_filters, (3,3),  padding="valid", **kwargs)

def pool_layer():
  return MaxPooling2D(pool_size=(3,3), strides=1)

train_data, train_labels, test_data, test_labels = preprocess()
print("labels = " + str(train_labels.shape))
print(train_data.shape)

model = Sequential()
model.add(ZeroPadding2D(1, input_shape=train_data.shape[1:]))
model.add(conv_layer(32))
model.add(LeakyReLU(alpha=0.33))
model.add(ZeroPadding2D(1))
model.add(conv_layer(32))
model.add(LeakyReLU(alpha=0.33))
model.add(pool_layer())
model.add(Dropout(0.25))
model.add(ZeroPadding2D(1))
model.add(conv_layer(64))
model.add(LeakyReLU(alpha=0.33))
model.add(ZeroPadding2D(1))
model.add(conv_layer(64))
model.add(LeakyReLU(alpha=0.33))
model.add(pool_layer())
model.add(Dropout(0.25))
model.add(ZeroPadding2D(1))
model.add(conv_layer(128))
model.add(LeakyReLU(alpha=0.33))
model.add(ZeroPadding2D(1))
model.add(conv_layer(128))
model.add(LeakyReLU(alpha=0.33))
model.add(pool_layer())
model.add(Dropout(0.25))
model.add(ZeroPadding2D(1))
model.add(conv_layer(256))
model.add(LeakyReLU(alpha=0.33))
model.add(ZeroPadding2D(1))
model.add(conv_layer(256))
model.add(LeakyReLU(alpha=0.33))
model.add(GlobalMaxPooling2D()) # this is where we should take embeddings
#for l in model.layers:
#  print(l.output_shape)
model.add(Dense(1024))
model.add(LeakyReLU(alpha=0.33))
model.add(Dropout(0.5))
model.add(Dense(11, activation='sigmoid'))


model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy', 'kullback_leibler_divergence'])

model.fit(train_data, train_labels, epochs=5, batch_size=32)
model.save("music_model.h5")
loss_metrics = model.evaluate(test_data, test_labels, batch_size=128)
