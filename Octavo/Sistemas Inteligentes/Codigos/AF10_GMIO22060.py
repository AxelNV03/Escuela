from random import randint
from random import random

def generarIndividuo():
    individuo = []
    while(len(individuo) < 4):
        n = randint(1,4)
        if n not in individuo:
            individuo.append(n)
    return individuo

def generarPoblacion(cantInd):
    poblacion = []
    for _ in range(cantInd):
        poblacion.append(generarIndividuo())
    return poblacion

def evaluarIndividuo(individuo):
    # por cada individuo
    fit = 0
    for i, j in enumerate(individuo):
        y1 = j
        # por  cada individuos restantes
        for k in range(1, len(individuo)-i): 
            #    si estan en la misma fila  o   esta en diagonal 
            if(y1 == individuo[i+k] or k == abs(individuo[i+k] - y1)):
                fit += 1
    return fit

def evaluarPoblacion(poblacion):
    fitness = []
    for individuo in poblacion:
        fitness.append(evaluarIndividuo(individuo))
    return fitness

def imprimirTablero(individuo):
    tablero = []
    for i in range(4):
        fila = []
        for j in range(4):
            if(individuo[j]-1 == i):
                fila.append(str(1))
            else:
                fila.append(str(0))
        tablero.append(fila)
    # Imprimir tablero
    for fila in tablero:
        print(fila)

def imprimirPoblacion(poblacion, fitness, mensaje):
    print(mensaje)
    i = 0
    for individuo, fit in zip(poblacion, fitness):
        i += 1
        print("Individuo " + str(i))
        print(individuo)
        print("fitness: " + str(fit))
        imprimirTablero(individuo)
        print("")

def seleccionarRangos(poblacion, fitness, m):
    nuevaPob=[]
    print("Seleccionar por rangos")

    #Seleccion basada en rangos
    n = len(poblacion)
    print("N:" + str(n))
    total = n*(n+1)/2
    print("Total:" + str(total))
    #Ordenar los fitness junto con la poblacion

    for i in range(len(fitness)):
        for j in range(len(fitness)-1):
            if fitness[j]<fitness[j+1]:
                fitness[j],fitness[j+1] = fitness[j+1],fitness[j]
                poblacion[j],poblacion[j+1] = poblacion[j+1],poblacion[j]

    rango = []
    for j in range(len(fitness)):
        rango.append((j+1)/total)

    for k in range(m):
        r = random()
        suma = 0
        ind = 0
        while(suma<r):
            suma += rango[ind]
            ind += 1
        nuevaPob.append(poblacion[ind-1])
    return nuevaPob

def seleccionarTorneo(poblacion, fitness, n, prob):
    nuevaPob=[]
    print("Seleccionar por torneo")
    for _ in range(n):
        #Seleccionar torneo
        ind1 = randint(0,len(poblacion)-1)
        ind2 = randint(0,len(poblacion)-1)
        while(ind1==ind2):
            ind2 = randint(0,len(poblacion)-1)
        if(fitness[ind1]<fitness[ind2]):
            nuevaPob.append(poblacion[ind1])
        else:
            nuevaPob.append(poblacion[ind2])
    return nuevaPob

def seleccionarRuleta(poblacion, fitness, n):
    nuevaPob=[]
    prob = []
    print("Seleccionar por Ruleta")
    for f in fitness:
        prob.append(1/f)
    #Seleccionar ruleta
    total = sum(prob)
    ruleta = []
    for fit in fitness:
        ruleta.append(fit/total)
    for _ in range(n):
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
    return nuevaPob

def seleccionar(poblacion, fitness, n, prob):
    nuevaPob=[]
    print("Seleccionar")
    nuevaPob = seleccionarRuleta(poblacion, fitness, n)
    nuevaPob.extend(seleccionarTorneo(poblacion, fitness, len(poblacion)-n, prob))
    return nuevaPob

def cruza(poblacion):
    nuevaPob=[]

    for i in range(len(poblacion)//2):

        padre1 = randint(0,len(poblacion)-1) #NUMERO DE INDICE
        padre2 = randint(0,len(poblacion)-1) #NUMERO DE INDICE

        columna = randint(0,len(poblacion[0])-1) #NUMERO DE INDICE

        while(padre1==padre2):
            padre2 = randint(0,len(poblacion)-1)

        hijo1, hijo2 = poblacion[padre1], poblacion[padre2]
        hijo1[columna], hijo2[columna] = hijo2[columna], hijo1[columna]

        for j in range(len(hijo1)):
            if hijo1[columna] == hijo1[j] and j != columna:
                hijo1[j] = hijo2[columna]
            if hijo2[columna] == hijo2[j] and j != columna:
                hijo2[j] = hijo1[columna]
        
        nuevaPob.append(hijo1)
        nuevaPob.append(hijo2)

    return nuevaPob

def mutacion(poblacion):
    nuevaPob=[]
    for i in range(len(poblacion)):
        individuo = list(poblacion[i])
        if random()<=0.1:
            alelo1 = randint(0,3)
            alelo2 = randint(0,3)
            while(alelo1==alelo2):
                alelo2 = randint(0,3)

            individuo[alelo1], individuo[alelo2] = individuo[alelo2], individuo[alelo1]

            print("Mutacion ocurrida")

        nuevaPob.append(individuo)
    return nuevaPob

def evaluacion(fitness):
    for fit in fitness:
        if fit==0:
            return True
    return False

#individuo = [1,4,2,3]
#imprimirTablero(individuo)

#1.- Generar la población aleatoria de 4 individuos
poblacion = []
poblacion = generarPoblacion(10)
#2.- Evaluar el fitness de cada individuo
fitness = evaluarPoblacion(poblacion)
paro = False
generacion = 0
while(paro != True and generacion <= 30):
    imprimirPoblacion(poblacion, fitness, "Poblacion Inicial:")

    #3.- Seleccionar por rangos (5) y por torneo con prob. 0.8 (5) segun su fitness
    poblacion = seleccionar(poblacion, fitness, 5, 0.8)
    fitness = evaluarPoblacion(poblacion)
    imprimirPoblacion(poblacion, fitness, "Poblacion Seleccionada:")

    #4.- Cruzar los individuos seleccionados
    poblacion = cruza(poblacion)
    fitness = evaluarPoblacion(poblacion)
    imprimirPoblacion(poblacion, fitness, "Poblacion Cruzada:")

    #5.- Mutar los individuos cruzados
    poblacion = mutacion(poblacion)
    fitness = evaluarPoblacion(poblacion)
    imprimirPoblacion(poblacion, fitness, "Poblacion Mutada:")

    generacion += 1
    paro = evaluacion(fitness)
    print("Generacion:")
    print(generacion)