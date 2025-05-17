#Evaluación del modelo de red neuronal convolucional entrenado

import numpy as np
from tensorflow.keras.utils import load_img,img_to_array
from keras.models import load_model
import os.path

#Leer la imagen a evaluar

imagen = "/content/drive/MyDrive/ImagenesCNN_8A2024/validar/platanos/platano8.jpg"

#Recortar la imagen

altura,anchura = 50,50
#Leer el modelo entrenado y sus pesos
modelo = "/content/drive/MyDrive/ImagenesCNN_8A2024/modelo/cnn.h5"
pesos = "/content/drive/MyDrive/ImagenesCNN_8A2024/modelo/cnn_pesos.h5"

#Cargar el modelo entrenado
cnn = load_model(modelo)
cnn.load_weights(pesos)

#Transformar la imagen a clasificar
imagen_clasificar = load_img(imagen,target_size=(altura,anchura))
imagen_clasificar = img_to_array(imagen_clasificar)
imagen_clasificar = np.expand_dims(imagen_clasificar,axis =0)

#Evaluar la imagen
clase = cnn.predict(imagen_clasificar)
print(clase)
arg_max = np.argmax(clase)

if arg_max == 0:
  print("Manzana")
elif(arg_max==1):
  print("Platano")



