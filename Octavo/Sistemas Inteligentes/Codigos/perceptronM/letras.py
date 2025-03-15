import numpy as np
from keras.models import Sequential
import tensorflow as tf

from keras.layers import Dense

# Patrones E y U and I
# patrones = np.array([[1,0,1,
#                     1,0,1,
#                     1,0,1,
#                     1,0,1,
#                     1,1,1],
#                     [1,1,0,
#                      1,0,0,
#                      1,1,0,
#                      1,0,0,
#                      1,1,0],
#                     [0,1,0,
#                      0,1,0,
#                      0,1,0,
#                      0,1,0,
#                      0,1,0]])


# Patrones E y U and I
# Convierte las listas en Numpy arrays
patrones = np.array([
    [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0]
])

salidas = np.array([0, 1, 2, 3])  # Convertir las salidas también a un Numpy array

#Creamos la red neuronal
model = Sequential()

#Dim es la cantidad de entradas (cantidad de numeros dentro del array)
model.add(Dense(16, input_dim=15, activation='relu'))
model.add(Dense(8, activation='relu'))
#model.add(Dense(1, activation='sigmoid'))

#Capas de salida
model.add(Dense(4, activation='softmax'))

#Compilamos la red neuronal
model.compile(loss='sparse_categorical_crossentropy', 
              optimizer='adam', 
              metrics=['sparse_categorical_accuracy'])

#Entrenamos la red neuronal
model.fit(patrones, salidas, epochs=500, batch_size=1)

#Evaluamos el modelo
scores = model.evaluate(patrones, salidas)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))


model.save('perceptron_E_U_I_F.h5')