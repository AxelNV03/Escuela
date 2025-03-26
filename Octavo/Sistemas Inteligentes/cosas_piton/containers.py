from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from nodes import DoubleLinkedNode

T = TypeVar("T")


class Container(Generic[T], ABC):
    """
    Interfaz abstracta para contenedores genéricos.

    Define las operaciones básicas que debe implementar cualquier contenedor.

    Methods:
        add(value: T): Agrega un elemento al contenedor.
        get() -> Optional[T]: Obtiene y elimina un elemento del contenedor.
        peek() -> Optional[T]: Devuelve el siguiente elemento sin eliminarlo.
        size() -> int: Devuelve el número de elementos en el contenedor.
        is_empty() -> bool: Indica si el contenedor está vacío.
    """

    @abstractmethod
    def add(self, value: T) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get(self) -> Optional[T]:
        raise NotImplementedError()

    @abstractmethod
    def peek(self) -> Optional[T]:
        raise NotImplementedError()

    @abstractmethod
    def size(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def is_empty(self) -> bool:
        raise NotImplementedError()


class Queue(Generic[T], Container[T]):
    """
    Implementación de una cola (FIFO) utilizando nodos doblemente enlazados.

    Attributes:
        _len (int): Número de elementos en la cola.
        _head (Optional[DoubleLinkedNode[T]]): Nodo inicial de la cola.
        _tail (Optional[DoubleLinkedNode[T]]): Nodo final de la cola.
    """

    def __init__(self) -> None:
        """
        Inicializa una cola vacía.
        """
        self._len: int = 0
        self._head: Optional[DoubleLinkedNode[T]] = None
        self._tail: Optional[DoubleLinkedNode[T]] = None

    def size(self) -> int:
        """
        Devuelve el número de elementos en la cola.

        Returns:
            int: Tamaño de la cola.
        """
        return self._len

    def is_empty(self) -> bool:
        """
        Indica si la cola está vacía.

        Returns:
            bool: True si la cola está vacía, False en caso contrario.
        """
        return self.size() == 0

    def enqueue(self, value: T) -> None:
        """
        Agrega un elemento al final de la cola.

        Args:
            value (T): Valor a agregar.
        """
        new = DoubleLinkedNode[T](value)
        if self.is_empty():
            self._head = new
            self._tail = new
        else:
            assert self._tail is not None
            self._tail.next = new
            new.prev = self._tail
            self._tail = new
        self._len += 1

    def dequeue(self) -> Optional[T]:
        """
        Elimina y devuelve el elemento al inicio de la cola.

        Returns:
            Optional[T]: Valor eliminado, o None si la cola está vacía.
        """
        if self.is_empty():
            return None

        assert self._head is not None
        value = self._head.value

        self._head = self._head.next
        if self._head:
            self._head.prev = None
        else:
            self._tail = None

        self._len -= 1
        return value

    def __str__(self) -> str:
        """
        Representa la cola como una cadena.

        Returns:
            str: Representación de los elementos de la cola.
        """
        values = []
        current = self._head
        while current:
            values.append(str(current.value))
            current = current.next
        return f"Queue[{', '.join(values)}]"

    def add(self, value: T) -> None:
        """
        Alias de enqueue. Agrega un elemento al final de la cola.
        """
        self.enqueue(value)

    def get(self) -> Optional[T]:
        """
        Alias de dequeue. Elimina y devuelve el elemento al inicio de la cola.
        """
        return self.dequeue()

    def peek(self) -> Optional[T]:
        """
        Devuelve el elemento al inicio de la cola sin eliminarlo.

        Returns:
            Optional[T]: Valor del primer elemento, o None si la cola está vacía.
        """
        return self._head.value if self._head else None


class Stack(Generic[T], Container[T]):
    """
    Implementación de una pila (LIFO) utilizando nodos doblemente enlazados.

    Attributes:
        __len (int): Número de elementos en la pila.
        __head (Optional[DoubleLinkedNode[T]]): Nodo en la parte superior de la pila.
    """

    def __init__(self) -> None:
        """
        Inicializa una pila vacía.
        """
        self.__len: int = 0
        self.__head: Optional[DoubleLinkedNode[T]] = None

    def size(self) -> int:
        """
        Devuelve el número de elementos en la pila.

        Returns:
            int: Tamaño de la pila.
        """
        return self.__len

    def is_empty(self) -> bool:
        """
        Indica si la pila está vacía.

        Returns:
            bool: True si la pila está vacía, False en caso contrario.
        """
        return self.__len == 0

    def push(self, value: T) -> None:
        """
        Agrega un elemento a la cima de la pila.

        Args:
            value (T): Valor a agregar.
        """
        new_node = DoubleLinkedNode[T](value, self.__head)
        if self.__head:
            self.__head.prev = new_node
        self.__head = new_node
        self.__len += 1

    def pop(self) -> Optional[T]:
        """
        Elimina y devuelve el elemento en la cima de la pila.

        Returns:
            Optional[T]: Valor eliminado, o None si la pila está vacía.
        """
        if self.is_empty():
            return None

        assert self.__head is not None
        value = self.__head.value
        self.__head = self.__head.next
        if self.__head:
            self.__head.prev = None
        self.__len -= 1
        return value

    def peek(self) -> Optional[T]:
        """
        Devuelve el elemento en la cima de la pila sin eliminarlo.

        Returns:
            Optional[T]: Valor del elemento superior, o None si la pila está vacía.
        """
        return self.__head.value if self.__head else None

    def add(self, value: T) -> None:
        """
        Alias de push. Agrega un elemento a la cima de la pila.
        """
        self.push(value)

    def get(self) -> Optional[T]:
        """
        Alias de pop. Elimina y devuelve el elemento en la cima de la pila.
        """
        return self.pop()

    def __str__(self) -> str:
        """
        Representa la pila como una cadena.

        Returns:
            str: Representación de los elementos de la pila.
        """
        values = []
        current = self.__head
        while current:
            values.append(str(current.value))
            current = current.next
        return f"Stack[{', '.join(values)}]"
