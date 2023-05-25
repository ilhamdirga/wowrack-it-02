import tensorflow.keras.backend as K
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
from sklearn.utils import shuffle
import tensorflow as tf

def buat_dataset_siamese(path_images, labels, image_path):   
    #membuat list label yang tunggal
    unique_labels = np.unique(labels)

    #mencari index dari gambar dari suatu label
    tempat_gambar = {}
    for label in unique_labels:
        tempat_gambar[label] = [i for i, curr_label in enumerate(labels) if curr_label == label]

    #memasangkan images positif dan negatif    
    pair_images = []
    pair_labels = []
    for i, image in enumerate(image_path):
        image = cv2.imread(os.path.join(path_images, image), cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (105,105), interpolation=cv2.INTER_AREA)
        image = image/255.
        neg_index = [j for j, label in enumerate(labels) if label != labels[i]]
        post_index = tempat_gambar.get(labels[i])
    
        post_image = image_path[np.random.choice(post_index)]
        post_image = cv2.imread(os.path.join(path_images, post_image), cv2.IMREAD_GRAYSCALE)
        post_image = cv2.resize(post_image, (105,105), interpolation=cv2.INTER_AREA)
        post_image = post_image/255.
        pair_images.append((image, post_image))
        pair_labels.append(1)
    
        neg_image = image_path[np.random.choice(neg_index)]
        neg_image = cv2.imread(os.path.join(path_images, neg_image), cv2.IMREAD_GRAYSCALE)
        neg_image = cv2.resize(neg_image, (105,105), interpolation=cv2.INTER_AREA)
        neg_image = neg_image/255.
        pair_images.append((image, neg_image))
        pair_labels.append(0)
    images_dataset = np.array(pair_images, dtype='float64')
    labels_dataset = np.array(pair_labels, dtype='float64')

    images_dataset = np.expand_dims(images_dataset, axis=-1)

    images_dataset, labels_dataset = shuffle(images_dataset, labels_dataset)
    return images_dataset, labels_dataset

def distance(vectors):
    (vectorA, vectorB) = vectors
    sumSquared = K.sum(K.square(vectorA - vectorB), axis=1, keepdims=True)
    return K.sqrt(K.maximum(sumSquared, K.epsilon()))

def plot(history, plot_path):
    plt.plot(H.history["loss"], label="train_loss")
    plt.plot(H.history["val_loss"], label="val_loss")
    plt.plot(H.history["accuracy"], label="train_acc")
    plt.plot(H.history["val_accuracy"], label="val_acc")
    plt.title('Hasil Train')
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig(plot_path)
    
def contrastive_loss(y, yhat, margin=1):
    y = tf.cast(y, yhat.dtype)
    squared_yhat = K.square(yhat)
    squared_margin = K.square(K.maximum(margin - yhat, 0))
    return K.mean((y * squared_yhat) + ((1 - y) * squared_margin))