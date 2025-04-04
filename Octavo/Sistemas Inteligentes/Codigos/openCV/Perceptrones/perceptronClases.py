import random
#-------------------Clase Perceptron-------------------
def perceptron(patrones, W, umbral):
    #Bandera de ajuste
    flag=1
    iteraciones=0
    #Iteracion de ajuste de pesos y umbral
    while flag==1:
        flag=0 #Reinicio de bandera de ajuste
        
        #Iteracion de patrones
        for i in range(len(patrones)):
            #Calculo de la salida (suma ponderada)
            # y = (x1*w1) + (entrada 2 * peso 2) + umbral
            y=(patrones[i][0]*W[0])+(patrones[i][1]*W[1])+umbral
            
            #funcion de activacion (escalon)
            y = 1 if y > 0 else 0

            #Salida obtenida != salida esperada
            if y!= patrones[i][2]:
                #Bandera de ajuste
                flag=1

                #w1=w1+(d-y)*x1
                W[0]=W[0]+((patrones[i][2]-y)*(patrones[i][0]))
                
                #w2=w2+(d-y)*x2
                W[1]=W[1]+((patrones[i][2]-y)*(patrones[i][1]))
                
                #umbral=umbral+(d-y)
                umbral=umbral+(patrones[i][2]-y)
        iteraciones+=1
    return iteraciones, umbral
#-------------------Funcion imferencia-------------------
def inferencia(entrada, W, umbral):
    y=entrada[0]*W[0]+entrada[1]*W[1]+umbral
    return 1 if y > 0 else 0
#-------------------Funcion -------------------

#Tabla de verdad
patrones=[
    [2,0,0],
    [3,1,1],
    [4,1,1],
    [1,0,0],
    [5,1,1],
    [6,1,1],
    [3,0,0],
    [4,0,0]
]

W=[]
W.append(random.randint(-5,5))
W.append(random.randint(-5,5))
umbral = random.randint(-5,5)
iter,umbral=perceptron(patrones, W, umbral)

#Aleatorizar pesos y umbral (w y 0)
entrada=[6,1]
salida = inferencia(entrada, W, umbral)


print("Pesos finales: ",W)
print("Umbral final: ",umbral)
print("iteraciones: ",iter)
print("Entrada: ",entrada)
print("Salida: ",salida)
print("\n")

# for i in patrones:
#     #Aleatorizar pesos y umbral (w y 0)
#     entrada=[i[0],i[1]]
#     salida = inferencia(entrada, W, umbral)


#     print("Pesos finales: ",W)
#     print("Umbral final: ",umbral)
#     print("iteraciones: ",iter)
#     print("Entrada: ",entrada)
#     print("Salida: ",salida)
#     print("\n")