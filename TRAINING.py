import tensorflow as tf
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import numpy as np
import cv2
from sklearn.utils import shuffle
import os

# Function to load images and preprocess them
def load_images(folder, prefix, count):
    images = []
    for i in range(count):
        image_path = os.path.join(folder, f'{prefix}_{i}.png')
        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Image not found at {image_path}")
            continue
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        images.append(gray_image.reshape(89, 100, 1))
    return images

# Load images for training
loadedImages = load_images('Dataset/SwingImages', 'swing', 1000)
loadedImages += load_images('Dataset/PalmImages', 'palm', 1000)
loadedImages += load_images('Dataset/FistImages', 'fist', 1000)
loadedImages += load_images('Dataset/FistImages', 'One_', 1000)

# Define output labels
outputVectors = [[1, 0, 0]] * 1000 + [[0, 1, 0]] * 1000 + [[0, 0, 1]] * 1000

# Load images for testing
testImages = load_images('Dataset/SwingTest', 'swing', 100)
testImages += load_images('Dataset/PalmTest', 'palm', 100)
testImages += load_images('Dataset/FistTest', 'fist', 100)
testImages += load_images('Dataset/FistTest', 'One_', 100)

# Define test labels
testLabels = [[1, 0, 0]] * 100 + [[0, 1, 0]] * 100 + [[0, 0, 1]] * 100

# Shuffle Training Data
loadedImages, outputVectors = shuffle(loadedImages, outputVectors, random_state=0)

# Define the CNN Model
convnet = input_data(shape=[None, 89, 100, 1], name='input')
convnet = conv_2d(convnet, 32, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)
convnet = conv_2d(convnet, 64, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 128, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 256, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 256, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 128, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = fully_connected(convnet, 1000, activation='relu')
convnet = dropout(convnet, 0.75)

convnet = fully_connected(convnet, 3, activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=0.001, loss='categorical_crossentropy', name='regression')

model = tflearn.DNN(convnet, tensorboard_verbose=0)

# Train model
model.fit(loadedImages, outputVectors, n_epoch=5,
          validation_set=(testImages, testLabels),
          snapshot_step=100, show_metric=True, run_id='convnet_coursera')

# Save the trained model
model.save("TrainedModel/model26.tfl")
print("Model training complete and saved as model26.tfl")
