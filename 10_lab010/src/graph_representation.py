"""
Модуль для представления графов в памяти.

Реализует две основные структуры данных для представления графов:
1. Матрица смежности - O(V²) памяти, быстрая проверка ребра O(1)
2. Список смежности - O(V + E) памяти, эффективный обход соседей O(V+E)
"""

from typing import Dict, List
from collections import defaultdict
import sys


class AdjacencyMatrixGraph:
    """
    Представление графа матрицей смежности.
    
    Сложность операций:
    - Добавление ребра: O(1)
    - Удаление ребра: O(1)
    - Проверка ребра: O(1)
    - Получение соседей: O(V)
    - Память: O(V²)
    
    Преимущества:
    - Быстрая проверка существования ребра
    - Удобно для плотных графов
    
    Недостатки:
    - Много памяти для разреженных графов
    - Медленный обход соседей
    """
    
    def __init__(self, vertices: int, directed: bool = False, weighted: bool = False):
        """
        Инициализация графа матрицей смежности.
        
        Args:
            vertices: Количество вершин
            directed: Ориентированный ли граф
            weighted: Взвешенный ли граф
        """
        self.vertices = vertices
        self.directed = directed
        self.weighted = weighted
        
        # Инициализация матрицы смежности
        if weighted:
            self.matrix = [[float('inf') for _ in range(vertices)] for _ in range(vertices)]
            # Диагональ = 0 (расстояние до самого себя)
            for i in range(vertices):
                self.matrix[i][i] = 0
        else:
            self.matrix = [[False for _ in range(vertices)] for _ in range(vertices)]
        
        self.edge_count = 0
    
    def add_edge(self, u: int, v: int, weight: float = 1) -> None:
        """
        Добавить ребро в граф.
        
        Сложность: O(1)
        
        Args:
            u: Начальная вершина
            v: Конечная вершина
            weight: Вес ребра (для взвешенного графа)
        """
        if u >= self.vertices or v >= self.vertices or u < 0 or v < 0:  # O(1)
            raise ValueError(f"Вершины должны быть в диапазоне [0, {self.vertices-1}]")  # O(1)
        
        if self.weighted:  # O(1)
            self.matrix[u][v] = weight  # O(1)
            if not self.directed:  # O(1)
                self.matrix[v][u] = weight  # O(1)
        else:  # O(1)
            self.matrix[u][v] = True  # O(1)
            if not self.directed:  # O(1)
                self.matrix[v][u] = True  # O(1)
        
        self.edge_count += 1  # O(1)
    
    def remove_edge(self, u: int, v: int) -> None:
        """
        Удалить ребро из графа.
        
        Сложность: O(1)
        
        Args:
            u: Начальная вершина
            v: Конечная вершина
        """
        if u >= self.vertices or v >= self.vertices or u < 0 or v < 0:  # O(1)
            raise ValueError(f"Вершины должны быть в диапазоне [0, {self.vertices-1}]")  # O(1)
        
        if self.weighted:  # O(1)
            if self.matrix[u][v] != float('inf'):  # O(1)
                self.matrix[u][v] = float('inf')  # O(1)
                if not self.directed:  # O(1)
                    self.matrix[v][u] = float('inf')  # O(1)
                self.edge_count -= 1  # O(1)
        else:  # O(1)
            if self.matrix[u][v]:  # O(1)
                self.matrix[u][v] = False  # O(1)
                if not self.directed:  # O(1)
                    self.matrix[v][u] = False  # O(1)
                self.edge_count -= 1  # O(1)
    
    def has_edge(self, u: int, v: int) -> bool:
        """
        Проверить наличие ребра.
        
        Сложность: O(1)
        
        Args:
            u: Начальная вершина
            v: Конечная вершина
            
        Returns:
            True если ребро существует, False иначе
        """
        if u >= self.vertices or v >= self.vertices or u < 0 or v < 0:  # O(1)
            return False  # O(1)
        
        if self.weighted:  # O(1)
            return self.matrix[u][v] != float('inf')  # O(1)
        return self.matrix[u][v]  # O(1)
    
    def get_neighbors(self, vertex: int) -> List[int]:
        """
        Получить всех соседей вершины.
        
        Сложность: O(V)
        
        Args:
            vertex: Индекс вершины
            
        Returns:
            Список соседей вершины
        """
        if vertex >= self.vertices or vertex < 0:  # O(1)
            raise ValueError(f"Вершина должна быть в диапазоне [0, {self.vertices-1}]")  # O(1)
        
        neighbors = []  # O(1)
        for i in range(self.vertices):  # O(V)
            if self.weighted:  # O(1)
                if self.matrix[vertex][i] != float('inf') and i != vertex:  # O(1)
                    neighbors.append(i)  # O(1)
            else:  # O(1)
                if self.matrix[vertex][i]:  # O(1)
                    neighbors.append(i)  # O(1)
        return neighbors  # O(1)
    
    def get_weight(self, u: int, v: int) -> float:
        """
        Получить вес ребра.
        
        Args:
            u: Начальная вершина
            v: Конечная вершина
            
        Returns:
            Вес ребра или inf если ребра нет
        """
        if self.weighted:  # O(1)
            return self.matrix[u][v]  # O(1)
        return 1 if self.has_edge(u, v) else float('inf')  # O(1)
    
    def get_memory_usage(self) -> int:
        """
        Получить приблизительное потребление памяти в байтах.
        
        Returns:
            Размер памяти в байтах
        """
        # Матрица хранится как список списков
        # Каждый элемент занимает ~28 байт (ссылка на объект) + сам объект
        element_size = sys.getsizeof(True) if not self.weighted else sys.getsizeof(1.0)
        return sys.getsizeof(self.matrix) + self.vertices**2 * element_size


class AdjacencyListGraph:
    """
    Представление графа списком смежности.
    
    Сложность операций:
    - Добавление ребра: O(1)
    - Удаление ребра: O(E) в худшем случае
    - Проверка ребра: O(degree(v))
    - Получение соседей: O(degree(v))
    - Память: O(V + E)
    
    Преимущества:
    - Экономная память для разреженных графов
    - Эффективный обход соседей
    
    Недостатки:
    - Медленная проверка существования ребра
    - Более сложная реализация
    """
    
    def __init__(self, vertices: int, directed: bool = False, weighted: bool = False):
        """
        Инициализация графа списком смежности.
        
        Args:
            vertices: Количество вершин
            directed: Ориентированный ли граф
            weighted: Взвешенный ли граф
        """
        self.vertices = vertices
        self.directed = directed
        self.weighted = weighted
        
        # Список смежности: вершина -> список соседей (или (сосед, вес))
        self.adjacency_list: Dict[int, List] = defaultdict(list)
        self.edge_count = 0
    
    def add_edge(self, u: int, v: int, weight: float = 1) -> None:
        """
        Добавить ребро в граф.
        
        Сложность: O(1)
        
        Args:
            u: Начальная вершина
            v: Конечная вершина
            weight: Вес ребра (для взвешенного графа)
        """
        if u >= self.vertices or v >= self.vertices or u < 0 or v < 0:  # O(1)
            raise ValueError(f"Вершины должны быть в диапазоне [0, {self.vertices-1}]")  # O(1)
        
        if self.weighted:  # O(1)
            self.adjacency_list[u].append((v, weight))  # O(1)
            if not self.directed:  # O(1)
                self.adjacency_list[v].append((u, weight))  # O(1)
        else:  # O(1)
            self.adjacency_list[u].append(v)  # O(1)
            if not self.directed:  # O(1)
                self.adjacency_list[v].append(u)  # O(1)
        
        self.edge_count += 1  # O(1)
    
    def remove_edge(self, u: int, v: int) -> None:
        """
        Удалить ребро из графа.
        
        Сложность: O(E) в худшем случае
        
        Args:
            u: Начальная вершина
            v: Конечная вершина
        """
        if u >= self.vertices or v >= self.vertices or u < 0 or v < 0:  # O(1)
            raise ValueError(f"Вершины должны быть в диапазоне [0, {self.vertices-1}]")  # O(1)
        
        if self.weighted:  # O(1)
            before_len = len(self.adjacency_list[u])  # O(1)
            self.adjacency_list[u] = [(neighbor, w) for neighbor, w in self.adjacency_list[u]   # O(degree(u))
                                      if neighbor != v]
            if not self.directed:  # O(1)
                self.adjacency_list[v] = [(neighbor, w) for neighbor, w in self.adjacency_list[v]   # O(degree(v))
                                          if neighbor != u]
        else:  # O(1)
            before_len = len(self.adjacency_list[u])  # O(1)
            self.adjacency_list[u] = [neighbor for neighbor in self.adjacency_list[u]   # O(degree(u))
                                      if neighbor != v]
            if not self.directed:  # O(1)
                self.adjacency_list[v] = [neighbor for neighbor in self.adjacency_list[v]   # O(degree(v))
                                          if neighbor != u]
        
        if len(self.adjacency_list[u]) < before_len:  # O(1)
            self.edge_count -= 1  # O(1)
    
    def has_edge(self, u: int, v: int) -> bool:
        """
        Проверить наличие ребра.
        
        Сложность: O(degree(u))
        
        Args:
            u: Начальная вершина
            v: Конечная вершина
            
        Returns:
            True если ребро существует, False иначе
        """
        if u >= self.vertices or v >= self.vertices or u < 0 or v < 0:  # O(1)
            return False  # O(1)
        
        if self.weighted:  # O(1)
            return any(neighbor == v for neighbor, _ in self.adjacency_list[u])  # O(degree(u))
        return v in self.adjacency_list[u]  # O(degree(u))
    
    def get_neighbors(self, vertex: int) -> List[int]:
        """
        Получить всех соседей вершины.
        
        Сложность: O(degree(v))
        
        Args:
            vertex: Индекс вершины
            
        Returns:
            Список соседей вершины
        """
        if vertex >= self.vertices or vertex < 0:  # O(1)
            raise ValueError(f"Вершина должна быть в диапазоне [0, {self.vertices-1}]")  # O(1)
        
        if self.weighted:  # O(1)
            return [neighbor for neighbor, _ in self.adjacency_list[vertex]]  # O(degree(v))
        return self.adjacency_list[vertex].copy()  # O(degree(v))
    
    def get_weight(self, u: int, v: int) -> float:
        """
        Получить вес ребра.
        
        Args:
            u: Начальная вершина
            v: Конечная вершина
            
        Returns:
            Вес ребра или inf если ребра нет
        """
        if self.weighted:  # O(1)
            for neighbor, weight in self.adjacency_list[u]:  # O(degree(u))
                if neighbor == v:  # O(1)
                    return weight  # O(1)
            return float('inf')  # O(1)
        return 1 if self.has_edge(u, v) else float('inf')  # O(degree(u))
    
    def get_memory_usage(self) -> int:
        """
        Получить приблизительное потребление памяти в байтах.
        
        Returns:
            Размер памяти в байтах
        """
        total = sys.getsizeof(self.adjacency_list)  # O(1)
        for vertex, neighbors in self.adjacency_list.items():  # O(V)
            total += sys.getsizeof(vertex) + sys.getsizeof(neighbors)  # O(1)
            for neighbor in neighbors:  # O(degree(v))
                if isinstance(neighbor, tuple):  # O(1)
                    total += sys.getsizeof(neighbor)  # O(1)
                else:  # O(1)
                    total += sys.getsizeof(neighbor)  # O(1)
        return total  # O(1)
