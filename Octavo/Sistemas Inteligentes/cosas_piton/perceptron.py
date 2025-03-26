# Perceptron
from random import random
from typing import Callable, Optional


def evaluar_neurona_perceptron(
    entrada: list[float],
    pesos: list[float],
    umbral: float,
    f: Callable[[float], float],
) -> float:
    assert len(entrada) == len(pesos)

    acumulado = 0
    for i in range(len(entrada)):
        acumulado = acumulado + (entrada[i] * pesos[i] + umbral)

    return f(acumulado)


def aprendizaje_perceptron(
    modificacion_peso: Callable[
        [
            float,  # entrada actual
            float,  # Peso actual
            float,  # umbral actual
            float,  # resultado
            float,  # salida esperada
        ],
        float,  # retorno
    ],
    modificacion_umbral: Callable[
        [
            float,  # umbral actual
            float,  # resultado
            float,  # salida esperada
        ],
        float,  # retorno
    ],
    entradas: list[list[float]],
    salidas_esperadas: list[float],
    f: Callable[[float], float],
    pesos: Optional[list[float]] = None,
    umbral_inicial: Optional[float] = None,
    lim_iteraciones: Optional[int] = None,
) -> tuple[list[float], float]:
    if pesos == None:
        nums_a_generar = len(entradas[0])
        pesos = [random() for i in range(nums_a_generar)]

    umbral: float = random() if umbral_inicial == None else umbral_inicial

    iteraciones = 0
    continuar = True
    while continuar and (lim_iteraciones == None or iteraciones < lim_iteraciones):
        iteraciones += 1
        continuar = False

        print(f"-------- Iteracion {iteraciones} ---------")
        for i in range(len(entradas)):
            resultado = evaluar_neurona_perceptron(
                entrada=entradas[i],
                f=f,
                pesos=pesos,
                umbral=umbral,
            )

            print(f"Entrada {i+1} {entradas[i]}")
            print(f"Pesos: {pesos}")
            print(f"Umbral: {umbral}")
            print(f"Resultado: {resultado}")
            print(f"Resultado esperado {salidas_esperadas[i]}")
            print()

            if resultado != salidas_esperadas[i]:
                pesos = [
                    modificacion_peso(
                        entradas[i][j],
                        pesos[j],
                        umbral,
                        resultado,
                        salidas_esperadas[i],
                    )
                    for j in range(len(entradas[i]))
                ]
                print(
                    f"umbral {umbral} resultado {resultado} salida esperada {salidas_esperadas[i]}"
                )
                umbral = modificacion_umbral(umbral, resultado, salidas_esperadas[i])
                continuar = True

                print(f"Modificacion iteracion {iteraciones} entrada {i + 1}")
                print(f"Pesos: {pesos}")
                print(f"Umbral: {umbral}")
                print()
            else:
                print("No se modifica ningun valor")
                print()
        print(f"------------------------------------------")
    return (pesos, umbral)


print("----- PUERTA LOGICA AND ------")
pesos, umbral = aprendizaje_perceptron(
    entradas=[
        [-1.0, -1.0],  # F and F
        [+1.0, -1.0],  # F and V
        [-1.0, +1.0],  # V and F
        [+1.0, +1.0],  # V and V
    ],
    salidas_esperadas=[-1.0, -1.0, -1.0, +1.0],  # F  # F  # F  # V
    pesos=[1.0, 1.0],
    f=lambda x: 1 if x > 0 else -1,
    modificacion_peso=(
        lambda entrada_actual, peso_actual, umbral_actual, resultado_actual, salida_esperada: peso_actual
        + (salida_esperada * entrada_actual)
    ),
    modificacion_umbral=(
        lambda umbral_actual, resultado, salida_esperada: umbral_actual
        + salida_esperada
    ),
)
print(f"Pesos finales: {pesos}")
print(f"Umbral final: {umbral}")

print("----- PROBLEMA ASISTENCIAs ------")
pesos, umbral = aprendizaje_perceptron(
    entradas=[
        # Horas, asistencia
        [+2.0, -1.0],
        [+3.0, +1.0],
        [-4.0, +1.0],
        [+1.0, -1.0],
        [+5.0, +1.0],
        [+6.0, +1.0],
        [+3.0, -1.0],
        [+4.0, -1.0],
    ],
    salidas_esperadas=[
        # aprueba
        -1.0,
        +1.0,
        +1.0,
        -1.0,
        +1.0,
        +1.0,
        -1.0,
        -1.0,
    ],
    pesos=[1.0, 1.0],
    f=lambda x: 1 if x > 0 else -1,
    modificacion_peso=(
        lambda entrada_actual, peso_actual, umbral_actual, resultado_actual, salida_esperada: peso_actual
        + (salida_esperada * entrada_actual)
    ),
    modificacion_umbral=(
        lambda umbral_actual, resultado, salida_esperada: umbral_actual
        + salida_esperada
    ),
)
print(f"Pesos finales: {pesos}")
print(f"Umbral final: {umbral}")
