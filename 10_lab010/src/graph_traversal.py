"""
Модуль для алгоритмов обхода графов.

Реализует основные алгоритмы поиска в графах:
1. BFS (поиск в ширину) - O(V + E)
2. DFS (поиск в глубину) - рекурсивный и итеративный - O(V + E)
"""

from typing import Dict, List, Tuple, Set, Optional
from collections import deque
from graph_representation import AdjacencyListGraph


class GraphTraversal:
    """Класс для алгоритмов обхода графов."""
    
    @staticmethod
    def bfs(graph: AdjacencyListGraph, start: int) -> Tuple[Dict[int, int], Dict[int, Optional[int]]]:
        """
        Поиск в ширину (BFS) - Breadth-First Search.
        
        Алгоритм:
        1. Инициализируем очередь с начальной вершиной
        2. Помечаем начальную вершину как посещенную на расстояние 0
        3. Пока очередь не пуста:
           - Извлекаем вершину из начала очереди
           - Для каждого соседа:
             - Если не посещен, добавляем в очередь и помечаем расстояние
        
        Сложность: O(V + E)
        Память: O(V)
        
        Args:
            graph: Граф для обхода
            start: Начальная вершина
            
        Returns:
            distances: Словарь расстояний от start до каждой вершины
            parents: Словарь родителей для восстановления пути
        """
        distances = {start: 0}  # O(1)
        parents = {start: None}  # O(1)
        queue = deque([start])  # O(1)
        
        while queue:  # O(V)
            vertex = queue.popleft()  # O(1)
            
            for neighbor in graph.get_neighbors(vertex):  # O(degree(v))
                if neighbor not in distances:  # O(1)
                    distances[neighbor] = distances[vertex] + 1  # O(1)
                    parents[neighbor] = vertex  # O(1)
                    queue.append(neighbor)  # O(1)
        
        return distances, parents  # O(1)
    
    @staticmethod
    def bfs_shortest_path(graph: AdjacencyListGraph, start: int, end: int) -> Optional[List[int]]:
        """
        Найти кратчайший путь между двумя вершинами используя BFS.
        
        Сложность: O(V + E)
        
        Args:
            graph: Граф для поиска
            start: Начальная вершина
            end: Конечная вершина
            
        Returns:
            Список вершин пути или None если пути нет
        """
        if start == end:  # O(1)
            return [start]  # O(1)
        
        distances, parents = GraphTraversal.bfs(graph, start)  # O(V + E)
        
        if end not in distances:  # O(1)
            return None  # O(1)
        
        path = []  # O(1)
        current = end  # O(1)
        while current is not None:  # O(V)
            path.append(current)  # O(1)
            current = parents[current]  # O(1)
        
        return path[::-1]  # O(V)
    
    @staticmethod
    @staticmethod
    def dfs_recursive(graph: AdjacencyListGraph, start: int) -> Tuple[List[int], Dict[int, Optional[int]]]:
        """
        Поиск в глубину (DFS) - рекурсивная реализация.
        
        Алгоритм:
        1. Помечаем текущую вершину как посещенную
        2. Для каждого соседа:
           - Если не посещен, рекурсивно вызываем DFS
        
        Сложность: O(V + E)
        Память: O(V) для стека вызовов + O(V) для хранения результатов
        
        Args:
            graph: Граф для обхода
            start: Начальная вершина
            
        Returns:
            visited_order: Порядок посещения вершин
            parents: Словарь родителей для восстановления пути
        """
        visited = set()  # O(1)
        visited_order = []  # O(1)
        parents = {}  # O(1)
        
        def dfs_helper(vertex: int, parent: Optional[int] = None):  # O(V + E)
            visited.add(vertex)  # O(1)
            visited_order.append(vertex)  # O(1)
            parents[vertex] = parent  # O(1)
            
            for neighbor in graph.get_neighbors(vertex):  # O(degree(v))
                if neighbor not in visited:  # O(1)
                    dfs_helper(neighbor, vertex)  # O(V + E)
        
        dfs_helper(start)  # O(V + E)
        return visited_order, parents  # O(1)
    @staticmethod
    def dfs_iterative(graph: AdjacencyListGraph, start: int) -> Tuple[List[int], Dict[int, Optional[int]]]:
        """
        Поиск в глубину (DFS) - итеративная реализация с явным стеком.
        
        Алгоритм:
        1. Инициализируем стек с начальной вершиной
        2. Пока стек не пуст:
           - Извлекаем вершину из вершины стека
           - Если не посещена, помечаем как посещенную
           - Добавляем всех непосещенных соседей в стек
        
        Сложность: O(V + E)
        Память: O(V)
        
        Args:
            graph: Граф для обхода
            start: Начальная вершина
            
        Returns:
            visited_order: Порядок посещения вершин
            parents: Словарь родителей для восстановления пути
        """
        visited = set()  # O(1)
        visited_order = []  # O(1)
        parents = {start: None}  # O(1)
        stack = [start]  # O(1)
        
        while stack:  # O(V)
            vertex = stack.pop()  # O(1)
            
            if vertex not in visited:  # O(1)
                visited.add(vertex)  # O(1)
                visited_order.append(vertex)  # O(1)
                
                for neighbor in reversed(graph.get_neighbors(vertex)):  # O(degree(v))
                    if neighbor not in visited:  # O(1)
                        if neighbor not in parents:  # O(1)
                            parents[neighbor] = vertex  # O(1)
                        stack.append(neighbor)  # O(1)
        
        return visited_order, parents  # O(1)
    
    @staticmethod
    @staticmethod
    def find_connected_components(graph: AdjacencyListGraph) -> List[Set[int]]:
        """
        Найти все компоненты связности неориентированного графа.
        
        Алгоритм:
        1. Для каждой непосещенной вершины:
           - Запускаем DFS
           - Собираем все вершины в одной компоненте
        
        Сложность: O(V + E)
        
        Args:
            graph: Неориентированный граф
            
        Returns:
            Список компонент связности (каждая компонента - Set вершин)
        """
        visited = set()  # O(1)
        components = []  # O(1)
        
        def dfs(vertex: int, component: Set[int]):  # O(V + E)
            visited.add(vertex)  # O(1)
            component.add(vertex)  # O(1)
            
            for neighbor in graph.get_neighbors(vertex):  # O(degree(v))
                if neighbor not in visited:  # O(1)
                    dfs(neighbor, component)  # O(V + E)
        
        for vertex in range(graph.vertices):  # O(V)
            if vertex not in visited:  # O(1)
                component = set()  # O(1)
                dfs(vertex, component)  # O(V + E)
                components.append(component)  # O(1)
        
        return components  # O(1)
    @staticmethod
    @staticmethod
    def find_cycle_undirected(graph: AdjacencyListGraph) -> Optional[List[int]]:
        """
        Найти цикл в неориентированном графе.
        
        Алгоритм:
        - DFS с отслеживанием родителя
        - Если встречаем посещенную вершину, которая не родитель - нашли цикл
        
        Сложность: O(V + E)
        
        Args:
            graph: Неориентированный граф
            
        Returns:
            Список вершин цикла или None если цикла нет
        """
        visited = set()  # O(1)
        parent = {}  # O(1)
        cycle = []  # O(1)
        
        def dfs(v: int, p: int = -1) -> bool:  # O(V + E)
            visited.add(v)  # O(1)
            parent[v] = p  # O(1)
            
            for neighbor in graph.get_neighbors(v):  # O(degree(v))
                if neighbor not in visited:  # O(1)
                    if dfs(neighbor, v):  # O(V + E)
                        return True  # O(1)
                elif neighbor != p:  # O(1)
                    cycle_vertex = v  # O(1)
                    while cycle_vertex != neighbor:  # O(V)
                        cycle.append(cycle_vertex)  # O(1)
                        cycle_vertex = parent[cycle_vertex]  # O(1)
                    cycle.append(neighbor)  # O(1)
                    return True  # O(1)
            
            return False  # O(1)
        
        for v in range(graph.vertices):  # O(V)
            if v not in visited:  # O(1)
                if dfs(v):  # O(V + E)
                    return cycle  # O(1)
        
        return None  # O(1)
        
    @staticmethod
    def is_bipartite(graph: AdjacencyListGraph) -> bool:
        """
        Проверить, является ли граф двудольным (раскрашивается в 2 цвета).
        
        Алгоритм:
        - BFS с раскрашиванием вершин в 2 цвета
        - Если при обходе соседа у него уже есть такой же цвет - не двудольный
        
        Сложность: O(V + E)
        
        Args:
            graph: Граф для проверки
            
        Returns:
            True если граф двудольный, False иначе
        """
        color = {-1: None}  # O(1)
        
        def bfs_coloring(start: int) -> bool:  # O(V + E)
            queue = deque([start])  # O(1)
            color[start] = 0  # O(1)
            
            while queue:  # O(V)
                vertex = queue.popleft()  # O(1)
                
                for neighbor in graph.get_neighbors(vertex):  # O(degree(v))
                    if neighbor not in color:  # O(1)
                        color[neighbor] = 1 - color[vertex]  # O(1)
                        queue.append(neighbor)  # O(1)
                    elif color[neighbor] == color[vertex]:  # O(1)
                        return False  # O(1)
            
            return True  # O(1)
        
        for vertex in range(graph.vertices):  # O(V)
            if vertex not in color:  # O(1)
                if not bfs_coloring(vertex):  # O(V + E)
                    return False  # O(1)
        
        return True  # O(1)