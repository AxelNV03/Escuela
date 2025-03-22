from funciones import getFitness

def mostrarPoblacion(poblacion):
    for i in range(len(poblacion)):
        fitness = getFitness(poblacion[i][0], poblacion[i][1], poblacion[i][2], poblacion[i][3])
        
        # Aseguramos que los valores estén alineados correctamente
        valores = ", ".join([f"{x:3}" for x in poblacion[i]]) 

        print(f"solucion {i+1:4} --> {{{valores}}} --> fit: {fitness:6.2f}")
