from abc import ABC
from typing import Generic, Optional, TypeVar

T = TypeVar("T")
Adjacency = TypeVar("Adjacency")


class Node(Generic[T], ABC):
    """
    Clase base abstracta para representar nodos en estructuras de datos.

    Attributes:
        value (T): El valor almacenado en el nodo.
    """

    def __init__(self, value: T, label: Optional[str] = None) -> None:
        """
        Inicializa un nodo con un valor dado.

        Args:
            value (T): El valor a almacenar en el nodo.
        """
        super().__init__()
        self.value: T = value
        self.label: Optional[str] = label

    def __str__(self) -> str:
        """
        Representa el nodo como una cadena.

        Returns:
            str: Una representación en cadena del nodo.
        """
        return (
            f"({self.value})" if self.label is None else f"({self.label}:{self.value})"
        )


class Vertex(Node[T], Generic[T, Adjacency], ABC):
    """
    Clase base abstracta para vértices en grafos.

    Attributes:
        adjacencies (list[Adjacency]): Lista de adyacencias del vértice.
        lvl (Optional[int]): Nivel del vértice en un recorrido o estructura jerárquica.
        visited (bool): Indica si el vértice ha sido visitado.
    """

    def __init__(
        self,
        value: T,
        lvl: Optional[int] = None,
        adjacencies: Optional[list[Adjacency]] = None,
        label: Optional[str] = None,
    ) -> None:
        """
        Inicializa un vértice con un valor, nivel y lista de adyacencias opcionales.

        Args:
            value (T): El valor almacenado en el vértice.
            lvl (Optional[int]): Nivel del vértice (por defecto, None).
            adjacencies (Optional[list[Adjacency]]): Lista inicial de adyacencias (por defecto, lista vacía).
        """
        super().__init__(value, label)
        self.adjacencies: list[Adjacency] = adjacencies if adjacencies else []
        self.lvl: Optional[int] = lvl
        self.visited: bool = False

    def append(self, *adjacencies: Adjacency) -> None:
        """
        Agrega una o más adyacencias al vértice.

        Args:
            *adjacencies (Adjacency): Adyacencias a agregar.
        """
        self.adjacencies.extend(adjacencies)

    def get(self, index: int) -> Optional[Adjacency]:
        """
        Obtiene la adyacencia en un índice específico.

        Args:
            index (int): Índice de la adyacencia.

        Returns:
            Optional[Adjacency]: La adyacencia en el índice, o None si el índice es inválido.
        """
        try:
            return self.adjacencies[index]
        except IndexError:
            return None

    def __str__(self) -> str:
        """
        Representa el vértice como una cadena.

        Returns:
            str: Una representación en cadena del vértice.
        """
        return (
            f"{{ value: {self.value} lvl: {self.lvl} }}"
            if self.label is None
            else f"{self.label} {{ value: {self.value} lvl: {self.lvl} }}"
        )


class DoubleLinkedNode(Node[T]):
    """
    Nodo que mantiene referencias a los nodos anterior y siguiente.

    Attributes:
        next (Optional[DoubleLinkedNode]): Referencia al siguiente nodo.
        prev (Optional[DoubleLinkedNode]): Referencia al nodo anterior.
    """

    def __init__(
        self,
        value: T,
        next: Optional["DoubleLinkedNode[T]"] = None,
        prev: Optional["DoubleLinkedNode[T]"] = None,
    ) -> None:
        """
        Inicializa un nodo doblemente enlazado.

        Args:
            value (T): El valor almacenado en el nodo.
            next (Optional[DoubleLinkedNode]): Referencia al siguiente nodo (por defecto, None).
            prev (Optional[DoubleLinkedNode]): Referencia al nodo anterior (por defecto, None).
        """
        super().__init__(value)
        self.next: Optional[DoubleLinkedNode[T]] = next
        self.prev: Optional[DoubleLinkedNode[T]] = prev


class NonWeightedVertex(Vertex[T, "NonWeightedVertex[T]"]):
    """
    Vértice para grafos no ponderados.

    Attributes:
        adjacencies (list[NonWeightedVertex[T]]): Lista de vértices adyacentes.
    """

    def __init__(
        self,
        value: T,
        lvl: Optional[int] = None,
        adjacencies: Optional[list["NonWeightedVertex[T]"]] = None,
    ) -> None:
        """
        Inicializa un vértice no ponderado.

        Args:
            value (T): El valor almacenado en el vértice.
            lvl (Optional[int]): Nivel del vértice (por defecto, None).
            adjacencies (Optional[list[NonWeightedVertex[T]]]): Lista inicial de adyacencias (por defecto, lista vacía).
        """
        super().__init__(value, lvl, adjacencies)


class WeightedVertex(Vertex[T, tuple["WeightedVertex[T]", float]]):
    """
    Vértice para grafos ponderados.

    Attributes:
        adjacencies (list[tuple[WeightedVertex[T], float]]): Lista de adyacencias con pesos asociados.
    """

    def __init__(
        self,
        value: T,
        lvl: Optional[int] = None,
        adjacencies: Optional[list[tuple["WeightedVertex[T]", float]]] = None,
    ) -> None:
        """
        Inicializa un vértice ponderado.

        Args:
            value (T): El valor almacenado en el vértice.
            lvl (Optional[int]): Nivel del vértice (por defecto, None).
            adjacencies (Optional[list[tuple[WeightedVertex[T], float]]]): Lista inicial de adyacencias con pesos (por defecto, lista vacía).
        """
        super().__init__(value, lvl, adjacencies)
