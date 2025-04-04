import cv2
import numpy as np

imagen = cv2.imread("images/web/Dia24.png")
height, width=imagen.shape[:2]
imagenSepia = np.zeros((height, width, 3), np.uint8)  # Imagen de 3 canales (RGB)

print("El alto es: ",height)
print("El ancho es: ",width)

for i in range(width):
    for j in range(height):
        b=imagen.item(j,i,0) # Canal Azul ()
        g=imagen.item(j,i,1) # Canal Verde 
        r=imagen.item(j,i,2) # Canal Rojo     

        tr = 0.393*r + 0.769*g + 0.189*b
        tg = 0.349*r + 0.686*g + 0.168*b
        tb = 0.272*r + 0.534*g + 0.131*b

        if tr > 255:
            r =255 
        else:
            r = tr

        if tg > 255:
            g = 255
        else:
            g = tg

        if tb > 255:
            b = 255
        else:
            b = tb

        imagenSepia[j][i] = (b, g, r)
cv2.imshow("Primera Imagen", imagenSepia)

#cv2.waitKey(0)
#Para que cierre con ESC
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # 27 es el código ASCII de la tecla Esc
        break

cv2.destroyAllWindows