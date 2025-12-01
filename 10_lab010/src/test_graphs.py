"""
Unit-тесты для всех компонентов графов.

Тестирует:
- Представления графов (матрица смежности, список смежности)
- Алгоритмы обхода (BFS, DFS)
- Алгоритмы на графах (Дейкстра, топологическая сортировка)
- Различные типы графов (ориентированные, неориентированные, взвешенные)
"""

import unittest
from graph_representation import AdjacencyMatrixGraph, AdjacencyListGraph
from graph_traversal import GraphTraversal
from shortest_path import ShortestPath, TopologicalSort


class TestAdjacencyMatrixGraph(unittest.TestCase):
    """Тесты для представления графа матрицей смежности."""
    
    def setUp(self):
        """Подготовка к тестам."""
        self.graph = AdjacencyMatrixGraph(5, directed=False, weighted=False)
    
    def test_add_edge(self):
        """Тестирование добавления ребра."""
        self.graph.add_edge(0, 1)
        self.assertTrue(self.graph.has_edge(0, 1))
        self.assertTrue(self.graph.has_edge(1, 0))  # Неориентированный граф
    
    def test_remove_edge(self):
        """Тестирование удаления ребра."""
        self.graph.add_edge(0, 1)
        self.graph.remove_edge(0, 1)
        self.assertFalse(self.graph.has_edge(0, 1))
    
    def test_has_edge(self):
        """Тестирование проверки наличия ребра."""
        self.assertFalse(self.graph.has_edge(0, 1))
        self.graph.add_edge(0, 1)
        self.assertTrue(self.graph.has_edge(0, 1))
    
    def test_get_neighbors(self):
        """Тестирование получения соседей."""
        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 2)
        neighbors = self.graph.get_neighbors(0)
        self.assertIn(1, neighbors)
        self.assertIn(2, neighbors)
        self.assertEqual(len(neighbors), 2)
    
    def test_directed_graph(self):
        """Тестирование ориентированного графа."""
        directed_graph = AdjacencyMatrixGraph(3, directed=True)
        directed_graph.add_edge(0, 1)
        self.assertTrue(directed_graph.has_edge(0, 1))
        self.assertFalse(directed_graph.has_edge(1, 0))
    
    def test_weighted_graph(self):
        """Тестирование взвешенного графа."""
        weighted_graph = AdjacencyMatrixGraph(3, directed=False, weighted=True)
        weighted_graph.add_edge(0, 1, weight=5.0)
        self.assertEqual(weighted_graph.get_weight(0, 1), 5.0)
        self.assertEqual(weighted_graph.get_weight(1, 0), 5.0)


class TestAdjacencyListGraph(unittest.TestCase):
    """Тесты для представления графа списком смежности."""
    
    def setUp(self):
        """Подготовка к тестам."""
        self.graph = AdjacencyListGraph(5, directed=False, weighted=False)
    
    def test_add_edge(self):
        """Тестирование добавления ребра."""
        self.graph.add_edge(0, 1)
        self.assertTrue(self.graph.has_edge(0, 1))
        self.assertTrue(self.graph.has_edge(1, 0))
    
    def test_remove_edge(self):
        """Тестирование удаления ребра."""
        self.graph.add_edge(0, 1)
        self.graph.remove_edge(0, 1)
        self.assertFalse(self.graph.has_edge(0, 1))
    
    def test_has_edge(self):
        """Тестирование проверки наличия ребра."""
        self.assertFalse(self.graph.has_edge(0, 1))
        self.graph.add_edge(0, 1)
        self.assertTrue(self.graph.has_edge(0, 1))
    
    def test_get_neighbors(self):
        """Тестирование получения соседей."""
        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 2)
        neighbors = self.graph.get_neighbors(0)
        self.assertIn(1, neighbors)
        self.assertIn(2, neighbors)
        self.assertEqual(len(neighbors), 2)
    
    def test_directed_graph(self):
        """Тестирование ориентированного графа."""
        directed_graph = AdjacencyListGraph(3, directed=True)
        directed_graph.add_edge(0, 1)
        self.assertTrue(directed_graph.has_edge(0, 1))
        self.assertFalse(directed_graph.has_edge(1, 0))
    
    def test_weighted_graph(self):
        """Тестирование взвешенного графа."""
        weighted_graph = AdjacencyListGraph(3, directed=False, weighted=True)
        weighted_graph.add_edge(0, 1, weight=5.0)
        self.assertEqual(weighted_graph.get_weight(0, 1), 5.0)
        self.assertEqual(weighted_graph.get_weight(1, 0), 5.0)


class TestBFS(unittest.TestCase):
    """Тесты для алгоритма BFS."""
    
    def setUp(self):
        """Подготовка графа для тестов."""
        self.graph = AdjacencyListGraph(6)
        # Граф: 0-1-2
        #       |   |
        #       3-4-5
        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 3)
        self.graph.add_edge(1, 2)
        self.graph.add_edge(1, 4)
        self.graph.add_edge(2, 5)
        self.graph.add_edge(3, 4)
        self.graph.add_edge(4, 5)
    
    def test_bfs_distances(self):
        """Тестирование расстояний BFS."""
        distances, _ = GraphTraversal.bfs(self.graph, 0)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 1)
        self.assertEqual(distances[3], 1)
        self.assertEqual(distances[2], 2)
    
    def test_bfs_shortest_path(self):
        """Тестирование поиска кратчайшего пути BFS."""
        path = GraphTraversal.bfs_shortest_path(self.graph, 0, 5)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 0)
        self.assertEqual(path[-1], 5)
        self.assertEqual(len(path), 4)  # Минимальная длина пути
    
    def test_bfs_same_vertex(self):
        """Тестирование пути к самой себе."""
        path = GraphTraversal.bfs_shortest_path(self.graph, 0, 0)
        self.assertEqual(path, [0])
    
    def test_bfs_no_path(self):
        """Тестирование отсутствия пути."""
        disconnected_graph = AdjacencyListGraph(3)
        disconnected_graph.add_edge(0, 1)
        path = GraphTraversal.bfs_shortest_path(disconnected_graph, 0, 2)
        self.assertIsNone(path)


class TestDFS(unittest.TestCase):
    """Тесты для алгоритма DFS."""
    
    def setUp(self):
        """Подготовка графа для тестов."""
        self.graph = AdjacencyListGraph(4)
        self.graph.add_edge(0, 1)
        self.graph.add_edge(0, 2)
        self.graph.add_edge(1, 3)
    
    def test_dfs_recursive(self):
        """Тестирование рекурсивного DFS."""
        visited_order, _ = GraphTraversal.dfs_recursive(self.graph, 0)
        self.assertEqual(visited_order[0], 0)
        self.assertIn(1, visited_order)
        self.assertIn(2, visited_order)
        self.assertIn(3, visited_order)
    
    def test_dfs_iterative(self):
        """Тестирование итеративного DFS."""
        visited_order, _ = GraphTraversal.dfs_iterative(self.graph, 0)
        self.assertEqual(visited_order[0], 0)
        self.assertIn(1, visited_order)
        self.assertIn(2, visited_order)
        self.assertIn(3, visited_order)
    
    def test_dfs_all_vertices_visited(self):
        """Тестирование посещения всех вершин."""
        visited_order, _ = GraphTraversal.dfs_recursive(self.graph, 0)
        self.assertEqual(len(visited_order), 4)


class TestConnectedComponents(unittest.TestCase):
    """Тесты для поиска компонент связности."""
    
    def test_single_component(self):
        """Тестирование графа с одной компонентой."""
        graph = AdjacencyListGraph(4)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        
        components = GraphTraversal.find_connected_components(graph)
        self.assertEqual(len(components), 1)
    
    def test_multiple_components(self):
        """Тестирование графа с несколькими компонентами."""
        graph = AdjacencyListGraph(6)
        graph.add_edge(0, 1)
        graph.add_edge(2, 3)
        graph.add_edge(4, 5)
        
        components = GraphTraversal.find_connected_components(graph)
        self.assertEqual(len(components), 3)
    
    def test_isolated_vertices(self):
        """Тестирование изолированных вершин."""
        graph = AdjacencyListGraph(3)
        components = GraphTraversal.find_connected_components(graph)
        self.assertEqual(len(components), 3)


class TestDijkstra(unittest.TestCase):
    """Тесты для алгоритма Дейкстры."""
    
    def setUp(self):
        """Подготовка взвешенного графа."""
        self.graph = AdjacencyListGraph(5, weighted=True)
        # Простой граф с весами
        self.graph.add_edge(0, 1, 4)
        self.graph.add_edge(0, 2, 1)
        self.graph.add_edge(2, 1, 2)
        self.graph.add_edge(1, 3, 1)
        self.graph.add_edge(2, 3, 5)
        self.graph.add_edge(3, 4, 3)
    
    def test_dijkstra_distances(self):
        """Тестирование расстояний Дейкстры."""
        distances, _ = ShortestPath.dijkstra(self.graph, 0)
        self.assertEqual(distances[0], 0)
        self.assertEqual(distances[1], 3)  # 0->2->1
        self.assertEqual(distances[2], 1)  # 0->2
        self.assertEqual(distances[3], 4)  # 0->2->1->3
    
    def test_dijkstra_shortest_path(self):
        """Тестирование поиска кратчайшего пути."""
        path = ShortestPath.dijkstra_shortest_path(self.graph, 0, 3)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], 0)
        self.assertEqual(path[-1], 3)
    
    def test_dijkstra_unreachable(self):
        """Тестирование недостижимой вершины."""
        disconnected = AdjacencyListGraph(3, weighted=True)
        disconnected.add_edge(0, 1, 1)
        distances, _ = ShortestPath.dijkstra(disconnected, 0)
        self.assertEqual(distances[2], float('inf'))


class TestTopologicalSort(unittest.TestCase):
    """Тесты для топологической сортировки."""
    
    def setUp(self):
        """Подготовка DAG для тестов."""
        self.dag = AdjacencyListGraph(6, directed=True)
        # Граф зависимостей задач:
        # 0 -> 1 -> 3
        # 0 -> 2 -> 3 -> 4
        #           |
        #           5
        self.dag.add_edge(0, 1)
        self.dag.add_edge(0, 2)
        self.dag.add_edge(1, 3)
        self.dag.add_edge(2, 3)
        self.dag.add_edge(3, 4)
        self.dag.add_edge(3, 5)
    
    def test_topological_sort_dfs(self):
        """Тестирование DFS-сортировки."""
        result = TopologicalSort.topological_sort_dfs(self.dag)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        
        # Проверяем порядок: 0 должна быть перед 1 и 2
        self.assertLess(result.index(0), result.index(1))
        self.assertLess(result.index(0), result.index(2))
    
    def test_topological_sort_kahn(self):
        """Тестирование сортировки Кана."""
        result = TopologicalSort.topological_sort_kahn(self.dag)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
    
    def test_cycle_detection(self):
        """Тестирование обнаружения цикла."""
        cyclic = AdjacencyListGraph(3, directed=True)
        cyclic.add_edge(0, 1)
        cyclic.add_edge(1, 2)
        cyclic.add_edge(2, 0)  # Цикл
        
        result = TopologicalSort.topological_sort_dfs(cyclic)
        self.assertIsNone(result)  # Должен вернуть None при наличии цикла


class TestCycleDetection(unittest.TestCase):
    """Тесты для обнаружения циклов."""
    
    def test_cycle_in_undirected_graph(self):
        """Тестирование обнаружения цикла в неориентированном графе."""
        graph = AdjacencyListGraph(4)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 1)  # Цикл 1-2-3
        
        cycle = GraphTraversal.find_cycle_undirected(graph)
        self.assertIsNotNone(cycle)
    
    def test_no_cycle(self):
        """Тестирование графа без цикла."""
        graph = AdjacencyListGraph(4)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        
        cycle = GraphTraversal.find_cycle_undirected(graph)
        self.assertIsNone(cycle)


class TestBipartiteGraph(unittest.TestCase):
    """Тесты для проверки двудольности графа."""
    
    def test_bipartite_graph(self):
        """Тестирование двудольного графа."""
        graph = AdjacencyListGraph(4)
        # 0 - 1
        # |   |
        # 2 - 3
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.add_edge(1, 3)
        graph.add_edge(2, 3)
        
        self.assertTrue(GraphTraversal.is_bipartite(graph))
    
    def test_non_bipartite_graph(self):
        """Тестирование не двудольного графа (треугольник)."""
        graph = AdjacencyListGraph(3)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)  # Нечетный цикл
        
        self.assertFalse(GraphTraversal.is_bipartite(graph))


class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев."""
    
    def test_single_vertex(self):
        """Тестирование графа с одной вершиной."""
        graph = AdjacencyListGraph(1)
        distances, _ = GraphTraversal.bfs(graph, 0)
        self.assertEqual(distances[0], 0)
    
    def test_self_loop(self):
        """Тестирование петли (ребра вершины к себе)."""
        graph = AdjacencyListGraph(2)
        graph.add_edge(0, 0)
        neighbors = graph.get_neighbors(0)
        self.assertIn(0, neighbors)
    
    def test_empty_graph(self):
        """Тестирование пустого графа (без ребер)."""
        graph = AdjacencyListGraph(5)
        components = GraphTraversal.find_connected_components(graph)
        self.assertEqual(len(components), 5)


if __name__ == '__main__':
    unittest.main()
