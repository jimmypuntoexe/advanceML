# -*- coding: utf-8 -*-
"""assignment3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IKiD11DmoSLMpmeVhPOrm8JMUvNfAI0l

**Setup**
"""

import numpy as np 
from tensorflow import keras
from tensorflow.keras import layers
from matplotlib import pyplot as plt
import seaborn as sns
import tensorflow as tf

"""**Data Preparation**"""

# Model/data parameters 
num_classes = 10 #digits 0-9
input_shape = (28,28,1)

# load the data and divide it into train/test split
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

x_train= x_train.astype("float32") / 255
x_test, x_test.astype("float32") / 255

# plot some samples
image_index  = 7777
print(y_train[image_index])
plt.imshow(x_train[image_index],cmap='gray')
plt.axis("off")
plt.show()

x_train.shape

#expand dimension of our data (28,28,1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)
print("x_train shape: ", x_train.shape)
print("x_train samples: ", x_train.shape[0])
print("x_test sample: ", x_test.shape[0])

plt.figure(figsize=(10,7))
g = sns.countplot(y_train, palette="icefire")
plt.title("Number of digit classes")

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
y_train.shape

model = keras.Sequential (
    [
      keras.Input(shape =  input_shape),
    
      layers.Conv2D(8, kernel_size=(3,3), activation='relu'),
      layers.Conv2D(8, kernel_size=(3,3), activation='relu'),
      layers.MaxPool2D(pool_size=(2,2)),
     
      layers.Conv2D(16, kernel_size=(3,3), activation='relu'),
      layers.Conv2D(16, kernel_size=(3,3), activation='relu'),
      layers.MaxPool2D(pool_size=(2,2)),
      
      layers.Flatten(),
      layers.Dropout(0.3),
      layers.Dense(num_classes, activation='softmax'),
    ]
)
model.summary()

"""Train the model"""

from keras.callbacks import EarlyStopping
early_stopping = [EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)]

batch_size = 128
epochs = 150  

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

network_history = model.fit(x_train, y_train, batch_size=batch_size, callbacks=early_stopping,  epochs = epochs, validation_split=0.2)

x_plot = list(range(1,len(network_history.history['val_accuracy']) + 1))


def plot_history(network_history):
    plt.figure()
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.plot(x_plot, network_history.history['loss'])
    plt.plot(x_plot, network_history.history['val_loss'])
    plt.legend(['Training', 'Validation'])

    plt.figure()
    # plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.plot(x_plot, network_history.history['accuracy'])
    plt.plot(x_plot, network_history.history['val_accuracy'])
    plt.legend(['Training', 'Validation'], loc='lower right')
    plt.show()

plot_history(network_history)

score = model.evaluate(x_train, y_train, verbose=0)
print ('Train loss', score[0])
print('Train accuracy', score[1])

predicted = np.round(model.predict(x_train))
from sklearn.metrics import classification_report
targets = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
print(classification_report(y_train,predicted,  target_names=targets))

"""Evaluation on testset"""

score = model.evaluate(x_test, y_test, verbose=0)
print ('Test loss', score[0])
print('Test accuracy', score[1])

predicted = np.round(model.predict(x_test))
from sklearn.metrics import classification_report
targets = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
print(classification_report(y_test,predicted,  target_names=targets))