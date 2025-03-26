from enum import Enum, auto
from random import randint, random
from typing import Callable, Generic, Optional, TypeVar

V = TypeVar("V")
C = TypeVar("C")


class Pueblerino(Generic[V, C]):
    def __init__(self, valor: V, codificacion: C, fitness: float) -> None:
        self.valor = valor
        self.codificacion = codificacion
        self.fitness = fitness

    def __str__(self) -> str:
        return f"{{ Valor: {self.valor} Codificacion: {self.codificacion} Fitness: {self.fitness} }}"


class AlgoritmoGenetico(Generic[V, C]):
    class ModoSeleccion(Enum):
        ELITISMO = auto()
        RANGOS = auto()
        RULETA = auto()

    def __init__(
        self,
        # Funcion para realizar la cruza
        cruza: Callable[[list[Pueblerino[V, C]]], list[Pueblerino[V, C]]],
        # Funcion para mutar la poblacion
        muta: Callable[[list[Pueblerino[V, C]]], list[Pueblerino[V, C]]],
        # Funcion para determinar si se llegó al objetivo
        paro: Callable[[list[Pueblerino[V, C]]], bool],
    ) -> None:
        self.cruza = cruza
        self.muta = muta
        self.paro = paro

    def elitismo(self, poblacion: list[Pueblerino[V, C]]) -> list[Pueblerino[V, C]]:
        nueva_poblacion: list[Pueblerino[V, C]] = []
        mejor = max(poblacion, key=lambda p: p.fitness)
        nueva_poblacion.append(mejor)

        max_index = len(poblacion) - 1
        for _ in range(max_index):
            ind1 = randint(0, max_index)
            ind2 = randint(0, max_index)
            while ind1 == ind2:
                ind2 = randint(0, max_index)

            if poblacion[ind1].fitness > poblacion[ind2].fitness:
                nueva_poblacion.append(poblacion[ind1])
            else:
                nueva_poblacion.append(poblacion[ind2])

        return nueva_poblacion

    def rangos(self, poblacion: list[Pueblerino[V, C]]) -> list[Pueblerino[V, C]]:
        nueva_poblacion: list[Pueblerino[V, C]] = []
        poblacion_ordenada = sorted(poblacion, key=lambda p: p.fitness)

        size = len(poblacion)

        # Formula de los primeros n numeros naturales
        sumatoria_ranking = size * (size + 1) / 2

        rangos = [0.0]
        for i in range(size):
            porcentaje = (i + 1) / sumatoria_ranking
            porcentaje_acumulado = rangos[i] + porcentaje
            redondeo = round(porcentaje_acumulado, 3)
            rangos.append(redondeo)

        for _ in range(size):
            random_num = random()

            for i in range(len(rangos)):
                if rangos[i - 1] <= random_num < rangos[i]:
                    seleccion = poblacion_ordenada[i - 1]
                    nueva_poblacion.append(seleccion)
                    break

        return nueva_poblacion

    def ruleta(self, poblacion: list[Pueblerino[V, C]]) -> list[Pueblerino[V, C]]:
        nueva_poblacion: list[Pueblerino[V, C]] = []
        poblacion_ordenada = sorted(poblacion, key=lambda p: p.fitness, reverse=True)
        aptitud_total = sum(p.fitness for p in poblacion_ordenada)

        size = len(poblacion)
        rangos = [0.0]

        for i in range(size):
            p = poblacion_ordenada[i]
            porcentaje = p.fitness / aptitud_total
            porcentaje_acumulado = rangos[i] + porcentaje
            rangos.append(round(porcentaje_acumulado, 3))

        for _ in range(size):
            random_num = random()

            for i in range(len(rangos)):
                if rangos[i - 1] <= random_num < rangos[i]:
                    seleccionado = poblacion_ordenada[i - 1]
                    nueva_poblacion.append(seleccionado)
                    break

        return nueva_poblacion

    def ejecutar_algoritmo(
        self,
        poblacion: list[Pueblerino[V, C]],
        seleccion: ModoSeleccion,
        lim_generaciones: Optional[int] = None,
    ):
        generacion = 0
        poblacion_cpy = poblacion.copy()

        seleccionMatcher = {
            self.ModoSeleccion.ELITISMO: self.elitismo,
            self.ModoSeleccion.RULETA: self.ruleta,
            self.ModoSeleccion.RANGOS: self.rangos,
        }

        print(f"Poblacion inicial")
        for p in poblacion_cpy:
            print(p)

        while not self.paro(poblacion_cpy) and (
            lim_generaciones == None or generacion <= lim_generaciones
        ):
            poblacion_cpy = seleccionMatcher[seleccion](poblacion_cpy)
            poblacion_cpy = self.cruza(poblacion_cpy)
            poblacion_cpy = self.muta(poblacion_cpy)

            print(f"Generacion {generacion}")
            for p in poblacion_cpy:
                print(p)

            generacion += 1


if __name__ == "__main__":

    def calcular_fitness(valor: int):
        return valor**2

    def generar_poblacion_binaria_aleatoria(
        num_pueblerinos: int,
        bits: int,
    ) -> list[Pueblerino]:
        if bits <= 0 or num_pueblerinos <= 0:
            error = f"Los valores deben ser enteros positivos, se recibió {num_pueblerinos} y {bits}"
            raise Exception(error)

        poblacion: list[Pueblerino] = []

        for _ in range(num_pueblerinos):
            max_num_binario_posible = 2**bits - 1
            codificacion = format(randint(0, max_num_binario_posible), f"0{bits}b")
            valor = int(codificacion, 2)
            fitness = calcular_fitness(valor)
            poblacion.append(Pueblerino(valor, codificacion, fitness))

        return poblacion

    def muta(
        poblacion: list[Pueblerino],
        probabilidad_muta: float = 0.1,
    ) -> list[Pueblerino]:
        nueva_poblacion = []
        if probabilidad_muta > 1 or probabilidad_muta < 0:
            raise ValueError("La probabilidad de muta debe estar entre 0 y 1")

        for i in range(len(poblacion)):
            pueblerino = poblacion[i]
            codificacion_arr = list(pueblerino.codificacion)
            if random() <= probabilidad_muta:
                alelo = randint(0, len(codificacion_arr) - 1)
                if codificacion_arr[alelo] == "0":
                    codificacion_arr[alelo] = "1"
                else:
                    codificacion_arr[alelo] = "0"

            codificacion = "".join(codificacion_arr)
            valor = int(codificacion, 2)
            nuevo_pueblerino = Pueblerino(
                codificacion=codificacion,
                valor=valor,
                fitness=calcular_fitness(valor),
            )
            nueva_poblacion.append(nuevo_pueblerino)
        return nueva_poblacion

    def cruza(poblacion: list[Pueblerino]) -> list[Pueblerino]:
        nuevaPob = []
        tamanio_poblacion = len(poblacion)
        num_parejas = tamanio_poblacion // 2  # Número de parejas (división entera)
        longitud_codificacion = len(poblacion[0].codificacion)

        for _ in range(num_parejas):
            ind_padre1 = randint(0, tamanio_poblacion - 1)
            ind_padre2 = randint(0, tamanio_poblacion - 1)

            while ind_padre1 == ind_padre2:  # Evitar que sea el mismo padre
                ind_padre2 = randint(0, tamanio_poblacion - 1)

            puntoCruce = randint(1, longitud_codificacion - 1)
            padre1 = poblacion[ind_padre1]
            padre2 = poblacion[ind_padre2]

            codificacion_hijo1 = (
                padre1.codificacion[:puntoCruce] + padre2.codificacion[puntoCruce:]
            )

            codificacion_hijo2 = (
                padre2.codificacion[:puntoCruce] + padre1.codificacion[puntoCruce:]
            )

            valor = int(codificacion_hijo1, 2)
            codificacion = codificacion_hijo1
            fitness = calcular_fitness(valor)
            hijo1 = Pueblerino(valor, codificacion, fitness)
            valor = int(codificacion_hijo2, 2)
            codificacion = codificacion_hijo2
            fitness = calcular_fitness(valor)
            hijo2 = Pueblerino(
                valor=valor,
                codificacion=codificacion,
                fitness=fitness,
            )

            nuevaPob.append(hijo1)
            nuevaPob.append(hijo2)

        # Si el tamaño de la población es impar, generar un hijo adicional
        if tamanio_poblacion % 2 != 0:
            ind_padre1 = randint(0, tamanio_poblacion - 1)
            ind_padre2 = randint(0, tamanio_poblacion - 1)

            while ind_padre1 == ind_padre2:
                padre2 = randint(0, tamanio_poblacion - 1)

            puntoCruce = randint(1, longitud_codificacion - 1)
            padre1 = poblacion[ind_padre1]
            padre2 = poblacion[ind_padre2]
            codificacion_hijo = (
                padre1.codificacion[:puntoCruce] + padre2.codificacion[puntoCruce:]
            )
            valor = int(codificacion_hijo, 2)
            codificacion = codificacion_hijo
            fitness = calcular_fitness(valor)
            hijo = Pueblerino(
                valor=valor,
                codificacion=codificacion,
                fitness=fitness,
            )
            nuevaPob.append(hijo)

        return nuevaPob

    def paro(poblacion: list[Pueblerino]):
        for pueblerino in poblacion:
            if pueblerino.fitness == 961:
                return True
        return False

    algoritmo = AlgoritmoGenetico(cruza=cruza, paro=paro, muta=muta)
    poblacion = generar_poblacion_binaria_aleatoria(num_pueblerinos=10, bits=5)
    algoritmo.ejecutar_algoritmo(
        poblacion=poblacion,
        seleccion=AlgoritmoGenetico.ModoSeleccion.ELITISMO,
        lim_generaciones=30,
    )
