from random import random, uniform, randint
#////////////////////////////////////////////////////////////////////////////////
def generadorPoblacion(n):
    poblacion = []
    for _ in range(n):
        i1 = round(uniform(-10.00, 10.00), 2)
        i2 = round(uniform(-10.00, 10.00), 2)
        i3 = round(uniform(-10.00, 10.00), 2)
        i4 = round(uniform(-10.00, 10.00), 2)
        i5 = round(uniform(-10.00, 10.00), 2)
        i6 = round(uniform(-10.00, 10.00), 2)
        i7 = round(uniform(-10.00, 10.00), 2)
        poblacion.append((i1, i2, i3, i4, i5, i6, i7))
    return poblacion
#////////////////////////////////////////////////////////////////////////////////
def mostrarPoblacion(poblacion):
    for i in range(len(poblacion)):
        fitness = getFitness(poblacion[i])
        
        # Aseguramos que los valores estén alineados correctamente
        valores = ", ".join([f"{x:6}" for x in poblacion[i]]) 

        print(f"solucion {i+1:4} --> {{{valores}}} --> fit: {fitness:6.2f}")
#////////////////////////////////////////////////////////////////////////////////
def matyas_function(x1, x2):
    return 0.26 * (x1**2 + x2**2) - 0.48 * x1 * x2
#////////////////////////////////////////////////////////////////////////////////
def getFitness(individuo):
    suma = 0

    # Calcula la sumatoria
    for i in range(len(individuo)-1):
        x1, x2 = individuo[i], individuo[i+1]
        suma += matyas_function(x1,x2)

    return suma
#////////////////////////////////////////////////////////////////////////////////
def promedioFit(poblacion):
    fitness = []

    # Obtiene el fitness de cada individuo 
    for i in range(len(poblacion)):
        fitness.append(getFitness(poblacion[i]))

    #calcula el promedio
    promedio = sum(fitness)/len(fitness)

    if promedio < 0.8:
        return True
    else:
        return False
#////////////////////////////////////////////////////////////////////////////////
def seleccionarElitismo(poblacion):
    fitness = []

    # Obtiene el fitness de cada individuo 
    for i in range(len(poblacion)):
        fitness.append(getFitness(poblacion[i]))

    # Ordena fitness y guarda los índices ordenados
    indices_ordenados = sorted(range(len(fitness)), key=lambda i: fitness[i], reverse=True)

    # Reorganizar la población según estos índices
    poblacion_ordenada = [poblacion[i] for i in indices_ordenados]

    return poblacion_ordenada[0] # Retorna el mas grande
#////////////////////////////////////////////////////////////////////////////////
def seleccionRuleta(poblacion, cantIndividuos):
    nuevaPob = [] #Guarda los individuos seleccionados
    fitness = []  #Guarda el fitness de cada individuo
    aptitud = []  #Guarda la aptitud de cada individuo
    probabilidad = [] #Guarda la probabilidad de cada individuo
    rangos = [] #Guarda los rangos de cada individuo

    #Calcula el fitness de cada individuo
    for i in range(len(poblacion)):
        fitness.append(getFitness(poblacion[i]))

    #Calcula la aptitud de cada individuo (1/fitness)
    for f in fitness:
        aptitud.append(1/f +0.0001) # + 0.01 para evitar divisiones entre 0
 
    #Calcula la suma de las aptitudes obtenidas
    sumaAptitudes = sum(aptitud)

    #Calcula la probabilidad de cada individuo
    for a in aptitud:
        probabilidad.append(a/sumaAptitudes)

    #calcula los rangos de las probabilidades
    rango = 0 
    for i in range(len(poblacion)):
        rango += probabilidad[i]
        rangos.append(rango)
        
    #Seleccion
    for i in range(cantIndividuos):
        r = random()                            #Genera un numero aleatorio entre 0 y 1
        for j in range(len(rangos)):            #Recorre los rangos
            if r < rangos[j]:                  #Si el numero aleatorio es menor al rango {
                nuevaPob.append(poblacion[j])       #Selecciona el individuo con ese indice
                break                               #Lo agrega y Sale del ciclo for j

    return nuevaPob
#////////////////////////////////////////////////////////////////////////////////
def torneoDeterminista(poblacion, cantIndividuos):
    nuevaPob = []

    for _ in range (cantIndividuos):
        #Elije dos aleatorios:
        par1 = randint (0, len(poblacion)-1)
        par2 = randint (0, len(poblacion)-1)

        # Evita que los padre se repitan
        while(par1==par2):
            par2 = randint (0, len(poblacion)-1)
        
        # evalua el fitness y guarda el que tenga menor fitness
        if (getFitness(poblacion[par1]) < getFitness(poblacion[par2])):
            nuevaPob.append(poblacion[par1])
        else: 
            nuevaPob.append(poblacion[par2])

    return nuevaPob # Retorna las poblaciones
#////////////////////////////////////////////////////////////////////////////////
def cruza(poblacion):
    hijos = [] # Guarda los hijos

    #Itera sobre la mitad de la poblacion. Esto creara 2 hijos por cada iteracion
    for _ in range(len(poblacion)//2):

        # Elige dos padres aleatorios
        p1 = randint(0, len(poblacion)-1) 
        p2 = randint(0, len(poblacion)-1)

        # Evita que los padres sean iguales
        while(p1==p2):
            p2 = randint(0,len(poblacion)-1)
        
        #Genera el aleatorio para ver si se cruzan
        r = random()

        #Evalua R
        if r <= 0.8:
            corte1 = randint(0,6) # Elije un punto de corte aleatorio
            corte2 = randint(0,6)

            # Evita que lso cortes sean iguales
            while (corte1==corte2):
                corte2=randint(0, 6)

            # Asegura que corte1 sea menor que corte2
            if corte1 > corte2:
                corte1, corte2 = corte2, corte1

            # Crea los hijos con dos puntos de corte
            hijo1 = poblacion[p1][:corte1] + poblacion[p2][corte1:corte2] + poblacion[p1][corte2:]
            hijo2 = poblacion[p2][:corte1] + poblacion[p1][corte1:corte2] + poblacion[p2][corte2:]

            # Agrega los hijos a la lista de hijos
            hijos.append(hijo1)
            hijos.append(hijo2)
        else: 
            # En caso de que el r no sea mayor a 0.8 agrega directamente a los padres
            hijos.append(p1)
            hijos.append(p2)
    return hijos
#////////////////////////////////////////////////////////////////////////////////
def mutacion(poblacion, mutation_rate):
    nuevaPob = []  # Guarda la nueva poblacion

    for i in range(len(poblacion)):
        individuo = list(poblacion[i])  # Convierte la tupla en lista
        r = random()             # Genera un numero aleatorio entre 0 y 1

        if r <= (mutation_rate / 100):
            nG1 = randint(0, 6)
            nG2 = randint(0, 6)
            nG3 = randint(0, 6)

            # Evita que se dupliquen
            while nG1 == nG2 or nG2 == nG3 or nG3 == nG1:
                nG2 = randint(0, 6)
                nG3 = randint(0, 6)

            # Muta rotando las posiciones
            individuo[nG1], individuo[nG2], individuo[nG3] = individuo[nG3], individuo[nG1], individuo[nG2]

        nuevaPob.append(tuple(individuo))

    return nuevaPob
#////////////////////////////////////////////////////////////////////////////////
startPoblation = generadorPoblacion(10)

print("\n\nPoblacion Inicial")
mostrarPoblacion(startPoblation) #Muestra la poblacion inicial

flag = False
generation = 0  

#Mientrasla generacion sea menor a 200 o promedio del fitness es menor a 0.8
while (flag != True or generation < 200):
    flag = True
    generation += 1

    #Seleccion
    selectedPoblation = []
    selectedPoblation.append(seleccionarElitismo(startPoblation))
    selectedPoblation.extend(seleccionRuleta(startPoblation, 5))
    selectedPoblation.extend(torneoDeterminista(startPoblation, 4))
    
    #Cruce
    hijos = cruza(selectedPoblation)

    mostrarPoblacion(hijos)
    #Mutacion
    #mutados = mutacion(hijos, 10)

    # Muestra la generacion despues del proceso genetico
    #print("\nGeneracion: ", generation)
    #mostrarPoblacion(mutados)

    #Evaluacion del fitness
    #flag = promedioFit(mutados)
    
    #Actualiza la poblacion inicial para el siguiente ciclo
    #startPoblation = mutados

    generation=200