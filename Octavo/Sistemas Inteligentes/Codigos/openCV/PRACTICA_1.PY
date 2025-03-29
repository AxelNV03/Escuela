"""
pip install opencv-python
"""

import cv2

img = cv2.imread("/home/nv/Escuela/Octavo/Sistemas Inteligentes/Codigos/openCV/images/rosas.jpg")
# cv2.imshow("imagen original", img)
img=cv2.resize(img, (720,480))

gray = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
rgb = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

yuv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
yuv1 = cv2.cvtColor(rgb, cv2.COLOR_BGR2HLS)
yuv2 = cv2.cvtColor(rgb, cv2.COLOR_BGR2YUV)

cv2.imshow("imagen con filtro1", yuv)
cv2.imshow("imagen con filtro1", yuv1)
cv2.imshow("imagen con filtro1", yuv2)


# cv2.waitKey(0)
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # 27 es el código ASCII de la tecla Esc
        break


cv2.destroyAllWindows()