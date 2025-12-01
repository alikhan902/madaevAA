"""
Практические задачи на графах.

Решены три практические задачи:
1. Поиск кратчайшего пути в лабиринте
2. Определение связности сети
3. Задача на топологическую сортировку
"""

from typing import List, Tuple, Optional
from enum import Enum
from graph_representation import AdjacencyListGraph
from graph_traversal import GraphTraversal
from shortest_path import TopologicalSort


class MazeCell(Enum):
    """Типы ячеек лабиринта."""
    WALL = '#'
    PATH = ' '
    START = 'S'
    END = 'E'


class PracticalProblem1_Maze:
    """
    Практическая задача 1: Поиск кратчайшего пути в лабиринте.
    
    Описание:
    Дан лабиринт в виде двумерной сетки. Нужно найти кратчайший путь от
    стартовой точки до финиша, обходя стены.
    
    Алгоритм:
    1. Преобразуем лабиринт в граф, где вершины - проходимые ячейки
    2. Добавляем ребра между соседними проходимыми ячейками
    3. Используем BFS для поиска кратчайшего пути
    
    Сложность: O(rows * cols)
    Память: O(rows * cols)
    """
    
    @staticmethod
    def solve_maze(maze: List[List[str]]) -> Optional[List[Tuple[int, int]]]:
        """
        Найти кратчайший путь в лабиринте от S до E.
        
        Args:
            maze: Двумерный массив представления лабиринта
                  '#' - стена, ' ' - проход, 'S' - старт, 'E' - финиш
                  
        Returns:
            Список координат пути от старта до финиша или None если пути нет
        """
        rows, cols = len(maze), len(maze[0]) if maze else 0  # O(1)
        start = None  # O(1)
        end = None  # O(1)
        
        for i in range(rows):  # O(rows)
            for j in range(cols):  # O(cols)
                if maze[i][j] == 'S':  # O(1)
                    start = (i, j)  # O(1)
                elif maze[i][j] == 'E':  # O(1)
                    end = (i, j)  # O(1)
        
        if not start or not end:  # O(1)
            return None  # O(1)
        
        coord_to_vertex = {}  # O(1)
        vertex_to_coord = {}  # O(1)
        vertex_count = 0  # O(1)
        
        for i in range(rows):  # O(rows)
            for j in range(cols):  # O(cols)
                if maze[i][j] != '#':  # O(1)
                    coord_to_vertex[(i, j)] = vertex_count  # O(1)
                    vertex_to_coord[vertex_count] = (i, j)  # O(1)
                    vertex_count += 1  # O(1)
        
        if start not in coord_to_vertex or end not in coord_to_vertex:  # O(1)
            return None  # O(1)
        
        graph = AdjacencyListGraph(vertex_count)  # O(1)
        
        for i in range(rows):  # O(rows)
            for j in range(cols):  # O(cols)
                if maze[i][j] != '#':  # O(1)
                    current = coord_to_vertex[(i, j)]  # O(1)
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # O(1)
                        ni, nj = i + di, j + dj  # O(1)
                        if 0 <= ni < rows and 0 <= nj < cols and maze[ni][nj] != '#':  # O(1)
                            neighbor = coord_to_vertex[(ni, nj)]  # O(1)
                            graph.add_edge(current, neighbor)  # O(1)
        
        start_vertex = coord_to_vertex[start]  # O(1)
        end_vertex = coord_to_vertex[end]  # O(1)
        
        path = GraphTraversal.bfs_shortest_path(graph, start_vertex, end_vertex)  # O(V + E)
        
        if path:  # O(1)
            return [vertex_to_coord[v] for v in path]  # O(V)
        return None  # O(1)
    
    @staticmethod
    def print_maze_with_path(maze: List[List[str]], path: Optional[List[Tuple[int, int]]]) -> str:
        """
        Визуализировать лабиринт с найденным путем.
        
        Args:
            maze: Исходный лабиринт
            path: Путь от старта до финиша
            
        Returns:
            Строковое представление лабиринта с путем
        """
        result = [row[:] for row in maze]  # O(rows * cols)
        
        if path:  # O(1)
            for i, (r, c) in enumerate(path):  # O(V)
                if result[r][c] not in ['S', 'E']:  # O(1)
                    result[r][c] = '.'  # O(1)
        
        return '\n'.join(''.join(row) for row in result)  # O(rows * cols)


class PracticalProblem2_NetworkConnectivity:
    """
    Практическая задача 2: Определение связности сети.
    
    Описание:
    Дана сеть компьютеров с имеющимися соединениями между ними.
    Нужно определить:
    1. Является ли сеть связной
    2. Сколько отдельных компонент связности
    3. Какие компьютеры могут общаться между собой
    
    Применение:
    - Проверка связности компьютерной сети
    - Определение групп взаимодействующих узлов
    - Поиск критических узлов для разделения сети
    """
    
    @staticmethod
    def analyze_network(connections: List[Tuple[int, int]], num_nodes: int) -> dict:
        """
        Анализировать связность сети.
        
        Args:
            connections: Список соединений (ребер) между узлами
            num_nodes: Количество узлов в сети
            
        Returns:
            Словарь с информацией о связности сети
        """
        graph = AdjacencyListGraph(num_nodes)  # O(V)
        
        for u, v in connections:  # O(E)
            if 0 <= u < num_nodes and 0 <= v < num_nodes:  # O(1)
                graph.add_edge(u, v)  # O(1)
        
        components = GraphTraversal.find_connected_components(graph)  # O(V + E)
        
        result = {  # O(1)
            'is_connected': len(components) == 1,  # O(1)
            'num_components': len(components),  # O(1)
            'components': [sorted(list(comp)) for comp in components],  # O(V log V)
            'largest_component': max(components, key=len) if components else set(),  # O(V)
            'isolated_nodes': [comp.pop() for comp in components if len(comp) == 1]  # O(V)
        }
        
        return result  # O(1)
    
    @staticmethod
    def find_critical_nodes(connections: List[Tuple[int, int]], num_nodes: int) -> List[int]:
        """
        Найти критические узлы (articulation points) - их удаление разделяет сеть.
        
        Алгоритм:
        1. Для каждого узла v:
           - Создаем граф без этого узла
           - Если количество компонент увеличилось - v критический узел
        
        Сложность: O(V * (V + E))
        
        Args:
            connections: Список соединений между узлами
            num_nodes: Количество узлов
            
        Returns:
            Список критических узлов
        """
        original_graph = AdjacencyListGraph(num_nodes)  # O(V)
        for u, v in connections:  # O(E)
            if 0 <= u < num_nodes and 0 <= v < num_nodes:  # O(1)
                original_graph.add_edge(u, v)  # O(1)
        
        original_components = len(GraphTraversal.find_connected_components(original_graph))  # O(V + E)
        critical_nodes = []  # O(1)
        
        for node in range(num_nodes):  # O(V)
            temp_graph = AdjacencyListGraph(num_nodes)  # O(V)
            for u, v in connections:  # O(E)
                if u != node and v != node and 0 <= u < num_nodes and 0 <= v < num_nodes:  # O(1)
                    temp_graph.add_edge(u, v)  # O(1)
            
            if len(GraphTraversal.find_connected_components(temp_graph)) > original_components:  # O(V + E)
                critical_nodes.append(node)  # O(1)
        
        return critical_nodes  # O(1)
    @staticmethod
    def network_reliability_report(connections: List[Tuple[int, int]], num_nodes: int) -> str:
        """
        Создать отчет о надежности сети.
        
        Args:
            connections: Список соединений
            num_nodes: Количество узлов
            
        Returns:
            Отчет о надежности сети в виде строки
        """
        analysis = PracticalProblem2_NetworkConnectivity.analyze_network(connections, num_nodes)  # O(V + E)
        critical_nodes = PracticalProblem2_NetworkConnectivity.find_critical_nodes(connections, num_nodes)  # O(V(V + E))
        
        report = []  # O(1)
        report.append("=" * 50)  # O(1)
        report.append("ОТЧЕТ О СВЯЗНОСТИ СЕТИ")  # O(1)
        report.append("=" * 50)  # O(1)
        report.append(f"Всего узлов: {num_nodes}")  # O(1)
        report.append(f"Всего соединений: {len(connections)}")  # O(1)
        report.append(f"Сеть связна: {'Да' if analysis['is_connected'] else 'Нет'}")  # O(1)
        report.append(f"Количество компонент: {analysis['num_components']}")  # O(1)
        
        if analysis['isolated_nodes']:  # O(1)
            report.append(f"Изолированные узлы: {analysis['isolated_nodes']}")  # O(1)
        
        if critical_nodes:  # O(1)
            report.append(f"Критические узлы: {critical_nodes}")  # O(1)
        else:  # O(1)
            report.append("Критических узлов не найдено")  # O(1)
        
        report.append("\nКомпоненты связности:")  # O(1)
        for i, comp in enumerate(analysis['components']):  # O(V)
            report.append(f"  Компонента {i+1}: {comp}")  # O(1)
        
        return '\n'.join(report)  # O(V)


class PracticalProblem3_TaskScheduling:
    """
    Практическая задача 3: Планирование задач с зависимостями.
    
    Описание:
    Даны задачи с зависимостями между ними. Нужно определить порядок
    выполнения задач так, чтобы все зависимости были удовлетворены.
    
    Применение:
    - Планирование проектов (метод критического пути)
    - Разрешение зависимостей при установке пакетов
    - Составление расписания с ограничениями
    
    Пример:
    Задачи: A, B, C, D, E
    Зависимости: A->B (B зависит от A), A->C, B->D, C->D, D->E
    Возможный порядок: A, B, C, D, E или A, C, B, D, E
    """

    @staticmethod
    def find_task_order(tasks: List[str], dependencies: List[Tuple[int, int]]) -> Optional[List[str]]:
        """
        Найти порядок выполнения задач при наличии зависимостей.
        
        Args:
            tasks: Список названий задач
            dependencies: Список зависимостей (i -> j означает j зависит от i)
                         Индексы относятся к позициям в списке tasks
            
        Returns:
            Список задач в порядке выполнения или None если есть циклические зависимости
        """
        num_tasks = len(tasks)  # O(1)
        graph = AdjacencyListGraph(num_tasks, directed=True)  # O(V)
        
        for u, v in dependencies:  # O(E)
            if 0 <= u < num_tasks and 0 <= v < num_tasks:  # O(1)
                graph.add_edge(u, v)  # O(1)
        
        order = TopologicalSort.topological_sort_kahn(graph)  # O(V + E)
        
        if order is None:  # O(1)
            return None  # O(1)
        
        return [tasks[i] for i in order]  # O(V)
    
    @staticmethod
    def estimate_project_duration(tasks: List[str], 
                                 task_durations: List[float],
                                 dependencies: List[Tuple[int, int]]) -> Tuple[float, List[int]]:
        """
        Оценить время выполнения проекта (критический путь).
        
        Args:
            tasks: Список названий задач
            task_durations: Длительность каждой задачи
            dependencies: Зависимости между задачами
            
        Returns:
            (общее время проекта, критический путь как список индексов задач)
        """
        num_tasks = len(tasks)  # O(1)
        
        earliest_time = [0.0] * num_tasks  # O(V)
        predecessors = [[] for _ in range(num_tasks)]  # O(V)
        
        for u, v in dependencies:  # O(E)
            if 0 <= u < num_tasks and 0 <= v < num_tasks:  # O(1)
                predecessors[v].append(u)  # O(1)
        
        changed = True  # O(1)
        while changed:  # O(V²) в худшем случае
            changed = False  # O(1)
            for task in range(num_tasks):  # O(V)
                if predecessors[task]:  # O(1)
                    max_pred_time = max(earliest_time[pred] + task_durations[pred]   # O(degree(v))
                                       for pred in predecessors[task])
                    if max_pred_time > earliest_time[task]:  # O(1)
                        earliest_time[task] = max_pred_time  # O(1)
                        changed = True  # O(1)
        
        project_duration = max(earliest_time[i] + task_durations[i]   # O(V)
                              for i in range(num_tasks))
        
        critical_path = []  # O(1)
        for i in range(num_tasks):  # O(V)
            if earliest_time[i] + task_durations[i] == project_duration:  # O(1)
                critical_path.append(i)  # O(1)
        
        return project_duration, critical_path  # O(1)
    
    @staticmethod
    def check_feasibility(num_tasks: int, dependencies: List[Tuple[int, int]]) -> Tuple[bool, Optional[List[int]]]:
        """
        Проверить, является ли список задач с зависимостями выполняемым.
        
        Args:
            num_tasks: Количество задач
            dependencies: Зависимости между задачами
            
        Returns:
            (выполняемо ли, цикл если существует)
        """
        graph = AdjacencyListGraph(num_tasks, directed=True)  # O(V)
        
        for u, v in dependencies:  # O(E)
            if 0 <= u < num_tasks and 0 <= v < num_tasks:  # O(1)
                graph.add_edge(u, v)  # O(1)
        
        cycle = TopologicalSort.detect_cycle_directed(graph)  # O(V + E)
        return cycle is None, cycle  # O(1)


def run_practical_problems():
    """Запустить все практические задачи и вывести результаты."""
    print("=" * 70)
    print("ПРАКТИЧЕСКИЕ ЗАДАЧИ НА ГРАФАХ")
    print("=" * 70)
    
    # ЗАДАЧА 1: ЛАБИРИНТ
    print("\n" + "=" * 70)
    print("ЗАДАЧА 1: Поиск кратчайшего пути в лабиринте")
    print("=" * 70)
    
    maze = [
        ['S', ' ', '#', ' ', ' '],
        ['#', ' ', '#', ' ', '#'],
        [' ', ' ', ' ', ' ', ' '],
        [' ', '#', '#', '#', ' '],
        [' ', ' ', ' ', ' ', 'E']
    ]
    
    print("\nЛабиринт:")
    for row in maze:
        print(''.join(row))
    
    path = PracticalProblem1_Maze.solve_maze(maze)
    
    if path:
        print(f"\nНайден путь длиной {len(path)}:")
        print("Путь:", path)
        print("\nЛабиринт с решением:")
        print(PracticalProblem1_Maze.print_maze_with_path(maze, path))
    else:
        print("\nПути в лабиринте не найдено")
    
    # ЗАДАЧА 2: СВЯЗНОСТЬ СЕТИ
    print("\n" + "=" * 70)
    print("ЗАДАЧА 2: Определение связности сети компьютеров")
    print("=" * 70)
    
    connections = [
        (0, 1), (1, 2), (0, 2),  # Компонента 1
        (3, 4), (4, 5),          # Компонента 2
        (6, 7),                  # Компонента 3
        # Узел 8 изолирован
    ]
    num_nodes = 9
    
    print(PracticalProblem2_NetworkConnectivity.network_reliability_report(connections, num_nodes))
    
    # ЗАДАЧА 3: ПЛАНИРОВАНИЕ ЗАДАЧ
    print("\n" + "=" * 70)
    print("ЗАДАЧА 3: Планирование задач с зависимостями")
    print("=" * 70)
    
    tasks = ['A', 'B', 'C', 'D', 'E', 'F']
    task_durations = [2, 3, 1, 2, 1, 3]  # Длительность каждой задачи
    dependencies = [
        (0, 1),  # A -> B
        (0, 2),  # A -> C
        (1, 3),  # B -> D
        (2, 3),  # C -> D
        (3, 4),  # D -> E
        (4, 5)   # E -> F
    ]
    
    # Проверяем выполняемость
    feasible, cycle = PracticalProblem3_TaskScheduling.check_feasibility(len(tasks), dependencies)
    print(f"\nВыполняемость: {'Да' if feasible else f'Нет (цикл: {cycle})'}")
    
    # Находим порядок выполнения
    order = PracticalProblem3_TaskScheduling.find_task_order(tasks, dependencies)
    if order:
        print(f"Порядок выполнения: {' -> '.join(order)}")
    else:
        print("Порядок выполнения не может быть определен (циклические зависимости)")
    
    # Оцениваем время выполнения проекта
    if feasible:
        duration, critical_path = PracticalProblem3_TaskScheduling.estimate_project_duration(
            tasks, task_durations, dependencies
        )
        print(f"\nОбщее время проекта: {duration}")
        print(f"Критический путь: {' -> '.join([tasks[i] for i in critical_path])}")
        print("(Задачи на критическом пути определяют общую длительность проекта)")


if __name__ == '__main__':
    run_practical_problems()
