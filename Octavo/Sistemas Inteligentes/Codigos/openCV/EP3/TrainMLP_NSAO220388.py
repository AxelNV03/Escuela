import numpy as np
import cv2
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.optimizers import Adam
import matplotlib
matplotlib.use('Agg')  # Para un backend sin ventana, útil para guardar imágenes
import matplotlib.pyplot as plt
import os
import matplotlib.pyplot as plt


# Función para cargar y procesar las imágenes y etiquetas de clase
def cargar_imagenes_y_etiquetas(ruta,rango1,rango2):
    # Cargamos las imágenes
    imagenes = []
    etiquetas = []
    nombreClase=["ocho","manji","estrella"]
    
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
ruta1 = "/home/nv/Muestras/train/"
imagenesTrain, etiquetasTrain = cargar_imagenes_y_etiquetas(ruta1, 1,20)
ruta2 = "/home/nv/Muestras/test/"
imagenesTest, etiquetasTest = cargar_imagenes_y_etiquetas(ruta2, 21,30)

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
           epochs=100)

# Verificar si el archivo existe y borrarlo si es necesario
if os.path.exists('modelo_perceptronFiguras.h5'):
    os.remove('modelo_perceptronFiguras.h5')
# Guardamos el modelo
modelo.save("modelo_perceptronFiguras.h5")

# Verificar si los archivos existen y borrarlos si es necesario
if os.path.exists('../Graficas/grafica_error.png'):
    os.remove('../Graficas/grafica_error.png')
if os.path.exists('../Graficas/grafica_precision.png'):
    os.remove('../Graficas/grafica_precision.png')

# Graficar los errores de entrenamiento y validación
plt.plot(historial.history['loss'], label='Error de entrenamiento')
plt.plot(historial.history['val_loss'], label='Error de validación')
plt.xlabel('Épocas')
plt.ylabel('Pérdida (Loss)')
plt.title('Evolución del error en el entrenamiento')
plt.legend()
plt.show()
plt.savefig('../Graficas/grafica_error.png')  # Guarda la gráfica como un archivo PNG

# Graficar la precisión de entrenamiento y validación
plt.plot(historial.history['sparse_categorical_accuracy'], label='Precisión de entrenamiento')
plt.plot(historial.history['val_sparse_categorical_accuracy'], label='Precisión de validación')
plt.xlabel('Épocas')
plt.ylabel('Precisión')
plt.title('Evolución de la precisión en el entrenamiento')
plt.legend()
plt.savefig('../Graficas/grafica_precision.png')  # Guarda la gráfica en un archivo
plt.close()
