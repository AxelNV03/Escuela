import cv2

img = cv2.imread("/home/nv/Escuela/Octavo/Sistemas Inteligentes/Codigos/openCV/images/perry.png")
# cv2.imshow("imagen original", img)

# gray = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)

blur = cv2.blur(img,(4,4))
gaussian = cv2.GaussianBlur(img,(5,5),0)
median =  cv2.medianBlur(img, 21)


edges = cv2.Canny(blur, 200, 255)
edges1 = cv2.Canny(gaussian, 200, 255)
edges2 = cv2.Canny(median, 200, 255)


cv2.imshow("imagen con filtro1", blur)
cv2.imshow("imagen con filtro1", gaussian)
cv2.imshow("imagen con filtro1", median)

cv2.imshow("imagen con filtro1", edges)
cv2.imshow("imagen con filtro1", edges1)
cv2.imshow("imagen con filtro1", edges2)


# cv2.waitKey(0)

# Linux 
while True: 
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # 27 es el código ASCII de la tecla Esc
        break


cv2.destroyAllWindows()