"""
Модуль для анализа производительности представлений графов и алгоритмов.

Проводит сравнительный анализ:
1. Матрица смежности vs Список смежности
2. BFS vs DFS
3. Масштабируемость алгоритмов на больших графах
"""

import time
import random
import sys
from typing import Dict, Tuple, Callable
from graph_representation import AdjacencyMatrixGraph, AdjacencyListGraph
from graph_traversal import GraphTraversal
from shortest_path import ShortestPath

# Увеличиваем лимит рекурсии для больших графов
sys.setrecursionlimit(10000)


class PerformanceAnalyzer:
    """Класс для анализа производительности графов и алгоритмов."""
    
    @staticmethod
    def measure_time(func: Callable, *args, **kwargs) -> float:
        """
        Измерить время выполнения функции.
        
        Args:
            func: Функция для измерения
            *args: Позиционные аргументы
            **kwargs: Именованные аргументы
            
        Returns:
            Время выполнения в секундах
        """
        start = time.perf_counter()
        func(*args, **kwargs)
        end = time.perf_counter()
        return end - start
    
    @staticmethod
    def create_dense_graph(num_vertices: int) -> Tuple[AdjacencyMatrixGraph, AdjacencyListGraph]:
        """
        Создать плотный граф (много ребер).
        
        Args:
            num_vertices: Количество вершин
            
        Returns:
            Кортеж (матрица смежности, список смежности)
        """
        matrix_graph = AdjacencyMatrixGraph(num_vertices)
        list_graph = AdjacencyListGraph(num_vertices)
        
        # Добавляем много случайных ребер
        edges_count = int(num_vertices * (num_vertices - 1) / 2 * 0.5)  # 50% возможных ребер
        
        for _ in range(edges_count):
            u = random.randint(0, num_vertices - 1)
            v = random.randint(0, num_vertices - 1)
            if u != v:
                matrix_graph.add_edge(u, v)
                list_graph.add_edge(u, v)
        
        return matrix_graph, list_graph
    
    @staticmethod
    def create_sparse_graph(num_vertices: int) -> Tuple[AdjacencyMatrixGraph, AdjacencyListGraph]:
        """
        Создать разреженный граф (мало ребер).
        
        Args:
            num_vertices: Количество вершин
            
        Returns:
            Кортеж (матрица смежности, список смежности)
        """
        matrix_graph = AdjacencyMatrixGraph(num_vertices)
        list_graph = AdjacencyListGraph(num_vertices)
        
        # Добавляем мало ребер (линейное количество)
        edges_count = num_vertices * 2
        
        for _ in range(edges_count):
            u = random.randint(0, num_vertices - 1)
            v = random.randint(0, num_vertices - 1)
            if u != v and not matrix_graph.has_edge(u, v):
                matrix_graph.add_edge(u, v)
                list_graph.add_edge(u, v)
        
        return matrix_graph, list_graph
    
    @staticmethod
    def benchmark_memory_usage():
        """Сравнить потребление памяти для разных представлений."""
        print("\n" + "=" * 70)
        print("АНАЛИЗ ПОТРЕБЛЕНИЯ ПАМЯТИ")
        print("=" * 70)
        
        sizes = [10, 50, 100, 200, 500]
        
        print("\nПлотный граф (50% ребер):")
        print(f"{'Вершины':<10} {'Матрица (KB)':<15} {'Список (KB)':<15} {'Экономия':<10}")
        print("-" * 50)
        
        for size in sizes:
            matrix_graph, list_graph = PerformanceAnalyzer.create_dense_graph(size)
            matrix_mem = matrix_graph.get_memory_usage() / 1024
            list_mem = list_graph.get_memory_usage() / 1024
            savings = (1 - list_mem / matrix_mem) * 100
            print(f"{size:<10} {matrix_mem:<15.2f} {list_mem:<15.2f} {savings:<10.1f}%")
        
        print("\nРазреженный граф (линейное кол-во ребер):")
        print(f"{'Вершины':<10} {'Матрица (KB)':<15} {'Список (KB)':<15} {'Экономия':<10}")
        print("-" * 50)
        
        for size in sizes:
            matrix_graph, list_graph = PerformanceAnalyzer.create_sparse_graph(size)
            matrix_mem = matrix_graph.get_memory_usage() / 1024
            list_mem = list_graph.get_memory_usage() / 1024
            savings = (1 - list_mem / matrix_mem) * 100
            print(f"{size:<10} {matrix_mem:<15.2f} {list_mem:<15.2f} {savings:<10.1f}%")
    
    @staticmethod
    def benchmark_edge_checking():
        """Сравнить время проверки наличия ребра."""
        print("\n" + "=" * 70)
        print("АНАЛИЗ ОПЕРАЦИИ ПРОВЕРКИ РЕБРА has_edge()")
        print("=" * 70)
        
        sizes = [10, 50, 100, 200, 500]
        
        print("\nДля плотного графа:")
        print(f"{'Вершины':<10} {'Матрица (мкс)':<15} {'Список (мкс)':<15} {'Выигрыш':<10}")
        print("-" * 50)
        
        for size in sizes:
            matrix_graph, list_graph = PerformanceAnalyzer.create_dense_graph(size)
            
            # Выполняем проверку несколько раз
            matrix_time = sum(
                PerformanceAnalyzer.measure_time(matrix_graph.has_edge, 0, random.randint(1, size-1))
                for _ in range(100)
            ) / 100
            
            list_time = sum(
                PerformanceAnalyzer.measure_time(list_graph.has_edge, 0, random.randint(1, size-1))
                for _ in range(100)
            ) / 100
            
            speedup = list_time / matrix_time if matrix_time > 0 else 0
            print(f"{size:<10} {matrix_time*1e6:<15.2f} {list_time*1e6:<15.2f} {speedup:<10.2f}x")
        
        print("\nДля разреженного графа:")
        print(f"{'Вершины':<10} {'Матрица (мкс)':<15} {'Список (мкс)':<15} {'Выигрыш':<10}")
        print("-" * 50)
        
        for size in sizes:
            matrix_graph, list_graph = PerformanceAnalyzer.create_sparse_graph(size)
            
            matrix_time = sum(
                PerformanceAnalyzer.measure_time(matrix_graph.has_edge, 0, random.randint(1, size-1))
                for _ in range(100)
            ) / 100
            
            list_time = sum(
                PerformanceAnalyzer.measure_time(list_graph.has_edge, 0, random.randint(1, size-1))
                for _ in range(100)
            ) / 100
            
            speedup = list_time / matrix_time if matrix_time > 0 else 0
            print(f"{size:<10} {matrix_time*1e6:<15.2f} {list_time*1e6:<15.2f} {speedup:<10.2f}x")
    
    @staticmethod
    def benchmark_traversal():
        """Сравнить время работы BFS и DFS."""
        print("\n" + "=" * 70)
        print("АНАЛИЗ АЛГОРИТМОВ ОБХОДА (BFS vs DFS)")
        print("=" * 70)
        
        sizes = [50, 100, 200, 300]  # Убрали 500 чтобы избежать очень глубокой рекурсии
        
        print(f"\n{'Вершины':<10} {'BFS (мкс)':<15} {'DFS Итер. (мкс)':<15}")
        print("-" * 40)
        
        for size in sizes:
            list_graph = AdjacencyListGraph(size)
            
            # Создаем граф с ребрами
            for i in range(size - 1):
                list_graph.add_edge(i, i + 1)
                if i % 10 == 0:
                    list_graph.add_edge(i, random.randint(0, size - 1))
            
            bfs_time = PerformanceAnalyzer.measure_time(GraphTraversal.bfs, list_graph, 0)
            dfs_iter_time = PerformanceAnalyzer.measure_time(GraphTraversal.dfs_iterative, list_graph, 0)
            
            print(f"{size:<10} {bfs_time*1e6:<15.2f} {dfs_iter_time*1e6:<15.2f}")
    
    @staticmethod
    def benchmark_shortest_path():
        """Сравнить время работы алгоритмов поиска кратчайшего пути."""
        print("\n" + "=" * 70)
        print("АНАЛИЗ ПОИСКА КРАТЧАЙШИХ ПУТЕЙ (BFS vs Dijkstra)")
        print("=" * 70)
        
        sizes = [50, 100, 200, 300]
        
        print(f"\n{'Вершины':<10} {'BFS (мкс)':<15} {'Dijkstra (мкс)':<15} {'Ratio':<10}")
        print("-" * 50)
        
        for size in sizes:
            # Граф без весов для BFS
            unweighted_graph = AdjacencyListGraph(size)
            for i in range(size - 1):
                unweighted_graph.add_edge(i, i + 1)
                if i % 10 == 0 and i + 5 < size:
                    unweighted_graph.add_edge(i, i + 5)
            
            # Взвешенный граф для Dijkstra
            weighted_graph = AdjacencyListGraph(size, weighted=True)
            for i in range(size - 1):
                weighted_graph.add_edge(i, i + 1, weight=random.uniform(0.1, 10))
                if i % 10 == 0 and i + 5 < size:
                    weighted_graph.add_edge(i, i + 5, weight=random.uniform(0.1, 10))
            
            bfs_time = PerformanceAnalyzer.measure_time(
                GraphTraversal.bfs, unweighted_graph, 0
            )
            dijkstra_time = PerformanceAnalyzer.measure_time(
                ShortestPath.dijkstra, weighted_graph, 0
            )
            
            ratio = dijkstra_time / bfs_time if bfs_time > 0 else 0
            print(f"{size:<10} {bfs_time*1e6:<15.2f} {dijkstra_time*1e6:<15.2f} {ratio:<10.2f}x")
    
    @staticmethod
    def generate_scalability_report():
        """Создать отчет о масштабируемости алгоритмов."""
        print("\n" + "=" * 70)
        print("АНАЛИЗ МАСШТАБИРУЕМОСТИ")
        print("=" * 70)
        
        print("\nДля графа со списком смежности:")
        print("Сложность BFS: O(V + E)")
        print("Сложность DFS: O(V + E)")
        print("Сложность Dijkstra: O((V + E) log V)")
        
        sizes = [100, 200, 300, 400]
        
        print(f"\n{'Вершины':<10} {'Ребра':<10} {'BFS (мкс)':<15} {'DFS (мкс)':<15}")
        print("-" * 55)
        
        for size in sizes:
            graph = AdjacencyListGraph(size)
            edges = 0
            
            # Создаем полусвязный граф
            for i in range(size - 1):
                graph.add_edge(i, i + 1)
                edges += 1
                if i % 5 == 0 and i + 5 < size:
                    graph.add_edge(i, i + 5)
                    edges += 1
            
            bfs_time = PerformanceAnalyzer.measure_time(GraphTraversal.bfs, graph, 0)
            dfs_time = PerformanceAnalyzer.measure_time(GraphTraversal.dfs_iterative, graph, 0)
            
            print(f"{size:<10} {edges:<10} {bfs_time*1e6:<15.2f} {dfs_time*1e6:<15.2f}")


class SystemInfo:
    """Класс для получения информации о системе."""
    
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """
        Получить информацию о системе для тестирования.
        
        Returns:
            Словарь с информацией о системе
        """
        import platform
        import psutil
        
        info = {
            'OS': platform.system() + ' ' + platform.release(),
            'Processor': platform.processor(),
            'Python': platform.python_version(),
            'CPU Cores': str(psutil.cpu_count()),
            'Total Memory': f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            'CPU Frequency': f"{psutil.cpu_freq().current:.0f} MHz"
        }
        
        return info
    
    @staticmethod
    def print_system_info():
        """Вывести информацию о системе."""
        try:
            info = SystemInfo.get_system_info()
            print("\n" + "=" * 70)
            print("ХАРАКТЕРИСТИКИ ТЕСТОВОЙ СИСТЕМЫ")
            print("=" * 70)
            for key, value in info.items():
                print(f"{key:<20}: {value}")
        except:
            print("Не удалось получить информацию о системе")


def run_performance_analysis():
    """Запустить полный анализ производительности."""
    SystemInfo.print_system_info()
    PerformanceAnalyzer.benchmark_memory_usage()
    PerformanceAnalyzer.benchmark_edge_checking()
    PerformanceAnalyzer.benchmark_traversal()
    PerformanceAnalyzer.benchmark_shortest_path()
    PerformanceAnalyzer.generate_scalability_report()


if __name__ == '__main__':
    run_performance_analysis()
