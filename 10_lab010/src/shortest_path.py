"""
Модуль для алгоритмов поиска кратчайших путей и сортировок в графах.

Реализует:
1. Алгоритм Дейкстры - поиск кратчайших путей в взвешенном графе с неотрицательными весами - O((V+E)logV)
2. Топологическая сортировка - упорядочение вершин DAG - O(V+E)
"""

from typing import Dict, List, Optional, Tuple
from collections import deque
import heapq
from graph_representation import AdjacencyListGraph


class ShortestPath:
    """Класс для алгоритмов поиска кратчайших путей."""
    
    @staticmethod
    def dijkstra(graph: AdjacencyListGraph, start: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]]]:
        """
        Алгоритм Дейкстры для поиска кратчайших путей.
        
        Алгоритм:
        1. Инициализируем расстояния: start=0, остальные=∞
        2. Используем приоритетную очередь (минимальная куча)
        3. Пока очередь не пуста:
           - Извлекаем вершину с минимальным расстоянием
           - Для каждого соседа:
             - Если найден более короткий путь, обновляем расстояние и добавляем в очередь
        
        Сложность: O((V + E) log V) с использованием бинарной кучи
        Память: O(V)
        
        Предусловия:
        - Все веса ребер должны быть неотрицательные
        - Граф должен быть взвешенным
        
        Args:
            graph: Взвешенный граф
            start: Начальная вершина
            
        Returns:
            distances: Словарь кратчайших расстояний от start до каждой вершины
            parents: Словарь родителей для восстановления пути
        """
        distances = {i: float('inf') for i in range(graph.vertices)}  # O(V)
        distances[start] = 0  # O(1)
        parents = {start: None}  # O(1)
        
        pq = [(0, start)]  # O(1)
        visited = set()  # O(1)
        
        while pq:  # O(V log V)
            current_dist, vertex = heapq.heappop(pq)  # O(log V)
            
            if vertex in visited:  # O(1)
                continue  # O(1)
            
            visited.add(vertex)  # O(1)
            
            if current_dist > distances[vertex]:  # O(1)
                continue  # O(1)
            
            for neighbor in graph.get_neighbors(vertex):  # O(degree(v))
                weight = graph.get_weight(vertex, neighbor)  # O(degree(v))
                
                if weight != float('inf'):  # O(1)
                    new_distance = distances[vertex] + weight  # O(1)
                    
                    if new_distance < distances[neighbor]:  # O(1)
                        distances[neighbor] = new_distance  # O(1)
                        parents[neighbor] = vertex  # O(1)
                        heapq.heappush(pq, (new_distance, neighbor))  # O(log V)
        
        return distances, parents  # O(1)
    
    @staticmethod
    def dijkstra_shortest_path(graph: AdjacencyListGraph, start: int, end: int) -> Optional[List[int]]:
        """
        Найти кратчайший путь между двумя вершинами используя алгоритм Дейкстры.
        
        Сложность: O((V + E) log V)
        
        Args:
            graph: Взвешенный граф
            start: Начальная вершина
            end: Конечная вершина
            
        Returns:
            Список вершин кратчайшего пути или None если пути нет
        """
        if start == end:  # O(1)
            return [start]  # O(1)
        
        distances, parents = ShortestPath.dijkstra(graph, start)  # O((V + E) log V)
        
        if distances[end] == float('inf'):  # O(1)
            return None  # O(1)
        
        path = []  # O(1)
        current = end  # O(1)
        while current is not None:  # O(V)
            path.append(current)  # O(1)
            current = parents.get(current)  # O(1)
        
        return path[::-1]  # O(V)
    
    @staticmethod
    @staticmethod
    def dijkstra_all_distances(graph: AdjacencyListGraph, start: int) -> Dict[int, float]:
        """
        Получить кратчайшие расстояния от start до всех вершин.
        
        Args:
            graph: Взвешенный граф
            start: Начальная вершина
            
        Returns:
            Словарь расстояний
        """
        distances, _ = ShortestPath.dijkstra(graph, start)  # O((V + E) log V)
        return distances  # O(1)

class TopologicalSort:
    """Класс для топологической сортировки."""
    
    @staticmethod
    def topological_sort_dfs(graph: AdjacencyListGraph) -> Optional[List[int]]:
        """
        Топологическая сортировка с использованием DFS (алгоритм Кана).
        
        Алгоритм:
        1. Для каждой непосещенной вершины:
           - Рекурсивно посещаем всех соседей
           - После посещения всех соседей добавляем текущую вершину в результат
        2. Результат разворачиваем
        
        Сложность: O(V + E)
        Память: O(V)
        
        Применимость:
        - Работает только для ориентированных ациклических графов (DAG)
        - Возвращает None если граф содержит цикл
        
        Применение:
        - Планирование задач с зависимостями
        - Компиляция с разрешением зависимостей
        - Определение порядка установки пакетов
        
        Args:
            graph: Ориентированный граф (должен быть ациклическим)
            
        Returns:
            Список вершин в топологическом порядке или None если граф содержит цикл
        """
        visited = set()  # O(1)
        rec_stack = set()  # O(1)
        result = []  # O(1)
        
        def dfs(vertex: int) -> bool:  # O(V + E)
            visited.add(vertex)  # O(1)
            rec_stack.add(vertex)  # O(1)
            
            for neighbor in graph.get_neighbors(vertex):  # O(degree(v))
                if neighbor not in visited:  # O(1)
                    if not dfs(neighbor):  # O(V + E)
                        return False  # O(1)
                elif neighbor in rec_stack:  # O(1)
                    return False  # O(1)
            
            rec_stack.remove(vertex)  # O(1)
            result.append(vertex)  # O(1)
            return True  # O(1)
        
        for vertex in range(graph.vertices):  # O(V)
            if vertex not in visited:  # O(1)
                if not dfs(vertex):  # O(V + E)
                    return None  # O(1)
        
        return result[::-1]  # O(V)
    
    @staticmethod
    @staticmethod
    def topological_sort_kahn(graph: AdjacencyListGraph) -> Optional[List[int]]:
        """
        Топологическая сортировка алгоритмом Кана (на основе степени вершин).
        
        Алгоритм:
        1. Вычисляем входящую степень для каждой вершины
        2. Добавляем в очередь все вершины с входящей степенью 0
        3. Пока очередь не пуста:
           - Извлекаем вершину и добавляем в результат
           - Для каждого соседа:
             - Уменьшаем входящую степень
             - Если степень стала 0, добавляем в очередь
        4. Если результат содержит все вершины - граф ациклический, иначе содержит цикл
        
        Сложность: O(V + E)
        Память: O(V)
        
        Args:
            graph: Ориентированный граф
            
        Returns:
            Список вершин в топологическом порядке или None если граф содержит цикл
        """
        in_degree = [0] * graph.vertices  # O(V)
        
        for v in range(graph.vertices):  # O(V)
            for neighbor in graph.get_neighbors(v):  # O(degree(v))
                in_degree[neighbor] += 1  # O(1)
        
        queue = deque([v for v in range(graph.vertices) if in_degree[v] == 0])  # O(V)
        result = []  # O(1)
        
        while queue:  # O(V)
            vertex = queue.popleft()  # O(1)
            result.append(vertex)  # O(1)
            
            for neighbor in graph.get_neighbors(vertex):  # O(degree(v))
                in_degree[neighbor] -= 1  # O(1)
                if in_degree[neighbor] == 0:  # O(1)
                    queue.append(neighbor)  # O(1)
        
        if len(result) == graph.vertices:  # O(1)
            return result  # O(1)
        else:  # O(1)
            return None  # O(1)
    
    @staticmethod
    def detect_cycle_directed(graph: AdjacencyListGraph) -> Optional[List[int]]:
        """
        Обнаружить цикл в ориентированном графе и вернуть вершины цикла.
        
        Алгоритм: DFS с отслеживанием рекурсивного стека
        
        Сложность: O(V + E)
        
        Args:
            graph: Ориентированный граф
            
        Returns:
            Список вершин цикла или None если цикла нет
        """
        visited = set()  # O(1)
        rec_stack = set()  # O(1)
        parent = {}  # O(1)
        
        def dfs(vertex: int) -> Optional[List[int]]:  # O(V + E)
            visited.add(vertex)  # O(1)
            rec_stack.add(vertex)  # O(1)
            
            for neighbor in graph.get_neighbors(vertex):  # O(degree(v))
                if neighbor not in visited:  # O(1)
                    parent[neighbor] = vertex  # O(1)
                    result = dfs(neighbor)  # O(V + E)
                    if result:  # O(1)
                        return result  # O(1)
                elif neighbor in rec_stack:  # O(1)
                    cycle = [neighbor]  # O(1)
                    current = vertex  # O(1)
                    while current != neighbor:  # O(V)
                        cycle.append(current)  # O(1)
                        current = parent[current]  # O(1)
                    return cycle  # O(1)
            
            rec_stack.remove(vertex)  # O(1)
            return None  # O(1)
        
        for vertex in range(graph.vertices):  # O(V)
            if vertex not in visited:  # O(1)
                result = dfs(vertex)  # O(V + E)
                if result:  # O(1)
                    return result  # O(1)
        
        return None  # O(1)