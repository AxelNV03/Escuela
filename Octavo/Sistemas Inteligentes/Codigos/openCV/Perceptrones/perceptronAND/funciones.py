#-------------------Funcion perceptron ----------------
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
#--------------------------------------------------
def inferencia(entrada, W, umbral):
    y=entrada[0]*W[0]+entrada[1]*W[1]+umbral
    return 1 if y > 0 else 0
#--------------------------------------------------------