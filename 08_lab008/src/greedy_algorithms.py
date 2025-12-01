"""
Реализация классических жадных алгоритмов.

Жадный алгоритм: алгоритм, который на каждом шаге принимает локально
оптимальное решение в надежде, что итоговое решение будет глобально оптимальным.

Этот модуль содержит реализацию следующих алгоритмов:
1. Задача о выборе заявок (Interval Scheduling)
2. Непрерывный/дробный рюкзак (Fractional Knapsack)
3. Алгоритм Хаффмана (Huffman Coding)
4. Алгоритм Прима для MST (Minimum Spanning Tree)
5. Алгоритм для задачи о монетах (Coin Change)
"""

from typing import List, Tuple, Dict, Optional
import heapq
from collections import defaultdict


# ============================================================================
# 1. ЗАДАЧА О ВЫБОРЕ ЗАЯВОК (Interval Scheduling)
# ============================================================================

def interval_scheduling(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:  # O(n log n)
    """
    Выбирает максимальное количество непересекающихся интервалов.

    Жадная стратегия: сортируем интервалы по времени окончания и выбираем
    следующий интервал, который не пересекается с последним выбранным.

    Временная сложность: O(n log n) из-за сортировки
    Пространственная сложность: O(n)

    Корректность: Жадный выбор оптимален, потому что выбирая интервал,
    который заканчивается раньше всех, мы оставляем больше "места" для
    будущих интервалов. Если существует оптимальное решение с другим первым
    интервалом, мы можем заменить его на наш интервал, не получив худший результат.

    Args:
        intervals: Список кортежей (start, end) представляющих интервалы.

    Returns:
        Список выбранных непересекающихся интервалов.

    Examples:
        >>> interval_scheduling([(0, 5), (1, 3), (2, 4), (4, 7), (6, 9)])
        [(0, 5), (4, 7), (6, 9)]
    """
    if not intervals:
        return []

    # Сортируем по времени окончания
    sorted_intervals = sorted(intervals, key=lambda x: x[1])  # O(n log n)

    selected = [sorted_intervals[0]]

    for start, end in sorted_intervals[1:]:  # O(n) итераций
        # Выбираем интервал, если он не пересекается с последним выбранным
        if start >= selected[-1][1]:
            selected.append((start, end))

    return selected


def interval_scheduling_count(intervals: List[Tuple[int, int]]) -> int:
    """
    Возвращает количество максимального множества непересекающихся интервалов.

    Args:
        intervals: Список кортежей (start, end).

    Returns:
        Количество выбранных интервалов.
    """
    return len(interval_scheduling(intervals))


# ============================================================================
# 2. НЕПРЕРЫВНЫЙ РЮКЗАК (Fractional Knapsack)
# ============================================================================

def fractional_knapsack(  # O(n log n)
    items: List[Tuple[float, float]],
    capacity: float
) -> Tuple[float, List[Tuple[float, float]]]:
    """
    Решает задачу о непрерывном рюкзаке с помощью жадного алгоритма.

    Жадная стратегия: сортируем предметы по удельной стоимости (цена/вес)
    в убывающем порядке и добавляем предметы полностью или частично.

    Временная сложность: O(n log n) из-за сортировки
    Пространственная сложность: O(n)

    Корректность: Жадный выбор оптимален, потому что если мы берем предмет
    с наибольшей удельной стоимостью, любая замена его на другой предмет
    только уменьшит общую стоимость.

    Args:
        items: Список кортежей (стоимость, вес) для каждого предмета.
        capacity: Максимальная грузоподъемность рюкзака.

    Returns:
        Кортеж (общая стоимость, список взятых предметов с их долями).
        Каждый элемент списка: (стоимость_предмета, взятый_вес).

    Examples:
        >>> fractional_knapsack([(100, 5), (50, 10), (30, 2)], 10)
        (210.0, [(100, 5), (50, 5)])
    """
    if not items or capacity <= 0:
        return 0.0, []

    # Создаем список (value_per_weight_ratio, value, weight, original_index)
    items_with_ratio = [
        (value / weight, value, weight, idx)
        for idx, (value, weight) in enumerate(items)
    ]

    # Сортируем по удельной стоимости в убывающем порядке
    items_with_ratio.sort(reverse=True, key=lambda x: x[0])  # O(n log n)

    total_value = 0.0
    remaining_capacity = capacity
    selected_items = []

    for ratio, value, weight, idx in items_with_ratio:  # O(n) итераций
        if remaining_capacity <= 0:
            break

        if weight <= remaining_capacity:
            # Берем весь предмет
            total_value += value
            remaining_capacity -= weight
            selected_items.append((value, weight))
        else:
            # Берем часть предмета
            fraction = remaining_capacity / weight
            total_value += value * fraction
            selected_items.append((value * fraction, remaining_capacity))
            remaining_capacity = 0
            break

    return total_value, selected_items


# ============================================================================
# 3. АЛГОРИТМ ХАФФМАНА (Huffman Coding)
# ============================================================================

class HuffmanNode:
    """Узел дерева Хаффмана."""

    def __init__(self, char: Optional[str] = None, freq: int = 0,
                 left=None, right=None):
        """
        Инициализирует узел Хаффмана.

        Args:
            char: Символ (для листьев).
            freq: Частота символа.
            left: Левый потомок.
            right: Правый потомок.
        """
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        """Сравнение для использования в heapq."""
        return self.freq < other.freq

    def __eq__(self, other):
        """Проверка равенства."""
        if not isinstance(other, HuffmanNode):
            return False
        return self.freq == other.freq


def huffman_coding(text: str) -> Tuple[Dict[str, str], HuffmanNode]:  # O(n log n)
    """
    Строит оптимальный префиксный код Хаффмана для заданного текста.

    Жадная стратегия: многократно выбираем два узла с наименьшими частотами,
    объединяем их в новый узел с суммой частот и возвращаем в очередь.

    Временная сложность: O(n log n), где n - количество уникальных символов
    Пространственная сложность: O(n)

    Корректность: Хаффманов код является оптимальным префиксным кодом.
    Жадный выбор (объединение двух узлов с минимальными частотами) гарантирует,
    что часто встречающиеся символы получают более короткие коды, что
    минимизирует общую длину закодированного сообщения.

    Args:
        text: Текст для кодирования.

    Returns:
        Кортеж (словарь кодов, корень дерева Хаффмана).
        Словарь: {символ: бинарный_код}

    Examples:
        >>> codes, _ = huffman_coding("aaaabbcccd")
        >>> len(codes['a']) <= len(codes['d'])  # 'a' встречается чаще
        True
    """
    if not text:
        return {}, None

    # Подсчитываем частоты символов
    freq_dict = defaultdict(int)
    for char in text:
        freq_dict[char] += 1

    # Если только один уникальный символ
    if len(freq_dict) == 1:
        char = list(freq_dict.keys())[0]
        return {char: '0'}, HuffmanNode(char, freq_dict[char])

    # Создаем приоритетную очередь с узлами для каждого символа
    heap = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]  # O(m)
    heapq.heapify(heap)  # O(m)

    # Строим дерево Хаффмана
    while len(heap) > 1:  # O(m) итераций
        left = heapq.heappop(heap)  # O(log m)
        right = heapq.heappop(heap)  # O(log m)

        # Создаем новый внутренний узел с суммой частот
        parent = HuffmanNode(None, left.freq + right.freq, left, right)  # O(1)
        heapq.heappush(heap, parent)  # O(log m)

    # Корень дерева
    root = heap[0]

    # Генерируем коды для каждого символа
    codes = {}

    def generate_codes(node, code):
        """Рекурсивно генерирует коды."""
        if node is None:
            return

        # Листовой узел
        if node.char is not None:
            codes[node.char] = code if code else '0'
            return

        generate_codes(node.left, code + '0')
        generate_codes(node.right, code + '1')

    generate_codes(root, '')

    return codes, root


def huffman_encode(text: str, codes: Dict[str, str]) -> str:
    """
    Кодирует текст с использованием кодов Хаффмана.

    Args:
        text: Исходный текст.
        codes: Словарь кодов Хаффмана.

    Returns:
        Закодированная строка (последовательность бит).
    """
    return ''.join(codes[char] for char in text)


def huffman_decode(encoded: str, root: HuffmanNode) -> str:
    """
    Декодирует текст с использованием дерева Хаффмана.

    Args:
        encoded: Закодированная строка.
        root: Корень дерева Хаффмана.

    Returns:
        Декодированный текст.
    """
    if not encoded or root is None:
        return ''

    result = []
    current = root

    # Если единственный символ в тексте
    if root.char is not None:
        return root.char * len(encoded)

    for bit in encoded:
        if bit == '0':
            current = current.left
        else:
            current = current.right

        if current.char is not None:
            result.append(current.char)
            current = root

    return ''.join(result)


# ============================================================================
# 4. ЗАДАЧА О МОНЕТАХ (Coin Change)
# ============================================================================

def coin_change_greedy(amount: int,  # O(amount * len(coins))
                       coins: List[int]) -> Tuple[int, List[int]]:
    """
    Решает задачу о выдаче сдачи минимальным количеством монет
    с помощью жадного алгоритма.

    Жадная стратегия: берем монету с наибольшим номиналом, которая не
    превышает остаток, и повторяем процесс.

    Временная сложность: O(n * m), где n - сумма, m - количество номиналов
    Пространственная сложность: O(m)

    ВАЖНО: Жадный алгоритм работает для стандартной системы монет
    (1, 5, 10, 50, 100 и т.д.), но может давать неоптимальный результат
    для произвольных систем монет (например, [1, 3, 4]).

    Корректность для стандартной системы монет объясняется тем, что каждый
    номинал кратен степени 10 или произведению малых чисел, что гарантирует
    оптимальность жадного выбора.

    Args:
        amount: Сумма, которую нужно выдать.
        coins: Список доступных номиналов монет (в убывающем порядке).

    Returns:
        Кортеж (количество монет, список использованных монет).

    Examples:
        >>> coin_change_greedy(47, [50, 25, 10, 5, 1])
        (4, [25, 10, 10, 1, 1])

    Note:
        Для стандартной системы [1, 5, 10, 50, 100] жадный алгоритм оптимален.
        Для системы [1, 3, 4]: amount=6 дает [4, 1, 1] (3 монеты),
        но оптимально [3, 3] (2 монеты).
    """
    if amount <= 0:
        return 0, []

    # Сортируем монеты в убывающем порядке
    sorted_coins = sorted(coins, reverse=True)  # O(m log m)

    result = []  # O(1)
    remaining = amount  # O(1)

    for coin in sorted_coins:  # O(m) итераций
        while remaining >= coin:  # O(amount/coin) итераций
            result.append(coin)
            remaining -= coin

    if remaining > 0:
        # Невозможно выдать точную сумму
        return -1, []

    return len(result), result


# ============================================================================
# 5. АЛГОРИТМ ПРИМА ДЛЯ MST (Minimum Spanning Tree - Prim's Algorithm)
# ============================================================================

def prim_mst(graph: Dict[str, List[Tuple[str, int]]],  # O(E log V)
             start: str) -> Tuple[List[Tuple[str, str, int]], int]:
    """
    Находит минимальное остовное дерево графа с помощью алгоритма Прима.

    Жадная стратегия: начинаем с произвольной вершины и многократно выбираем
    ребро с минимальным весом, которое соединяет вершину в дереве с вершиной
    вне дерева.

    Временная сложность: O(E log V) с использованием приоритетной очереди
    Пространственная сложность: O(V + E)

    Корректность: Жадный выбор оптимален по теореме о срезе графа (Cut Theorem).
    Если мы уже построили часть MST, выбор ребра с минимальным весом,
    пересекающего срез между включенными и невключенными вершинами,
    гарантирует, что это ребро может быть частью какого-либо MST.

    Args:
        graph: Граф представлен как словарь {вершина: [(сосед, вес), ...]}.
        start: Начальная вершина.

    Returns:
        Кортеж (список ребер MST, общий вес дерева).
        Каждое ребро: (вершина1, вершина2, вес).

    Example:
        >>> graph = {
        ...     'A': [('B', 4), ('C', 2)],
        ...     'B': [('A', 4), ('C', 1), ('D', 5)],
        ...     'C': [('A', 2), ('B', 1), ('D', 8)],
        ...     'D': [('B', 5), ('C', 8)]
        ... }
        >>> edges, weight = prim_mst(graph, 'A')
        >>> weight
        7
    """
    vertices = set(graph.keys())

    if start not in vertices:
        return [], 0

    visited = set()
    edges = []
    min_heap = [(0, start, None)]  # (вес, текущая_вершина, предыдущая_вершина)
    total_weight = 0

    while min_heap and len(visited) < len(vertices):  # O(E) итераций
        weight, current, prev = heapq.heappop(min_heap)  # O(log E)

        if current in visited:
            continue

        visited.add(current)

        if prev is not None:
            edges.append((prev, current, weight))
            total_weight += weight

        # Добавляем все ребра к непосещенным соседям
        if current in graph:  # O(1)
            for neighbor, edge_weight in graph[current]:  # O(degree(current))
                if neighbor not in visited:  # O(1)
                    heapq.heappush(min_heap, (edge_weight, neighbor, current))  # O(log E)

    return edges, total_weight


# ============================================================================
# 6. АЛГОРИТМ КРАСКАЛА ДЛЯ MST (Kruskal's Algorithm)
# ============================================================================

class UnionFind:
    """Структура данных для отслеживания связных компонентов (Union-Find)."""

    def __init__(self, elements):
        """
        Инициализирует структуру Union-Find.

        Args:
            elements: Список элементов.
        """
        self.parent = {elem: elem for elem in elements}
        self.rank = {elem: 0 for elem in elements}

    def find(self, x):
        """
        Находит представителя (корень) компонента, содержащего x.

        Временная сложность: O(α(n)) с использованием сжатия пути.
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Сжатие пути
        return self.parent[x]

    def union(self, x, y):
        """
        Объединяет компоненты, содержащие x и y.

        Временная сложность: O(α(n)).

        Returns:
            True, если компоненты были объединены, False если они уже в одном компоненте.
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True


def kruskal_mst(vertices: List[str],  # O(E log E + E*α(V))
                edges: List[Tuple[str, str, int]]) -> Tuple[List[Tuple[str, str, int]], int]:
    """
    Находит минимальное остовное дерево графа с помощью алгоритма Краскала.

    Жадная стратегия: сортируем все ребра по весу и добавляем ребра
    в порядке возрастания веса, если они не создают цикл.

    Временная сложность: O(E log E + E * α(V))
    Пространственная сложность: O(V + E)

    Корректность: Жадный выбор оптимален по теореме о срезе графа.
    Выбирая ребро с минимальным весом, которое не создает цикл,
    мы гарантируем, что это ребро может быть частью какого-либо MST.

    Args:
        vertices: Список всех вершин графа.
        edges: Список всех ребер: (вершина1, вершина2, вес).

    Returns:
        Кортеж (список ребер MST, общий вес дерева).

    Example:
        >>> vertices = ['A', 'B', 'C', 'D']
        >>> edges = [('A', 'B', 4), ('A', 'C', 2), ('B', 'C', 1),
        ...          ('B', 'D', 5), ('C', 'D', 8)]
        >>> mst_edges, weight = kruskal_mst(vertices, edges)
        >>> weight
        7
    """
    if not vertices or not edges:
        return [], 0

    # Сортируем ребра по весу
    sorted_edges = sorted(edges, key=lambda x: x[2])  # O(E log E)

    uf = UnionFind(vertices)  # O(V)
    mst_edges = []  # O(1)
    total_weight = 0  # O(1)

    for u, v, weight in sorted_edges:  # O(E) итераций
        # Добавляем ребро, если оно не создает цикл
        if uf.union(u, v):  # O(α(V)) ≈ O(1)
            mst_edges.append((u, v, weight))
            total_weight += weight

            # Если у нас есть V-1 ребер, MST построен
            if len(mst_edges) == len(vertices) - 1:
                break

    return mst_edges, total_weight


# ============================================================================
# УТИЛИТЫ
# ============================================================================

def print_huffman_tree(node: HuffmanNode, prefix: str = '',
                       is_tail: bool = True) -> None:
    """
    Выводит дерево Хаффмана в текстовом формате.

    Args:
        node: Корень или узел дерева.
        prefix: Префикс для форматирования.
        is_tail: Является ли это последний потомок.
    """
    if node is None:
        return

    print(prefix + ("└── " if is_tail else "├── ") +
          (f"'{node.char}'" if node.char else f"(freq={node.freq})"))

    if node.left is not None or node.right is not None:
        if node.left:
            print_huffman_tree(node.left, prefix + ("    " if is_tail else "│   "), False)
        if node.right:
            print_huffman_tree(node.right, prefix + ("    " if is_tail else "│   "), True)
