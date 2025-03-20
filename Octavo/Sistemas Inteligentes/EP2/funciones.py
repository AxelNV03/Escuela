from random import randint, random

#////////////////////////////////////////////////
def generadorPoblacion(n):
    poblacion = []
    for i in range(n):
        x = randint(-5, 5)
        y = randint(-5, 5)
        z = randint(-5, 5)
        u = randint(-5, 5)
        poblacion.append((x, y, z, u))
    return poblacion
#////////////////////////////////////////////////
def sistema_ecuaciones(x, y, z, u):
    ec1 = (-2*x) + (3*y) -z + (2*u)
    ec2 = (3*x) - y + (3*z) -u 
    ec3 = (-x) + (2*y) + (5*z) - (2*u)  
    ec4 = (6*x) - (3*y) + z + u
    return ec1, ec2, ec3, ec4
#////////////////////////////////////////////////
def getFitness (x, y, z, u):
    valor = abs(x-2) + abs(y-2) + abs(z-11) + abs(u+4)  
    return valor
#////////////////////////////////////////////////
def seleccionRuleta(poblacion, cantIndividuos):
    nuevaPob = [] #Guarda los individuos seleccionados
    fitness = []  #Guarda el fitness de cada individuo
    aptitud = []  #Guarda la aptitud de cada individuo
    probabilidad = [] #Guarda la probabilidad de cada individuo
    rangos = [] #Guarda los rangos de cada individuo

    #Calcula el fitness de cada individuo
    for i in range(len(poblacion)):
        fitness.append(getFitness(poblacion[i][0], poblacion[i][1], poblacion[i][2], poblacion[i][3]))

    #Calcula la aptitud de cada individuo (1/fitness)
    for i in range(len(poblacion)):
        aptitud.append(1/fitness[i]+0.01) # + 0.01 para evitar divisiones entre 0

    #Calcula la suma de las aptitudes obtenidas
    sumaAptitudes = sum(aptitud)

    #Calcula la probabilidad de cada individuo
    for i in range(len(poblacion)):
        probabilidad.append(aptitud[i]/sumaAptitudes)

    #calcula los rangos de las probabilidades
    rango = 0 
    for i in range(len(poblacion)):
        rango += probabilidad[i]
        rangos.append(rango)

    
    #Seleccion
    for i in range(cantIndividuos):
        r = random()                            #Genera un numero aleatorio entre 0 y 1
        for j in range(len(rangos)):            #Recorre los rangos
            if r <= rangos[j]:          #Si el numero aleatorio es menor o igual al rango
                nuevaPob.append(poblacion[j])   #Selecciona el individuo
                break                           #Sale del ciclo for j

    return nuevaPob
#////////////////////////////////////////////////
def seleccionRango(poblacion, cantIndividuos):
    nuevaPob = [] #Guarda los individuos seleccionados
    fitness = []  #Guarda el fitness de cada individuo
    suma_rank = len(poblacion) * (len(poblacion)+1)/2  # Suma de las posiciones de los individuos
    rangos = [] #Guarda los rangos de cada individuo

    #Calcula el fitness de cada individuo
    for i in range(len(poblacion)):
        fitness.append(getFitness(poblacion[i][0], poblacion[i][1], poblacion[i][2], poblacion[i][3]))

    # Ordena fitness y guarda los índices ordenados
    indices_ordenados = sorted(range(len(fitness)), key=lambda i: fitness[i])

    # Reorganizar la población según estos índices
    poblacion_ordenada = [poblacion[i] for i in indices_ordenados]

    #Asigna probabilidad a cada individuo
    probabilidad = []
    for i in range(len(poblacion)):
        probabilidad.append((i+1)/suma_rank)

    #Suma de las probabilidades
    aux = 0 
    for i in range(len(poblacion)):
        aux += probabilidad[i]
        rangos.append(aux)`

    #Seleccion
    for i in range(cantIndividuos):
        r = random()                            #Genera un numero aleatorio entre 0 y 1
        for j in range(len(rangos)):            #Recorre los rangos
            if r <= rangos[j]:          #Si el numero aleatorio es menor o igual al rango
                nuevaPob.append(poblacion_ordenada[j])   #Selecciona el individuo
                break                           #Sale del ciclo for j
    
    return nuevaPob
#////////////////////////////////////////////////
def selecionPadres(poblacion):
    hijos = [] # Guarda los hijos

    #Itera sobre la mitad de la poblacion. Esto creara 2 hijos por cada iteracion
    for i in range(len(poblacion)//2):

        # Elige dos padres aleatorios
        p1 = randint(0, len(poblacion)-1) 
        p2 = randint(0, len(poblacion)-1)

        # Evita que los padres sean iguales
        while(p1==p2):
            p2 = randint(0,len(poblacion)-1)
        
        # Elije un punto de cruce aleatorio
        corte = randint(0,len(poblacion[0])-1)

        # Crea los hijos
        


    pass
#////////////////////////////////////////////////
def cruza():
    pass