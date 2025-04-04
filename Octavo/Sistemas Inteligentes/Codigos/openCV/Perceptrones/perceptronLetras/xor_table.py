import numpy as np
from keras.models import Sequential
import tensorflow as tf

from keras.layers import Dense

#Cargamos las 4 combinaciones de las compuertas XOR
patrones = np.array([[0,0],[0,1],[1,0],[1,1]])

#Salidas de las compuertas XOR
salidas = np.array([[0],[1],[1],[0]])

#Creamos la red neuronal
model = Sequential()
model.add(Dense(16, input_dim=2, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

#Compilamos la red neuronal
model.compile(loss='mean_squared_error', 
              optimizer='adam', 
              metrics=['binary_accuracy'])

#Entrenamos la red neuronal
model.fit(patrones, salidas, epochs=200)

#Evaluamos el modelo
scores = model.evaluate(patrones, salidas)

print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
model.save('modelo_perceptron.h5')