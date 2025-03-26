from abc import ABC, abstractmethod
from enum import Enum, auto
from random import randint
from typing import Any, Callable, Generic, Optional, TypeVar

from containers import Container, Queue, Stack
from nodes import NonWeightedVertex, Vertex, WeightedVertex

T = TypeVar("T")
Adjacency = TypeVar("Adjacency")


class Graph(Generic[T, Adjacency], ABC):
    """
    Clase abstracta que representa un grafo genérico con tipos parametrizados.

    Atributos:
        label (str): Etiqueta descriptiva del grafo
        vertexs (list[Vertex[T, Adjacency]]): Lista de vértices del grafo

    Args:
        T: Tipo de dato almacenado en los vértices
        Adjacency: Tipo de las relaciones de adyacencia

    Raises:
        ValueError: Si se proporcionan vértices que no son instancias de Vertex
    """

    class Direction(Enum):
        """Enumera las direcciones de recorrido posibles"""

        LEFT = auto()  # Recorrido por la izquierda (adyacencias invertidas)
        RIGHT = auto()  # Recorrido por la derecha (orden natural)

    class Algorithm(Enum):
        """Enumera los algoritmos de recorrido disponibles"""

        BFS = auto()  # Breadth-First Search
        DFS = auto()  # Depth-First Search

    class Objective(Enum):
        MINIMIZE = auto()
        MAXIMIZE = auto()

    def __init__(
        self, label: str, vertexs: Optional[list[Vertex[T, Adjacency]]] = None
    ) -> None:
        """
        Inicializa un nuevo grafo.

        Args:
            label: Nombre identificativo del grafo
            vertexs: Lista opcional de vértices iniciales
        """
        self.label = label

        if vertexs and not all(isinstance(v, Vertex) for v in vertexs):
            raise ValueError("All elements in 'vertexs' must be instances of Vertex.")

        self.vertexs: list[Vertex[T, Adjacency]] = vertexs if vertexs else []

    @abstractmethod
    def vertex_from_adjacency(self, adjacency: Adjacency) -> Vertex[T, Adjacency]:
        """
        Método abstracto para obtener el vértice destino desde una adyacencia.

        Args:
            adjacency: Relación de adyacencia a convertir

        Returns:
            Vértice correspondiente a la adyacencia
        """
        pass

    def adj_str(self, adjacency: Adjacency) -> str:
        """
        Formatea una adyacencia para representación como cadena.

        Args:
            adjacency: Relación de adyacencia a formatear

        Returns:
            Representación en cadena de la adyacencia
        """
        return str(adjacency)

    def show_adjacencies(self) -> None:
        """Muestra todas las adyacencias del grafo en formato legible."""
        print(f"Adyacencias de {self.label}:")
        for vertex in self.vertexs:
            adj_str = ", ".join(self.adj_str(adj) for adj in vertex.adjacencies)
            print(f"{vertex} -> {{{adj_str}}}")
        print()

    def reset_visited(self) -> None:
        """Reinicia el estado de visitado de todos los vértices."""
        for vertex in self.vertexs:
            vertex.visited = False

    def print_adjacency(
        self,
        vertex: Vertex[T, Adjacency],
        _: Optional[Any],
    ) -> tuple[bool, Optional[Any]]:
        """
        Acción por defecto para imprimir vértices durante el recorrido.

        Args:
            vertex: Vértice actual siendo visitado
            _: Argumento adicional no utilizado

        Returns:
            Tupla (False, None) para continuar el recorrido
        """
        print(f"  {vertex}")
        return (False, None)

    def equals(
        self, vertex: Vertex, vertex2: Optional[Any]
    ) -> tuple[bool, Optional[Any]]:
        """
        Compara dos vértices para búsqueda.

        Args:
            vertex: Vértice actual siendo visitado
            vertex2: Vértice buscado como objetivo

        Returns:
            Tupla (True, None) si coinciden, (False, None) en caso contrario

        Raises:
            ValueError: Si vertex2 no es una instancia de Vertex
        """
        if vertex2 is None or not isinstance(vertex2, Vertex):
            raise ValueError("Arg should be a Vertex")

        self.print_adjacency(vertex, None)

        return (True, None) if vertex is vertex2 else (False, None)

    def explore(
        self,
        start: Vertex[T, Adjacency],
        algorithm: Algorithm,
        direction: Direction = Direction.RIGHT,
        lvl_limit: Optional[int] = None,
        set_lvls: bool = False,
        iterative: bool = False,
        action: Optional[
            Callable[[Vertex[T, Adjacency], Optional[Any]], tuple[bool, Optional[Any]]]
        ] = None,
        arg: Optional[Any] = None,
    ) -> Optional[Any]:
        """
        Realiza un recorrido parametrizado del grafo ejecutando lógica personalizada en cada vértice.

        Parámetros:
            start: Vértice raíz donde inicia el recorrido
            algorithm: Estrategia de recorrido (Algoritmo.BFS o Algoritmo.DFS)
            direction: Orden de procesamiento de adyacencias (LEFT=invertido, RIGHT=natural)
            lvl_limit: Limitar la busqueda a un nivel específico, para esto los vértices deben
                tener el nivel puesto de forma correcta, si no se estableció ningún nivel la función
                soltará una excepción durante el recorrido o si se establecen niveles mal puede ocurrir
                un comportamiento inesperado
            set_lvls: Ejecutar la función self.set_lvls(start) antes de empezar la exploración
            iterative: Recorrer un arbol de forma iterativa (potencial error de ciclado en grafos)
            action: Función callback con firma:
                   (vértice_actual, arg) -> (detener_recorrido: bool, valor_retorno: Any)
                   - Si detener_recorrido = True, se aborta el recorrido y retorna valor_retorno
                   - Si detener_recorrido = False, continúa normalmente
            arg: Argumento opcional que se pasa a la función 'action'

        Retorno:
            - Valor retornado por 'action' si detiene el recorrido
            - None si completa todo el recorrido sin interrupciones
        """
        if set_lvls:
            self.set_lvls(start)

        loop = 1
        vertex_visited = 0
        vertex_before_loop = 0

        vertex_to_check: Container[Vertex[T, Adjacency]] = (
            Stack() if algorithm == self.Algorithm.DFS else Queue()
        )

        if action is None:
            action = self.print_adjacency
        assert action is not None

        limitTitle = f"con límite {lvl_limit}" if lvl_limit is not None else ""
        print(f"Recorrido {algorithm.name} por {direction.name} {limitTitle}")

        vertex_to_check.add(start)
        vertex_before_loop += 1
        if not iterative:
            start.visited = True

        while not vertex_to_check.is_empty():
            curr_v = vertex_to_check.get()

            if curr_v is None:
                raise RuntimeError("Vertice actual es None")

            end_explore, value_return = action(curr_v, arg)

            if end_explore:
                print()
                self.reset_visited()
                return value_return

            vertex_visited += 1

            if iterative and vertex_visited == vertex_before_loop:
                loop += 1
                vertex_to_check = (
                    Stack() if algorithm == self.Algorithm.DFS else Queue()
                )
                vertex_to_check.add(start)
                vertex_before_loop += 1
                vertex_visited = 0
                print(f"\nIteración {loop}")
                continue

            adjacencies = (
                curr_v.adjacencies
                if direction == self.Direction.RIGHT
                else list(reversed(curr_v.adjacencies))
            )

            for adjacency in adjacencies:
                neighbor = self.vertex_from_adjacency(adjacency)

                if lvl_limit is not None:
                    assert neighbor.lvl
                    should_add = not neighbor.visited and neighbor.lvl <= lvl_limit

                else:
                    should_add = not neighbor.visited

                if should_add:
                    vertex_to_check.add(neighbor)
                    if not iterative:
                        neighbor.visited = True

        print()
        self.reset_visited()
        return None

    def seek(
        self,
        start: Vertex[T, Adjacency],
        seek: Vertex[T, Adjacency],
        algorithm: Algorithm = Algorithm.BFS,
        direction: Direction = Direction.RIGHT,
        lvl_limit: Optional[int] = None,
        set_lvls: bool = False,
        iterative: bool = False,
        eval_eq: Callable[
            [Vertex[T, Adjacency], Vertex[T, Adjacency]], bool
        ] = lambda v1, v2: v1
        == v2,
    ) -> Optional[int]:
        """
        Busca un vértice en el grafo mediante recorrido.

        Args:
            start: Vértice inicial de búsqueda
            seek: Vértice objetivo a encontrar
            algorithm: Algoritmo de búsqueda a utilizar
            direction: Dirección de procesamiento de adyacencias
            direction: Orden de procesamiento de adyacencias (LEFT=invertido, RIGHT=natural)
            lvl_limit: Limitar la busqueda a un nivel específico, para esto los vértices deben
                tener el nivel puesto de forma correcta, si no se estableció ningún nivel la función
                soltará una excepción durante el recorrido o si se establecen niveles mal puede ocurrir
                un comportamiento inesperado
            set_lvls: Ejecutar la función self.set_lvls(start) antes de empezar la exploración

        Returns:
            None cuando encuentra el vértice o si no existe
        """
        nodesVisited = [0]

        def action(v: Vertex[T, Adjacency], arg) -> tuple[bool, Any]:
            arg[0] += 1

            print(f"{v}")
            return (eval_eq(v, seek), arg[0])

        print(f"Buscando {seek}")
        return self.explore(
            start=start,
            algorithm=algorithm,
            direction=direction,
            action=action,
            arg=nodesVisited,
            lvl_limit=lvl_limit,
            set_lvls=set_lvls,
            iterative=iterative,
        )

    def set_lvls(
        self, root: Vertex[T, Adjacency], direction: Direction = Direction.RIGHT
    ):
        vertex_to_check = Queue[Vertex[T, Adjacency]]()
        print("Calculando niveles...")
        root.visited = True
        root.lvl = 1
        vertex_to_check.enqueue(root)

        while not vertex_to_check.is_empty():
            curr_v = vertex_to_check.get()
            assert curr_v is not None
            assert curr_v.lvl is not None

            print(f"  {curr_v}")

            adjacencies = (
                curr_v.adjacencies
                if direction == self.Direction.RIGHT
                else list(reversed(curr_v.adjacencies))
            )

            for adj in adjacencies:
                vertex = self.vertex_from_adjacency(adj)
                if not vertex.visited:
                    vertex.visited = True
                    vertex.lvl = curr_v.lvl + 1
                    vertex_to_check.add(vertex)

        print()
        self.reset_visited()

    def hill_climbing(
        self,
        start: Vertex[T, Adjacency],
        seek: Vertex[T, Adjacency],
        action: Callable[
            [
                Vertex[T, Adjacency],  # curr_v
                Vertex[T, Adjacency],  # seek
                Any,  # arg
            ],
            tuple[bool, Optional[Any]],  # (end_explore, return)
        ],
        heuristic: Callable[
            [
                Vertex[T, Adjacency],  # adjacency
                Vertex[T, Adjacency],  # curr_v
                Vertex[T, Adjacency],  # seek
                Any,  # arg
            ],
            float,
        ],
        objective: Objective = Objective.MINIMIZE,
        arg: Optional[Any] = None,
    ):
        print("Recorrido Hill Climbing")
        reverse = False if objective == self.Objective.MINIMIZE else True
        agenda: list[Vertex[T, Adjacency]] = []
        agenda.append(start)
        while not len(agenda) == 0:
            curr_v = agenda.pop()
            assert curr_v is not None

            end_explore, returnValue = action(curr_v, seek, arg)

            if end_explore:
                return returnValue

            for adjacency in curr_v.adjacencies:
                vertex = self.vertex_from_adjacency(adjacency)
                agenda.append(vertex)

            if len(agenda) != 0:
                # Ordenar la agenda usando la heurística
                agenda.sort(
                    key=lambda v: heuristic(v, curr_v, seek, arg), reverse=reverse
                )

                # Obtener el valor mínimo de la heurística
                choosen_heuristic = heuristic(agenda[0], curr_v, seek, arg)

                # Filtrar las soluciones con la heurística mínima
                min_solutions = [
                    v
                    for v in agenda
                    if heuristic(v, curr_v, seek, arg) == choosen_heuristic
                ]

                # Elegir una solución
                choosen_index = randint(0, len(min_solutions) - 1)
                choosen_opt = min_solutions[choosen_index]
                agenda = [choosen_opt]
            else:
                return None

    def a_star(
        self,
        start: Vertex[T, Adjacency],
        seek: Vertex[T, Adjacency],
        action: Callable[
            [
                Vertex[T, Adjacency],  # curr_v
                Vertex[T, Adjacency],  # seek
                Any,  # arg
            ],
            tuple[bool, Optional[Any]],  # (end_explore, return)
        ],
        heuristic: Callable[
            [
                Vertex[T, Adjacency],  # adjacency
                Vertex[T, Adjacency],  # curr_v
                Vertex[T, Adjacency],  # seek
                Any,  # arg
            ],
            float,
        ],
        g: Callable[
            [
                Vertex[T, Adjacency],  # adjacency
                Vertex[T, Adjacency],  # curr_v
                Vertex[T, Adjacency],  # seek
                Any,  # arg
            ],
            float,
        ],
        objective: Objective = Objective.MINIMIZE,
        arg: Optional[Any] = None,
    ):
        print("Recorrido A*")
        reverse = False if objective == self.Objective.MINIMIZE else True

        agenda: list[Vertex[T, Adjacency]] = []

        agenda.append(start)

        def f(
            adjacency: Vertex[T, Adjacency],  # adjacency
            curr_v: Vertex[T, Adjacency],  # curr_v
            seek: Vertex[T, Adjacency],  # seek
            arg: Any,  # arg
        ) -> float:
            return g(adjacency, curr_v, seek, arg) + heuristic(
                adjacency, curr_v, seek, arg
            )

        while len(agenda) != 0:
            curr_v = agenda.pop()

            end_explore, return_value = action(curr_v, seek, arg)

            if end_explore:
                return return_value

            for adjacency in curr_v.adjacencies:
                vertex = self.vertex_from_adjacency(adjacency)
                agenda.append(vertex)

            if len(agenda) != 0:
                # Ordenar la agenda usando la heurística
                agenda.sort(
                    key=lambda v: f(v, curr_v, seek, arg),
                    reverse=reverse,
                )

                # Obtener el valor mínimo de la heurística
                choosen_heuristic = f(agenda[0], curr_v, seek, arg)

                # Filtrar las soluciones con la heurística mínima
                min_solutions = [
                    v for v in agenda if f(v, curr_v, seek, arg) == choosen_heuristic
                ]

                # Elegir una solución
                choosen_index = randint(0, len(min_solutions) - 1)
                choosen_opt = min_solutions[choosen_index]
                agenda.append(choosen_opt)


class NonWeightedGraph(Graph[T, NonWeightedVertex[T]]):
    """
    Grafo no ponderado donde las adyacencias son vértices directamente.

    Hereda de:
        Graph[T, NonWeightedVertex[T]]
    """

    def vertex_from_adjacency(
        self, adjacency: NonWeightedVertex[T]
    ) -> NonWeightedVertex[T]:
        """
        Obtiene el vértice destino desde una adyacencia no ponderada.

        Args:
            adjacency: Vértice adyacente directo

        Returns:
            El mismo vértice de la adyacencia
        """
        return adjacency


class WeightedGraph(Graph[T, tuple[WeightedVertex[T], float]]):
    """
    Grafo ponderado donde las adyacencias son tuplas (vértice, peso).

    Hereda de:
        Graph[T, tuple[WeightedVertex[T], float]]
    """

    def vertex_from_adjacency(
        self, adjacency: tuple[WeightedVertex[T], float]
    ) -> WeightedVertex[T]:
        """
        Obtiene el vértice destino desde una adyacencia ponderada.

        Args:
            adjacency: Tupla (vértice adyacente, peso)

        Returns:
            Componente vértice de la tupla de adyacencia
        """
        vertex, _ = adjacency
        return vertex

    def adj_str(self, adjacency: tuple[WeightedVertex[T], float]) -> str:
        """
        Formatea una adyacencia ponderada como '(valor, peso)'.

        Args:
            adjacency: Tupla (vértice, peso) a formatear

        Returns:
            Cadena formateada con valor del vértice y peso
        """
        vertex, weight = adjacency
        return f"({vertex.value}, {weight})"
