import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io
import cv2 as cv
from keras.models import load_model  # za vrsenje provjere i validacije modela
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPool2D
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import Dense
from keras.preprocessing.image import ImageDataGenerator
from skimage.transform import resize
from tflite_model_maker import image_classifier
from tflite_model_maker.image_classifier import DataLoader

'''
cnn = Sequential()
# Dodavanje prvog kovolucijskog sloja i pooling sloja
cnn.add(Conv2D(32, kernel_size=(3, 3), input_shape=(224, 224, 3), activation='relu'))
cnn.add(MaxPool2D(pool_size=(2, 2)))
cnn.add(Dropout(0.2))
# Dodavanje drugog kovolucijskog sloja i pooling sloja
cnn.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
cnn.add(MaxPool2D(pool_size=(2, 2)))
cnn.add(Dropout(0.2))
# Dodavanje treceg kovolucijskog sloja i pooling sloja
cnn.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
cnn.add(MaxPool2D(pool_size=(2, 2)))
cnn.add(Dropout(0.2))
# Dodavanje cetvrtog kovolucijskog sloja i pooling sloja
cnn.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
cnn.add(MaxPool2D(pool_size=(2, 2)))
cnn.add(Dropout(0.2))
# Dodavanje petog kovolucijskog sloja i pooling sloja
cnn.add(Conv2D(32, kernel_size=(3, 3), activation='relu'))
cnn.add(MaxPool2D(pool_size=(2, 2)))
cnn.add(Dropout(0.2))

# Flatten
cnn.add(Flatten())

# sredivanje inputa i outputa
cnn.add(Dense(units=256, activation='relu'))
cnn.add(Dense(units=256, activation='relu'))
cnn.add(Dense(units=256, activation='relu'))
cnn.add(Dense(units=196, activation='sigmoid'))

cnn.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Priprema podataka
train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1. / 255)

# ucitavanje train/test podataka iz foldera
train_data = train_datagen.flow_from_directory('car_data/car_data/train',
                                               target_size=(224, 224),
                                               batch_size=32,
                                               class_mode='categorical')
test_data = test_datagen.flow_from_directory('car_data/car_data/test',
                                             target_size=(224, 224),
                                             batch_size=32,
                                             class_mode='categorical')
# treniranje modela
history = cnn.fit(train_data,
                  steps_per_epoch=100,
                  epochs=30,
                  validation_data=test_data,
                  validation_steps=50)
cnn.save("cnn_model.h5", save_format="h5")
'''

train_data=DataLoader.from_folder('/content/car_data/train')
test_data=DataLoader.from_folder('/content/car_data/test')

# Customize the TensorFlow model.
model = image_classifier.create(train_data,)

# Evaluate the model.
loss, accuracy = model.evaluate(test_data)
#model.export(export_dir='.')

# testiranje istreniranog modela
model = model.model
slika = plt.imread("auto2.jpg")

width, height = 224, 224
slika_resized = resize(slika, (width, height))
plt.imshow(slika_resized)
plt.imsave("resizedTest.jpg", slika_resized)

# prvi nacin provjete tocnosti - primjeceno nepouzdanost podataka
try:
    vjerojatnosti = model.predict(np.array([slika_resized, ]))
    print(vjerojatnosti[0])

    max = 0
    index = 0
    for n, i in enumerate(vjerojatnosti[0]):
        if i > max:
            max = i
            index = n
    print(max)
    print(index)
except Exception as e:
    print("ERROR: ", e)

# drugi nacin provjere tocnosti
bgr_img = cv.imread("auto2.jpg")
bgr_img = cv.resize(bgr_img, (width, height), cv.INTER_CUBIC)
rgb_img = cv.cvtColor(bgr_img, cv.COLOR_BGR2RGB)
rgb_img = np.expand_dims(rgb_img, 0)
preds = model.predict(rgb_img)
prob = np.max(preds)
class_id = np.argmax(preds)

print(20 * "*")
cars_meta = scipy.io.loadmat('devkit/cars_meta')
class_names = cars_meta['class_names']  # shape=(1, 196)
class_names = np.transpose(class_names)
print("Vjerojatnost: ", prob)
print("Index: ", class_id)
print("Auto: ", class_names[class_id][0][0])
