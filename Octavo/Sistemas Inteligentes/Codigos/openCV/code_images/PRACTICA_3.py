import cv2
import numpy as np
import imutils

rojoBajo1=np.array([80,100,20],np.uint8)
rojoAlto1=np.array([90,255,255],np.uint8)
rojoBajo2=np.array([90,100,20],np.uint8)
rojoAlto2=np.array([100,255,255],np.uint8)

#Leer la imagen
image = cv2.imread("/home/nv/Escuela/Octavo/Sistemas Inteligentes/Codigos/openCV/code_images/images/messi.png")
image=imutils.resize(image,width=640)

#image=cv2.resize(image,(640,480))
imageGray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
imageGray=cv2.cvtColor(imageGray,cv2.COLOR_GRAY2BGR)
imageHSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

#Detectamos el color Rojo
maskRojo1=cv2.inRange(imageHSV,rojoBajo1,rojoAlto1)
maskRojo2=cv2.inRange(imageHSV,rojoBajo2,rojoAlto2)
mask=cv2.add(maskRojo1,maskRojo2)
mask=cv2.medianBlur(mask,7)
redDetected=cv2.bitwise_and(image,image,mask=mask)

#Fondo en grises
invMask=cv2.bitwise_not(mask)
bgGray=cv2.bitwise_and(imageGray,imageGray,mask=invMask)

#Sumamos bgGray y redDetected
finalImage=cv2.add(bgGray,redDetected)

#Visualización
cv2.imshow('image',redDetected)
# cv2.imshow('imageGray',imageGray)
# cv2.imshow('Invertida',invMask)
# cv2.imshow('bgGray',bgGray)
# cv2.imshow('finalImage',finalImage)

cv2.waitKey(0)
cv2.destroyAllWindows()
