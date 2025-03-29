import numpy as np
import cv2
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Flatten
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

pathFile = "/home/nv/Escuela/Octavo/Sistemas Inteligentes/Codigos/openCV/"

# Función para cargar y procesar las imágenes y etiquetas de clase
def cargar_imagenes_y_etiquetas(ruta,rango1,rango2):
    # Cargamos las imágenes
    imagenes = []
    etiquetas = []
    nombreClase=["hexagon","triangle","straightCross"]
   
    for clase in range(0, 3):
        for i in range(rango1, rango2):
           # print(ruta + nombreClase[clase] + '/' + nombreClase[clase]+'_'+str(i) + '.jpg')
            imagen = cv2.imread(ruta + nombreClase[clase] + '/' + nombreClase[clase]+'_'+str(i) + '.jpg')
            imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)  # Convertimos a escala de grises
            borde = cv2.Canny(imagen,100,200)    # Extraemos el borde
            imagen = borde.astype('float32') / 255.0 # Normalizamos los píxeles
            imagenes.append(imagen)
            etiquetas.append(clase)
   
    # Convertimos las listas de imágenes y etiquetas a arrays numpy
    imagenes = np.array(imagenes)
    etiquetas = np.array(etiquetas)  
   
       
    # Devolvemos las imágenes y etiquetas
    return imagenes, etiquetas


# Cargamos las imágenes y etiquetas de clase
ruta1 = '/home/nv/Escuela/Octavo/Sistemas Inteligentes/Codigos/openCV/Figuras/train'
imagenesTrain, etiquetasTrain = cargar_imagenes_y_etiquetas(ruta1, 41,200)
ruta2 = '/home/nv/Escuela/Octavo/Sistemas Inteligentes/Codigos/openCV/Figuras/test'
imagenesTest, etiquetasTest = cargar_imagenes_y_etiquetas(ruta2, 1,40)

# Definimos la arquitectura de la red neuronal
modelo=Sequential()
modelo.add(Flatten(input_shape=(64,64,1)))
modelo.add(Dense(128,activation='relu'))
# modelo.add(Dropout(0.5))
modelo.add(Dense(3,activation="softmax"))
# Compilamos el modelo
modelo.compile(loss='sparse_categorical_crossentropy',
              optimizer=Adam(learning_rate=0.001),
              metrics=['sparse_categorical_accuracy'])

# Entrenamos el modelo
historial=modelo.fit(imagenesTrain, etiquetasTrain,
           validation_data=(imagenesTest, etiquetasTest),
           epochs=50)

modelo.save("modelo_perceptronFigG")



# Graficar los errores de entrenamiento y validación
plt.plot(historial.history['loss'], label='Error de entrenamiento')
plt.plot(historial.history['val_loss'], label='Error de validación')
plt.xlabel('Épocas')
plt.ylabel('Pérdida (Loss)')
plt.title('Evolución del error en el entrenamiento')
plt.legend()
plt.show()