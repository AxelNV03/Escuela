from random import randint
from random import random

cadena = format(16,f'0{5}b')
print(cadena)

def generarPoblacion(cantInd):
    poblacion = []
    for i in range(cantInd):
        individuo = format(randint(0,31),f'0{5}b')
        poblacion.append(individuo)
    return poblacion

def evaluarPoblacion(poblacion):
    fitness=[]
    #DECODIFICAR Y APLICAR FUNCION OBJETIVO fx=x^2
    for individuo in poblacion:
        x = int(individuo,2)
        fitness.append(x**2)
    return fitness
    
def Seleccionar(poblacion,fitness):
    nuevaPob=[]
    #Seleccionar al mejor por elitismo
    nuevaPob.append(poblacion[fitness.index(max(fitness))])

    #Seleccionar al los demas individuos
    for i in range(3):
        #Seleccionar al azar
        ind1 = randint(0,3) #NUMERO DE INDICE
        ind2 = randint(0,3) #NUMERO DE INDICE
        while(ind1==ind2):
            ind2 = randint(0,3)
        #aplicar torneo determinista
        if(fitness[ind1]>fitness[ind2]): #FITNESS CON EL NUMERO DE INDICE
            nuevaPob.append(poblacion[ind1])
        else:
            nuevaPob.append(poblacion[ind2])
    return nuevaPob

def Seleccionar2(poblacion,fitness):
    nuevaPob=[]

    #Seleccionar al los demas individuos
    for i in range(2):
        #Seleccionar ruleta
        total = sum(fitness)
        ruleta = []
        for fit in fitness:
            ruleta.append(fit/total)
        #print("Ruleta: ",ruleta)
        r = random()
        #print("R: ",r)
        suma = 0
        ind = 0
        while(suma<r):
            suma += ruleta[ind]
            ind += 1
        #print("Indice: ",ind)
        nuevaPob.append(poblacion[ind-1])

    for i in range(2):
        #Seleccionar torneo
        ind1 = randint(0,3)
        ind2 = randint(0,3)
        while(ind1==ind2):
            ind2 = randint(0,3)
        r = random()
        if(r<0.7):
            if(fitness[ind1]>fitness[ind2]):
                nuevaPob.append(poblacion[ind1])
            else:
                nuevaPob.append(poblacion[ind2])
        else:
            if(fitness[ind1]<fitness[ind2]):
                nuevaPob.append(poblacion[ind1])
            else:
                nuevaPob.append(poblacion[ind2])
    return nuevaPob

def Seleccionar3(poblacion,fitness):
    nuevaPob=[]
    print("Seleccionar 3")

    #Seleccion basada en rangos
    n = len(poblacion)
    total = n*(n+1)/2
    print("Total:" + str(total))
    #Ordenar los fitness junto con la poblacion
    print("Antes:")
    print(poblacion)
    print(fitness)
    for i in range(len(fitness)):
        for j in range(len(fitness)-1):
            if fitness[j]>fitness[j+1]:
                fitness[j],fitness[j+1] = fitness[j+1],fitness[j]
                poblacion[j],poblacion[j+1] = poblacion[j+1],poblacion[j]
    print("Despues:")
    print(poblacion)
    print(fitness)
    rango = []
    for j in range(len(fitness)):
        rango.append((j+1)/total)

    for k in range(len(poblacion)):
        r = random()
        suma = 0
        ind = 0
        while(suma<r):
            suma += rango[ind]
            ind += 1
        nuevaPob.append(poblacion[ind-1])
    return nuevaPob

def Cruza(poblacion):
    nuevaPoblacion = []

    for i in range(2):
        padre1 = randint(0,3) #NUMERO DE INDICE
        padre2 = randint(0,3) #NUMERO DE INDICE

        while(padre1==padre2):
            padre2 = randint(0,3)

        puntoCruce = randint(1,4)

        hijo1 = poblacion[padre1][:puntoCruce]+poblacion[padre2][puntoCruce:]
        hijo2 = poblacion[padre2][:puntoCruce]+poblacion[padre1][puntoCruce:]

        nuevaPoblacion.append(hijo1)
        nuevaPoblacion.append(hijo2)

    return nuevaPoblacion

#Cruza de dos puntos
def Cruza2(poblacion):
    nuevaPoblacion = []

    for i in range(2):
        padre1 = randint(0,3) #NUMERO DE INDICE
        padre2 = randint(0,3) #NUMERO DE INDICE

        while(padre1==padre2):
            padre2 = randint(0,3)

        puntoCruce1 = randint(1,4)
        puntoCruce2 = randint(1,4)

        while(puntoCruce1==puntoCruce2):
            puntoCruce2 = randint(1,4)

        if puntoCruce1>puntoCruce2:
            puntoCruce1,puntoCruce2 = puntoCruce2,puntoCruce1
        

        hijo1 = poblacion[padre1][:puntoCruce1]+poblacion[padre2][puntoCruce1:puntoCruce2]+poblacion[padre1][puntoCruce2:]
        hijo2 = poblacion[padre2][:puntoCruce1]+poblacion[padre1][puntoCruce1:puntoCruce2]+poblacion[padre2][puntoCruce2:]

        print("padre1:")
        print(poblacion[padre1])
        print("padre2:")
        print(poblacion[padre2])
        print("puntoCruce1:")
        print(puntoCruce1)
        print("puntoCruce2:")
        print(puntoCruce2)
        print("hijo1:")
        print(hijo1)
        print("hijo2:")
        print(hijo2)

        nuevaPoblacion.append(hijo1)
        nuevaPoblacion.append(hijo2)
    
    return nuevaPoblacion

def Muta(poblacion):
    nuevaPoblacion = []
    for i in range(len(poblacion)):
        individuo = list(poblacion[i])
        if random()<=0.1:
            alelo = randint(0,4)
            print("Individuo original: ",individuo)
            if individuo[alelo]=='0':
                individuo[alelo]='1'
            else:
                individuo[alelo]='0'
            print("Individuo mutado: ",individuo)

        individuo=''.join(individuo)
        nuevaPoblacion.append(individuo)

    return nuevaPoblacion

def evaluacion(fitness):
    for fit in fitness:
        if fit==961:
            return True
    return False

#1.- Generar la población aleatoria de 4 individuos
poblacion=[]
poblacion=generarPoblacion(4)
#2.- Evaluar el fitness de cada individuo
fitness=evaluarPoblacion(poblacion)
paro = False
generacion = 0
while(paro!=True and generacion <= 30):
    #3.- Seleccionar los dos mejores individuos segun su fitness
    #Aplicar elitismo para el primer individuo
    print("Poblacion Inicial:")
    print(poblacion)
    poblacion=Seleccionar3(poblacion,fitness)
    print("Poblacion Seleccionada:")
    print(poblacion)
    poblacion=Cruza2(poblacion)
    print("Poblacion Cruzada:")
    print(poblacion)
    # Muta de un solo gen con prob. 0.1-10%
    poblacion=Muta(poblacion)
    fitness=evaluarPoblacion(poblacion)
    print("Poblacion Mutada:")
    print(poblacion)
    paro=evaluacion(fitness)
    generacion += 1
    print("Generacion: ",generacion)