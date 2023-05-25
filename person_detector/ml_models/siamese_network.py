import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Lambda, Input
from tensorflow.keras.models import Model

def buat_siamese(input_shape, embedding_dim=128):
    inp = Input(input_shape)
    
    #first convo
    c = Conv2D(4, (3,3), activation='relu', padding='same')(inp)
    m = MaxPooling2D(2,2)(c)
    
    #second convo
    c = Conv2D(8, (3,3), activation='relu')(m)
    m = MaxPooling2D(2,2)(c)
    
    #third convo
    c = Conv2D(16, (3,3), activation='relu')(m)
    m = MaxPooling2D(2,2)(c)
    
    #fourt convo
    c = Conv2D(64, (3,3), activation='relu')(m)
    m = MaxPooling2D(2,2)(c)
    
    #fifth convo
    c = Conv2D(64, (3,3), activation='relu')(m)
    m = MaxPooling2D(2,2)(c)
    
    #fc
    f = Flatten()(m)
    d = Dense(64, activation='relu')(f)
    output = Dense(embedding_dim)(f)
    return Model(inputs=inp , outputs=output)
