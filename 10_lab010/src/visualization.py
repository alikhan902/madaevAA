"""
Модуль для визуализации графов и результатов анализа.

Создает графики масштабируемости и визуализирует структуры графов.
"""

import time
import random
import matplotlib.pyplot as plt
import numpy as np

from graph_representation import AdjacencyListGraph
from graph_traversal import GraphTraversal
from shortest_path import ShortestPath


class GraphVisualizer:
    """Класс для визуализации графов и алгоритмов."""
    
    @staticmethod
    def plot_scalability():
        """
        Построить графики масштабируемости алгоритмов.
        """
        sizes = list(range(100, 2001, 200))
        bfs_times = []
        dfs_times = []
        dijkstra_times = []
        
        print("Сбор данных для графика масштабируемости...")
        
        for size in sizes:
            # Создаем граф со списком смежности
            graph = AdjacencyListGraph(size)
            weighted_graph = AdjacencyListGraph(size, weighted=True)
            
            # Добавляем ребра
            for i in range(size - 1):
                graph.add_edge(i, i + 1)
                weighted_graph.add_edge(i, i + 1, weight=random.uniform(1, 10))
                
                if i % 10 == 0:
                    max_skip = min(10, size - i - 1)
                    if max_skip > 2:
                        neighbor = i + random.randint(2, max_skip)
                        if neighbor < size:
                            graph.add_edge(i, neighbor)
                            weighted_graph.add_edge(i, neighbor, weight=random.uniform(1, 10))
            
            # Измеряем время BFS
            start = time.perf_counter()
            GraphTraversal.bfs(graph, 0)
            bfs_times.append((time.perf_counter() - start) * 1000)  # в мс
            
            # Измеряем время DFS
            start = time.perf_counter()
            GraphTraversal.dfs_iterative(graph, 0)
            dfs_times.append((time.perf_counter() - start) * 1000)
            
            # Измеряем время Dijkstra
            start = time.perf_counter()
            ShortestPath.dijkstra(weighted_graph, 0)
            dijkstra_times.append((time.perf_counter() - start) * 1000)
        
        # Создаем график
        plt.figure(figsize=(12, 6))
        
        plt.plot(sizes, bfs_times, 'b-o', label='BFS O(V+E)', linewidth=2, markersize=6)
        plt.plot(sizes, dfs_times, 'r-s', label='DFS O(V+E)', linewidth=2, markersize=6)
        plt.plot(sizes, dijkstra_times, 'g-^', label='Dijkstra O((V+E)logV)', linewidth=2, markersize=6)
        
        plt.xlabel('Количество вершин', fontsize=12)
        plt.ylabel('Время выполнения (мс)', fontsize=12)
        plt.title('Масштабируемость алгоритмов обхода графов', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('scalability.png', dpi=150)
        print("✓ График масштабируемости сохранен: scalability.png")
        
        return sizes, bfs_times, dfs_times, dijkstra_times
    
    @staticmethod
    def plot_memory_comparison():
        """
        Построить сравнение потребления памяти.
        """
        from graph_representation import AdjacencyMatrixGraph
        
        sizes = list(range(10, 201, 20))
        matrix_memory = []
        list_memory = []
        
        print("Сбор данных для графика памяти...")
        
        for size in sizes:
            # Плотный граф
            matrix_graph = AdjacencyMatrixGraph(size)
            list_graph = AdjacencyListGraph(size)
            
            for i in range(size):
                for j in range(i + 1, min(i + 5, size)):
                    matrix_graph.add_edge(i, j)
                    list_graph.add_edge(i, j)
            
            matrix_memory.append(matrix_graph.get_memory_usage() / 1024)  # KB
            list_memory.append(list_graph.get_memory_usage() / 1024)
        
        # Создаем график
        plt.figure(figsize=(12, 6))
        
        plt.plot(sizes, matrix_memory, 'b-o', label='Матрица смежности O(V²)', linewidth=2, markersize=6)
        plt.plot(sizes, list_memory, 'r-s', label='Список смежности O(V+E)', linewidth=2, markersize=6)
        
        plt.xlabel('Количество вершин', fontsize=12)
        plt.ylabel('Потребление памяти (KB)', fontsize=12)
        plt.title('Сравнение потребления памяти', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('memory_comparison.png', dpi=150)
        print("✓ График памяти сохранен: memory_comparison.png")
    
    @staticmethod
    def plot_complexity_comparison():
        """
        Визуализировать сложность операций для разных представлений.
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # Операции для матрицы смежности
        operations = ['Добавить\nребро', 'Удалить\nребро', 'Проверить\nребро', 'Получить\nсоседей']
        matrix_complexity = [1, 1, 1, 100]  # Условные единицы
        list_complexity = [1, 50, 30, 100]
        
        x = np.arange(len(operations))
        width = 0.35
        
        ax1.bar(x - width/2, matrix_complexity, width, label='Матрица', color='blue', alpha=0.7)
        ax1.bar(x + width/2, list_complexity, width, label='Список', color='red', alpha=0.7)
        ax1.set_ylabel('Относительное время', fontsize=10)
        ax1.set_title('Сложность операций (V=100)', fontsize=11, fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(operations, fontsize=9)
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Потребление памяти
        graph_types = ['Плотный\nграф', 'Средний\nграф', 'Разреженный\nграф']
        matrix_mem = [100, 80, 60]
        list_mem = [20, 15, 8]
        
        x2 = np.arange(len(graph_types))
        ax2.bar(x2 - width/2, matrix_mem, width, label='Матрица', color='blue', alpha=0.7)
        ax2.bar(x2 + width/2, list_mem, width, label='Список', color='red', alpha=0.7)
        ax2.set_ylabel('Потребление памяти (KB)', fontsize=10)
        ax2.set_title('Память для V=100 с разной плотностью', fontsize=11, fontweight='bold')
        ax2.set_xticks(x2)
        ax2.set_xticklabels(graph_types, fontsize=9)
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Алгоритмы обхода
        algo_names = ['BFS', 'DFS Рек.', 'DFS Итер.']
        algo_complexity = [100, 95, 100]
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
        
        ax3.bar(algo_names, algo_complexity, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        ax3.set_ylabel('Время (относительные единицы)', fontsize=10)
        ax3.set_title('Сравнение алгоритмов обхода', fontsize=11, fontweight='bold')
        ax3.set_ylim([0, 120])
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Сложность в Big-O нотации
        algos = ['BFS', 'DFS', 'Dijkstra', 'Топо-\nсортировка', 'Поиск\nцикла']
        complexities = ['O(V+E)', 'O(V+E)', 'O((V+E)\nlogV)', 'O(V+E)', 'O(V+E)']
        
        ax4.axis('off')
        ax4.text(0.5, 0.95, 'Сложность алгоритмов', ha='center', va='top', 
                fontsize=12, fontweight='bold', transform=ax4.transAxes)
        
        y_pos = 0.85
        for algo, complexity in zip(algos, complexities):
            ax4.text(0.1, y_pos, f"• {algo}:", fontsize=10, transform=ax4.transAxes, fontweight='bold')
            ax4.text(0.35, y_pos, complexity, fontsize=10, transform=ax4.transAxes, 
                    family='monospace', color='darkblue')
            y_pos -= 0.15
        
        plt.tight_layout()
        plt.savefig('complexity_comparison.png', dpi=150)
        print("✓ График сложности сохранен: complexity_comparison.png")
    
    @staticmethod
    def draw_simple_graph_example():
        """
        Нарисовать пример простого графа с путем.
        """
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Граф и BFS
        ax = axes[0]
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Граф для BFS', fontsize=12, fontweight='bold')
        
        # Добавляем ноды и ребра
        positions = {0: (1, 4), 1: (1, 2), 2: (3, 4), 3: (3, 2), 4: (3, 0)}
        edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4)]
        
        for v, (x, y) in positions.items():
            circle = plt.Circle((x, y), 0.3, color='lightblue', ec='black', linewidth=2, zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, str(v), ha='center', va='center', fontsize=11, fontweight='bold', zorder=4)
        
        for u, v in edges:
            x1, y1 = positions[u]
            x2, y2 = positions[v]
            ax.arrow(x1, y1 - 0.3, (x2-x1)*0.8, (y2-y1)*0.8, 
                    head_width=0.15, head_length=0.1, fc='black', ec='black', linewidth=1.5, zorder=2)
        
        # Порядок BFS
        bfs_order = "BFS порядок: 0, 1, 2, 3, 4\nРасстояния: [0, 1, 1, 2, 3]"
        ax.text(0.5, -0.5, bfs_order, fontsize=10, family='monospace', 
               bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))
        
        # Взвешенный граф
        ax = axes[1]
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Взвешенный граф для Dijkstra', fontsize=12, fontweight='bold')
        
        weighted_edges = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1), (2, 3, 5), (3, 4, 3)]
        
        for v, (x, y) in positions.items():
            circle = plt.Circle((x, y), 0.3, color='lightgreen', ec='black', linewidth=2, zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, str(v), ha='center', va='center', fontsize=11, fontweight='bold', zorder=4)
        
        for u, v, w in weighted_edges:
            x1, y1 = positions[u]
            x2, y2 = positions[v]
            ax.arrow(x1, y1 - 0.3, (x2-x1)*0.8, (y2-y1)*0.8, 
                    head_width=0.15, head_length=0.1, fc='black', ec='black', linewidth=1.5, zorder=2)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx + 0.2, my + 0.2, str(w), fontsize=10, 
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        dijkstra_info = "Dijkstra из 0:\nРасстояния: [0, 3, 1, 4, 7]\nПуть к 4: 0→2→1→3→4"
        ax.text(0.5, -0.5, dijkstra_info, fontsize=10, family='monospace',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))
        
        # Компоненты связности
        ax = axes[2]
        ax.set_xlim(-1, 5)
        ax.set_ylim(-1, 5)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Компоненты связности', fontsize=12, fontweight='bold')
        
        positions2 = {0: (0.5, 4), 1: (0.5, 2), 2: (1.5, 3),
                     3: (3, 4), 4: (4, 3), 5: (4, 1)}
        edges2 = [(0, 1), (0, 2), (1, 2), (3, 4), (3, 5)]
        
        colors = ['red', 'red', 'red', 'blue', 'blue', 'blue']
        
        for v, (x, y) in positions2.items():
            circle = plt.Circle((x, y), 0.3, color=colors[v], alpha=0.5, 
                              ec='black', linewidth=2, zorder=3)
            ax.add_patch(circle)
            ax.text(x, y, str(v), ha='center', va='center', fontsize=11, fontweight='bold', zorder=4)
        
        for u, v in edges2:
            x1, y1 = positions2[u]
            x2, y2 = positions2[v]
            ax.arrow(x1, y1 - 0.3, (x2-x1)*0.8, (y2-y1)*0.8, 
                    head_width=0.15, head_length=0.1, fc='black', ec='black', linewidth=1.5, zorder=2)
        
        comp_info = "2 компоненты связности:\nКомпонента 1: {0, 1, 2}\nКомпонента 2: {3, 4, 5}"
        ax.text(0.5, -0.5, comp_info, fontsize=10, family='monospace',
               bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.3))
        
        plt.tight_layout()
        plt.savefig('graph_examples.png', dpi=150)
        print("✓ Примеры графов сохранены: graph_examples.png")


def run_visualization():
    """Запустить визуализацию."""
    print("\n" + "=" * 70)
    print("СОЗДАНИЕ ГРАФИКОВ И ВИЗУАЛИЗАЦИЙ")
    print("=" * 70)
    
    GraphVisualizer.plot_scalability()
    GraphVisualizer.plot_memory_comparison()
    GraphVisualizer.plot_complexity_comparison()
    GraphVisualizer.draw_simple_graph_example()
    
    print("\n" + "=" * 70)
    print("✓ Все графики успешно созданы!")
    print("=" * 70)


if __name__ == '__main__':
    run_visualization()
