import cv2

imagen = cv2.imread("images/web/Dia24.png")
#print (imagen[100][100][0])

cv2.imshow("Primera Imagen", imagen)
#cv2.waitKey(0)
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # 27 es el código ASCII de la tecla Esc
        break
cv2.destroyAllWindows