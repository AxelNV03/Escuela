# MCSO220598 - MENDIETA CHIMAL SONY LUIS
# NSAO220388 - NAVA SANCHEZ AXEL
# TFJO220203 - TORRES FLORES JESUS ANTONIO
#////////////////////////////////////////////////////////////
from funciones import *
from vistas import *

startPoblation = generadorPoblacion(10) #Genera la poblacion inicial

print("\n\nPoblacion Inicial")
mostrarPoblacion(startPoblation) #Muestra la poblacion inicial

flag = False    
generation = 0  

#Mientrasla generacion sea menor a 200 y promedio del fitness es menor a 0.8
while(flag != True and generation < 10000): 
    flag = True
    generation += 1

    #Seleccion
    selectedPoblation = seleccionRuleta(startPoblation, 5) # Selecciona los primeros 5 individuos por ruleta
    selectedPoblation.extend(seleccionRango(startPoblation, 5)) # Selecciona los ultimos 5 individuos por rango

    #Cruce
    hijos = cruza(selectedPoblation) # Cruza los individuos seleccionados

    #Mutacion
    mutados = mutacion(hijos, 2.5) # Mutacion de los individuos cruzados
    
    # Muestra la generacion despues del proceso genetico
    print("\nGeneracion: ", generation)
    mostrarPoblacion(mutados)
    
    #Evaluacion
    flag = evaluacion(mutados) # Evalua si algun individuo tiene fitness 0

    #Actualiza la poblacion inicial para el siguiente ciclo
    startPoblation = mutados