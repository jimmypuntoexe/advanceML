# -*- coding: utf-8 -*-
"""Assignment4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1opgnOYQnbb8ZyIoZqXnBc_0o8nKhiZMz
"""

import numpy as np
import keras
from keras.models import Model
from keras.datasets.cifar10 import load_data
from tensorflow.keras.applications.vgg16 import VGG16 
from tensorflow.keras.preprocessing import image 
from tensorflow.keras.applications.vgg16 import preprocess_input 
from keras.models import Sequential
from keras.layers import Flatten, MaxPool2D
from keras.utils import to_categorical
from sklearn.metrics import accuracy_score

(x_train, y_train), (x_test, y_test) = load_data()

train_index = np.where(y_train.ravel() >= 4)
test_index = np.where(y_test.ravel() >= 4)

x_train = x_train[train_index]
y_train = y_train[train_index]
x_test = x_test[test_index]
y_test = y_test[test_index]

x_train = preprocess_input(x_train)
x_test = preprocess_input(x_test)
img_shape = x_train[0].shape

print("train shape: ", x_train.shape)
print("test shape: ", x_test.shape)
print("train target shape: ", y_train.shape)
print("test target shape: ", y_test.shape)

"""## **Primo taglio: FC layers**"""

model = VGG16(weights='imagenet', input_shape=img_shape, include_top=False) 
model.summary()

output = model.get_layer('block5_pool').output
output = Flatten()(output)
new_model = Model(model.input, output)
new_model.summary()

"""**Mio dataset cifar10**"""

x_train_features = new_model.predict(x_train) 
x_test_features = new_model.predict(x_test)

print("train shape: ", x_train_features.shape)
print("test shape: ", x_test_features.shape)

np.save('x_train_taglio_fc.npy', x_train_features)
np.save('x_test_taglio_fc.npy', x_test_features)

np.save('y_train_taglio_fc.npy', to_categorical(y_train))
np.save('y_test_taglio_fc.npy', to_categorical(y_test))

"""## **Esperimenti**"""

from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
split = 0.8

x_features = np.load('x_train_taglio_fc.npy')
x_features_test = np.load('x_test_taglio_fc.npy')
y_features = np.load('y_train_taglio_fc.npy')
y_features_test = np.load('y_test_taglio_fc.npy')

splitat = int(len(x_features) * split)
x_features_train = x_features[:splitat]
y_features_train = y_features[:splitat]

x_features_val = x_features[splitat:]
y_features_val = y_features[splitat:]

print("train shape: ", x_features_train.shape)
print("test shape: ", x_features_test.shape)

print("train shape: ", x_features_train.shape)
print("test shape: ", x_features_test.shape)

y_features_test = np.argmax(y_features_test, axis=1)
y_features_val = np.argmax(y_features_val, axis=1)
y_features_train = np.argmax(y_features_train, axis=1)
y_features_train.shape

from sklearn.svm import LinearSVC, SVC

svm = LinearSVC(verbose=2, max_iter=1000, C=0.1)
svm.fit(x_features_train, y_features_train)

x_features_test.shape

x_features_train.shape

"""## Performance-train"""

predictions_train = svm.predict(x_features_train)

print(classification_report(y_features_train, predictions_train))

acc_train1= accuracy_score(y_features_train, predictions_train)
acc_train1

predictions_val = svm.predict(x_features_val)
print(classification_report(y_features_val, predictions_val))

acc_val1= accuracy_score(y_features_val, predictions_val)
acc_val1

"""## TEST"""

predictions_test = svm.predict(x_features_test)
print(classification_report(y_features_test, predictions_test))

acc_test1= accuracy_score(y_features_test, predictions_test)
acc_test1

"""### **Secondo Taglio** """

from tensorflow.keras.models import Model
base_model = VGG16(weights = 'imagenet', input_shape=img_shape, include_top=False )
model2 = Model(inputs = base_model.input, outputs = base_model.get_layer('block4_pool').output)
output = model2.get_layer('block4_pool').output
output = Flatten()(output)
model2 = Model(model2.input, output)
model2.summary()

block4_pool_train_features = model2.predict(x_train)
block4_pool_test_features = model2.predict(x_test)
print(block4_pool_train_features.shape)
print(block4_pool_test_features.shape)
print(block4_pool_train_features)
print(block4_pool_test_features)

np.save('x_train_taglio_block4pool.npy', block4_pool_train_features)
np.save('x_test_taglio_block4pool.npy', block4_pool_test_features)

np.save('y_train_taglio_block4pool.npy', to_categorical(y_train))
np.save('y_test_taglio_block4pool.npy', to_categorical(y_test))

from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
split = 0.8

x_features = np.load('x_train_taglio_block4pool.npy')
x_features_test = np.load('x_test_taglio_block4pool.npy')
y_features = np.load('y_train_taglio_block4pool.npy')
y_features_test = np.load('y_test_taglio_block4pool.npy')

splitat = int(len(x_features) * split)
x_features_train = x_features[:splitat]
y_features_train = y_features[:splitat]

x_features_val = x_features[splitat:]
y_features_val = y_features[splitat:]

print("train shape: ", x_features_train.shape)
print("test shape: ", x_features_test.shape)

print("train shape: ", x_features_train.shape)
print("test shape: ", x_features_test.shape)

y_features_test = np.argmax(y_features_test, axis=1)
y_features_val = np.argmax(y_features_val, axis=1)
y_features_train = np.argmax(y_features_train, axis=1)
y_features_train.shape

from sklearn.svm import LinearSVC, SVC

svm2 = LinearSVC(verbose=1, max_iter=1000, C= 0.1)
svm2.fit(x_features_train, y_features_train)

predictions_train2 = svm2.predict(x_features_train)
print(classification_report(y_features_train, predictions_train2))

acc_train2= accuracy_score(y_features_train, predictions_train2)
acc_train2

predictions_val2 = svm2.predict(x_features_val)
print(classification_report(y_features_val, predictions_val2))

acc_val2= accuracy_score(y_features_val, predictions_val2)
acc_val2

predictions_test2 = svm2.predict(x_features_test)
print(classification_report(y_features_test, predictions_test2))

acc_test2= accuracy_score(y_features_test, predictions_test2)
acc_test2

"""### **TERZO TAGLIO**"""

from tensorflow.keras.models import Model
base_model = VGG16(weights = 'imagenet', input_shape=img_shape, include_top=False )
model3 = Model(inputs = base_model.input, outputs = base_model.get_layer('block3_pool').output)
output = model3.get_layer('block3_pool').output
output = Flatten()(output)
model3 = Model(model3.input, output)
model3.summary()

block2_pool_train_features = model3.predict(x_train)
block2_pool_test_features = model3.predict(x_test)
print(block2_pool_train_features.shape)
print(block2_pool_test_features.shape)

np.save('x_train_taglio_block3pool.npy', block2_pool_train_features)
np.save('x_test_taglio_block3pool.npy', block2_pool_test_features)

np.save('y_train_taglio_block3pool.npy', to_categorical(y_train))
np.save('y_test_taglio_block3pool.npy', to_categorical(y_test))

from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
split = 0.8

x_features = np.load('x_train_taglio_block3pool.npy')
x_features_test = np.load('x_test_taglio_block3pool.npy')
y_features = np.load('y_train_taglio_block3pool.npy')
y_features_test = np.load('y_test_taglio_block3pool.npy')

splitat = int(len(x_features) * split)
x_features_train = x_features[:splitat]
y_features_train = y_features[:splitat]

x_features_val = x_features[splitat:]
y_features_val = y_features[splitat:]

y_features_test = np.argmax(y_features_test, axis=1)
y_features_val = np.argmax(y_features_val, axis=1)
y_features_train = np.argmax(y_features_train, axis=1)
y_features_train.shape

from sklearn.svm import LinearSVC, SVC

svm3 = LinearSVC(verbose=1, max_iter=1000, C=0.1)
svm3.fit(x_features_train, y_features_train)

predictions_train3 = svm3.predict(x_features_train)
print(classification_report(y_features_train, predictions_train3))

acc_train3= accuracy_score(y_features_train, predictions_train3)
acc_train3

predictions_val3 = svm3.predict(x_features_val)
print(classification_report(y_features_val, predictions_val3))

acc_val3= accuracy_score(y_features_val, predictions_val3)
acc_val3

predictions_test3 = svm3.predict(x_features_test)
print(classification_report(y_features_test, predictions_test3))

acc_test3= accuracy_score(y_features_test, predictions_test3)
acc_test3

import matplotlib.pyplot as plt
"""#Plot accuracy train"""

accuracy_train = [acc_train1,acc_train2,acc_train3]

x_plot = list(['block5_pool','block4_pool','block3_pool'])

plt.figure()
plt.xlabel('Layer')
plt.ylabel('Accuracy')
plt.plot(x_plot, accuracy_train)

plt.legend(['Linear svm'])

"""#Plot accuracy val"""

accuracy_val = [acc_val1,acc_val2,acc_val3]

x_plot = list(['block5_pool','block4_pool','block3_pool'])

plt.figure()
plt.xlabel('Layer')
plt.ylabel('Accuracy')
plt.plot(x_plot, accuracy_val)

plt.legend(['Linear svm'])

"""#Plot accuracy test"""

accuracy_test = [acc_test1,acc_test2,acc_test3]

x_plot = list(['block5_pool','block4_pool','block3_pool'])

plt.figure()
plt.xlabel('Layer')
plt.ylabel('Accuracy')
plt.plot(x_plot, accuracy_test)

plt.legend(['Linear svm'])