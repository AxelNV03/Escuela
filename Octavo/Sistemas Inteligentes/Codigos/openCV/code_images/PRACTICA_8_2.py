import numpy as np
import cv2
import tensorflow as tf

modelo=tf.keras.models.load_model("modelo_perceptronFigG.h5")

imagen = cv2.imread("/home/nv/Figuras/entradas/t1.jpeg")
imagen = cv2.resize(imagen, (64, 64))
cv2.imshow("Imagen", imagen)
imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
borde = cv2.Canny(imagen,100,200)
imagen = imagen.astype('float32') / 255.0
imagen = imagen.reshape(1, 64, 64, 1)

x_test = tf.convert_to_tensor(np.array(imagen).reshape((1,64,64,1)), dtype=tf.float32)

prediccion = modelo.predict(x_test)
prediccion_int = np.argmax(prediccion)
print (prediccion, " ", prediccion_int)

# Linux
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # 27 es el código ASCII de la tecla Esc
        break

cv2.destroyAllWindows()