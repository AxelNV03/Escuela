import cv2
import numpy as np

imagen = cv2.imread("images/web/Dia24.png")


height, width=imagen.shape[:2]

#imagenGris=np.zeros(( height,width,1),np.uint8)
imagenRoja = np.zeros((height, width, 3), np.uint8)  # Imagen de 3 canales (RGB)

print("El alto es: ",height)
print("El ancho es: ",width)
#cv2.imshow("Primera Imagen", imagen)

for i in range(width):
    for j in range(height):
        b=imagen.item(j,i,0) # Canal Azul ()
        g=imagen.item(j,i,1) # Canal Verde 
        r=imagen.item(j,i,2) # Canal Rojo     
        
        imagenRoja[j, i] = [0, g, 0]  # Solo rojo, el resto es cero
        #imagenGris[j][i]=(int)(b+g+r)/3
        
#cv2.imshow("Primera Imagen", imagenGris)
cv2.imshow("Primera Imagen", imagenRoja)

#cv2.waitKey(0)
#Para que cierre con ESC
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # 27 es el código ASCII de la tecla Esc
        break
cv2.destroyAllWindows