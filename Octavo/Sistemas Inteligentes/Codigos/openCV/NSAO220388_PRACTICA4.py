import cv2

imagen = cv2.imread("images/web/Dia24.png")

cv2.imshow("Primera Imagen", imagen)
gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,100,200)

cv2.imshow("Imagen con bordes", edges)

#cv2.waitKey(0)
#Para que cierre con ESC
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # 27 es el código ASCII de la tecla Esc
        break
cv2.destroyAllWindows