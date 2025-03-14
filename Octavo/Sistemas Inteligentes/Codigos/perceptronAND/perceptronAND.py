import random
from funciones import *

#------------------------------------------------
true_table_AND = [
    [1, 1, 1],
    [1, 0, 0],
    [0, 0, 0],
    [0, 1, 0]
]
#--------------------------------------------

# Pesos (rango 1,-1)
W = []
W.append(random.randint(-1, 1))
W.append(random.randint(-1, 1))
umbral = random.randint(-1, 1)

iter, umbral = perceptron(true_table_AND, W, umbral)

# Entrada
entrada = [W[0], W[1]]
salida = inferencia(entrada, W, umbral)

# Muestra info
print("Pesos finales: ", W)
print("Umbral final: ", umbral)
print("Iteraciones: ", iter)
print("Entrada: ", entrada)
print("Salida: ", salida)
print("\n")
