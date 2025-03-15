import numpy as np
from keras.models import Sequential
import tensorflow as tf

# modelo=tf.keras.models.load_model('perceptron_E_U.h5')
modelo=tf.keras.models.load_model('perceptron_E_U_I_F.h5')

# test = np.array([
#     [1,0,1,
#      1,0,1,
#      1,0,1,
#      1,0,1,
#      1,1,1],
#     [1,1,0,
#      1,0,0,
#      1,1,0,
#      1,0,0,
#      1,1,0],c
#     [1,1,0,
#      1,0,0,
#      1,1,0,
#      1,0,0,
#      1,1,0],
#     [1,1,1,
#      1,0,0,
#      1,1,1,
#      1,0,0,
#      1,0,0]
# ])

test = np.array([[1,0,1,
                      1,0,1,
                      1,0,1,
                      1,0,1,
                      1,1,1],
                     [1,1,0,
                      1,0,0,
                      1,1,0,
                      1,0,0,
                      1,1,0],
                     [0,1,0,
                      0,1,0,
                      0,1,0,
                      0,1,0,
                      0,1,0],
                     [1,1,1,
                      1,0,0,
                      1,1,1,
                      1,0,0,
                      1,0,0]])


prediccion = modelo.predict(test)
print(prediccion.round())
# Convertir las predicciones de probabilidades a clases
clases_predichas = np.argmax(prediccion, axis=1)

print("Clases predichas: ", clases_predichas)