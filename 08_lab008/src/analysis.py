"""
Анализ жадных алгоритмов.

Этот модуль содержит:
1. Сравнение жадного и точного (DP) подходов для задачи о рюкзаке
2. Измерение производительности алгоритмов
3. Визуализацию результатов
4. Анализ корректности жадных алгоритмов
"""

import time
from typing import List, Tuple, Dict, Any
import matplotlib.pyplot as plt
import numpy as np
from greedy_algorithms import (
    interval_scheduling,
    fractional_knapsack,
    huffman_coding,
    huffman_encode,
    huffman_decode,
    coin_change_greedy,
    prim_mst,
    kruskal_mst,
)


# ============================================================================
# ТОЧНОЕ РЕШЕНИЕ ЗАДАЧИ О РЮКЗАКЕ (0-1 Knapsack с динамическим программированием)
# ============================================================================

def knapsack_dp(items: List[Tuple[float, float]],
                capacity: int) -> Tuple[float, List[Tuple[float, float]]]:
    """
    Решает задачу 0-1 рюкзака с помощью динамического программирования.

    Временная сложность: O(n * capacity)
    Пространственная сложность: O(n * capacity)

    Args:
        items: Список кортежей (стоимость, вес).
        capacity: Максимальная грузоподъемность рюкзака.

    Returns:
        Кортеж (максимальная стоимость, список включенных предметов).
    """
    if not items or capacity <= 0:
        return 0.0, []

    n = len(items)
    # dp[i][w] = максимальная стоимость для первых i предметов и вместимости w
    dp = [[0.0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Заполняем таблицу DP
    for i in range(1, n + 1):
        value, weight = items[i - 1]
        for w in range(capacity + 1):
            # Не берем предмет
            dp[i][w] = dp[i - 1][w]

            # Берем предмет, если он помещается
            if weight <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][int(w - weight)] + value)

    # Восстанавливаем решение
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            value, weight = items[i - 1]
            selected.append((value, weight))
            w -= weight

    return dp[n][capacity], selected


# ============================================================================
# ПОЛНЫЙ ПЕРЕБОР (Brute Force) для маленьких входных данных
# ============================================================================

def knapsack_brute_force(items: List[Tuple[float, float]],
                         capacity: float) -> Tuple[float, List[Tuple[float, float]]]:
    """
    Решает задачу 0-1 рюкзака полным перебором (только для маленьких входов).

    Временная сложность: O(2^n)
    Пространственная сложность: O(n)

    Args:
        items: Список кортежей (стоимость, вес).
        capacity: Максимальная грузоподъемность рюкзака.

    Returns:
        Кортеж (максимальная стоимость, список включенных предметов).
    """
    if not items or capacity <= 0:
        return 0.0, []

    n = len(items)
    max_value = 0.0
    best_subset = []

    # Перебираем все подмножества (2^n вариантов)
    for mask in range(1 << n):
        current_value = 0.0
        current_weight = 0.0
        current_items = []

        for i in range(n):
            if mask & (1 << i):
                value, weight = items[i]
                current_value += value
                current_weight += weight
                current_items.append((value, weight))

        # Проверяем, влезает ли это подмножество в рюкзак
        if current_weight <= capacity and current_value > max_value:
            max_value = current_value
            best_subset = current_items

    return max_value, best_subset


# ============================================================================
# СРАВНЕНИЕ ЖАДНОГО И ТОЧНОГО ПОДХОДОВ
# ============================================================================

def compare_knapsack_approaches() -> Dict[str, Any]:
    """
    Сравнивает жадный и точный подходы для задачи о рюкзаке.

    Демонстрирует, что для дискретной задачи 0-1 жадный алгоритм может
    давать неоптимальный результат.

    Returns:
        Словарь с результатами сравнения.
    """
    print("\n" + "=" * 80)
    print("СРАВНЕНИЕ ЖАДНОГО И ТОЧНОГО ПОДХОДОВ ДЛЯ ЗАДАЧИ О РЮКЗАКЕ")
    print("=" * 80)

    # Пример 1: Маленький вход (можно использовать brute force)
    items_1 = [(60, 10), (100, 20), (120, 30)]
    capacity_1 = 50

    print(f"\nПример 1: items={items_1}, capacity={capacity_1}")

    # Жадный подход (по удельной стоимости)
    greedy_value_1, greedy_items_1 = fractional_knapsack(items_1, capacity_1)
    print(f"  Жадный (непрерывный): значение={greedy_value_1:.1f}, предметы={len(greedy_items_1)}")

    # DP подход (точный для 0-1 задачи)
    dp_value_1, dp_items_1 = knapsack_dp(items_1, capacity_1)
    print(f"  DP (точный для 0-1): значение={dp_value_1:.1f}, предметы={len(dp_items_1)}")

    # Brute force
    bf_value_1, bf_items_1 = knapsack_brute_force(items_1, capacity_1)
    print(f"  Brute Force: значение={bf_value_1:.1f}, предметы={len(bf_items_1)}")

    # Пример 2: Классический контрпример для жадного алгоритма
    items_2 = [(10, 10), (1, 1), (1, 1)]
    capacity_2 = 10

    print(f"\nПример 2 (контрпример): items={items_2}, capacity={capacity_2}")

    greedy_value_2, greedy_items_2 = fractional_knapsack(items_2, capacity_2)
    print(f"  Жадный (берет первый предмет): значение={greedy_value_2:.1f}")

    dp_value_2, dp_items_2 = knapsack_dp(items_2, capacity_2)
    print(f"  DP (точный): значение={dp_value_2:.1f}")

    bf_value_2, bf_items_2 = knapsack_brute_force(items_2, capacity_2)
    print(f"  Brute Force: значение={bf_value_2:.1f}")

    # Пример 3: Большой вход для измерения производительности
    items_3 = [(50 + i * 5, 10 + i) for i in range(20)]
    capacity_3 = 100

    print(f"\nПример 3 (большой вход, 20 предметов): capacity={capacity_3}")

    start = time.time()
    greedy_value_3, _ = fractional_knapsack(items_3, capacity_3)
    greedy_time_3 = time.time() - start
    print(f"  Жадный: значение={greedy_value_3:.1f}, время={greedy_time_3:.6f}s")

    start = time.time()
    dp_value_3, _ = knapsack_dp(items_3, capacity_3)
    dp_time_3 = time.time() - start
    print(f"  DP: значение={dp_value_3:.1f}, время={dp_time_3:.6f}s")

    return {
        'example_1': {
            'items': items_1,
            'capacity': capacity_1,
            'greedy': greedy_value_1,
            'dp': dp_value_1,
            'bf': bf_value_1,
        },
        'example_2': {
            'items': items_2,
            'capacity': capacity_2,
            'greedy': greedy_value_2,
            'dp': dp_value_2,
            'bf': bf_value_2,
        },
        'example_3': {
            'items': items_3,
            'capacity': capacity_3,
            'greedy_value': greedy_value_3,
            'greedy_time': greedy_time_3,
            'dp_value': dp_value_3,
            'dp_time': dp_time_3,
        }
    }


# ============================================================================
# ИЗМЕРЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ АЛГОРИТМА ХАФФМАНА
# ============================================================================

def benchmark_huffman(max_size: int = 100000,
                      step: int = 10000) -> Tuple[List[int], List[float]]:
    """
    Измеряет время работы алгоритма Хаффмана на данных разного размера.

    Args:
        max_size: Максимальный размер входного текста.
        step: Шаг увеличения размера.

    Returns:
        Кортеж (список размеров, список времен выполнения).
    """
    print("\n" + "=" * 80)
    print("ИЗМЕРЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ АЛГОРИТМА ХАФФМАНА")
    print("=" * 80)

    sizes = []
    times = []

    # Создаем текст с известным распределением частот
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    frequencies = [100, 60, 40, 30, 25, 20, 15, 12, 10, 8, 7, 6, 5, 5, 4, 4,
                   3, 3, 3, 3, 2, 2, 2, 2, 2, 1]

    for size in range(step, max_size + step, step):
        # Генерируем текст пропорционально частотам
        text = ''.join(
            [letter * (size * freq // 500)
             for letter, freq in zip(alphabet, frequencies)]
        )

        start = time.time()
        codes, root = huffman_coding(text)
        elapsed = time.time() - start

        sizes.append(len(text))
        times.append(elapsed)

        print(f"  Размер: {len(text):7d}, время: {elapsed*1000:8.3f}ms, "
              f"кодов: {len(codes)}")

    return sizes, times


# ============================================================================
# АНАЛИЗ ЗАДАЧИ О МОНЕТАХ
# ============================================================================

def analyze_coin_change() -> None:
    """
    Анализирует задачу о монетах и демонстрирует ограничения жадного алгоритма.
    """
    print("\n" + "=" * 80)
    print("АНАЛИЗ ЗАДАЧИ О МОНЕТАХ")
    print("=" * 80)

    # Пример 1: Стандартная система монет (жадный работает)
    coins_standard = [100, 50, 25, 10, 5, 1]
    amounts = [47, 99, 123, 256]

    print("\nПример 1: Стандартная система монет [1, 5, 10, 25, 50, 100]")
    for amount in amounts:
        count, coins_used = coin_change_greedy(amount, coins_standard)
        print(f"  Сумма {amount:3d}: {count} монет, распределение: {coins_used}")

    # Пример 2: Система, где жадный алгоритм неоптимален
    coins_nonstandard = [1, 3, 4]
    amounts_2 = [6, 12, 15]

    print("\nПример 2: Нестандартная система [1, 3, 4] (жадный может быть неоптимален)")
    for amount in amounts_2:
        count, coins_used = coin_change_greedy(amount, coins_nonstandard)
        print(f"  Сумма {amount:2d}: {count} монет (жадный), "
              f"распределение: {coins_used}")
        print(f"            (Оптимально для {amount}: {amount // 3} × 3 = {amount - amount % 3}, "
              f"остаток {amount % 3})")


# ============================================================================
# АНАЛИЗ ЗАДАЧИ О ВЫБОРЕ ЗАЯВОК
# ============================================================================

def analyze_interval_scheduling() -> None:
    """
    Анализирует задачу о выборе заявок и демонстрирует оптимальность жадного подхода.
    """
    print("\n" + "=" * 80)
    print("АНАЛИЗ ЗАДАЧИ О ВЫБОРЕ ЗАЯВОК (Interval Scheduling)")
    print("=" * 80)

    # Пример 1
    intervals_1 = [(0, 5), (1, 3), (2, 4), (4, 7), (6, 9), (8, 11)]
    print(f"\nПример 1: интервалы = {intervals_1}")
    selected_1 = interval_scheduling(intervals_1)
    print(f"  Выбрано интервалов: {len(selected_1)}")
    print(f"  Интервалы: {selected_1}")

    # Пример 2
    intervals_2 = [(0, 2), (1, 5), (2, 3), (3, 6), (4, 8)]
    print(f"\nПример 2: интервалы = {intervals_2}")
    selected_2 = interval_scheduling(intervals_2)
    print(f"  Выбрано интервалов: {len(selected_2)}")
    print(f"  Интервалы: {selected_2}")


# ============================================================================
# АНАЛИЗ МИНИМАЛЬНОГО ОСТОВНОГО ДЕРЕВА
# ============================================================================

def analyze_mst() -> None:
    """
    Анализирует алгоритмы Прима и Краскала для нахождения MST.
    """
    print("\n" + "=" * 80)
    print("АНАЛИЗ МИНИМАЛЬНОГО ОСТОВНОГО ДЕРЕВА (MST)")
    print("=" * 80)

    # Граф для примера
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 1), ('D', 5)],
        'C': [('A', 2), ('B', 1), ('D', 8)],
        'D': [('B', 5), ('C', 8)]
    }

    print("\nГраф:")
    print("  A--4--B")
    print("  |     |")
    print("  2  1  5")
    print("  |     |")
    print("  C--8--D")

    # Алгоритм Прима
    print("\nАлгоритм Прима (начиная с вершины A):")
    prim_edges, prim_weight = prim_mst(graph, 'A')
    print(f"  Ребра MST: {prim_edges}")
    print(f"  Общий вес: {prim_weight}")

    # Алгоритм Краскала
    print("\nАлгоритм Краскала:")
    vertices = list(graph.keys())
    all_edges = []
    seen = set()
    for v, neighbors in graph.items():
        for u, weight in neighbors:
            edge = tuple(sorted([v, u]))
            if edge not in seen:
                all_edges.append((v, u, weight))
                seen.add(edge)

    kruskal_edges, kruskal_weight = kruskal_mst(vertices, all_edges)
    print(f"  Ребра MST: {kruskal_edges}")
    print(f"  Общий вес: {kruskal_weight}")


# ============================================================================
# ВИЗУАЛИЗАЦИЯ
# ============================================================================

def plot_huffman_performance(sizes: List[int],
                             times: List[float]) -> None:
    """
    Строит график производительности алгоритма Хаффмана.

    Args:
        sizes: Список размеров входных данных.
        times: Список времен выполнения.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, 'b-o', linewidth=2, markersize=8)

    # Добавляем линию O(n log n) для сравнения
    n = np.array(sizes)
    theoretical = n * np.log(n) / (sizes[0] * np.log(sizes[0])) * times[0]
    plt.plot(sizes, theoretical, 'r--', linewidth=2, label='O(n log n)')

    plt.xlabel('Размер входных данных (символы)', fontsize=12)
    plt.ylabel('Время выполнения (секунды)', fontsize=12)
    plt.title('Производительность алгоритма Хаффмана', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig('huffman_performance.png', dpi=150)
    print("\n✓ График сохранен как 'huffman_performance.png'")
    plt.close()


def plot_knapsack_comparison() -> None:
    """
    Строит график сравнения жадного и DP подходов для рюкзака.
    """
    # Сравнение на разных размерах входа
    item_counts = list(range(5, 21, 2))
    greedy_times = []
    dp_times = []

    print("\nИзмерение производительности жадного и DP подходов...")

    for count in item_counts:
        items = [(50 + i * 5, 10 + i) for i in range(count)]
        capacity = 100

        # Жадный
        start = time.time()
        for _ in range(1000):
            fractional_knapsack(items, capacity)
        greedy_times.append((time.time() - start) / 1000)

        # DP
        start = time.time()
        for _ in range(100):
            knapsack_dp(items, capacity)
        dp_times.append((time.time() - start) / 100)

    plt.figure(figsize=(10, 6))
    plt.plot(item_counts, greedy_times, 'g-o', linewidth=2, markersize=8,
             label='Жадный алгоритм')
    plt.plot(item_counts, dp_times, 'b-s', linewidth=2, markersize=8,
             label='DP (точный)')

    plt.xlabel('Количество предметов', fontsize=12)
    plt.ylabel('Время выполнения (секунды)', fontsize=12)
    plt.title('Сравнение жадного и DP подходов для задачи о рюкзаке',
              fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig('knapsack_comparison.png', dpi=150)
    print("✓ График сохранен как 'knapsack_comparison.png'")
    plt.close()


# ============================================================================
# ОСНОВНАЯ ФУНКЦИЯ
# ============================================================================

def main() -> None:
    """Главная функция для запуска анализа."""
    print("\n" + "=" * 80)
    print("АНАЛИЗ ЖАДНЫХ АЛГОРИТМОВ")
    print("=" * 80)

    # 1. Анализ различных алгоритмов
    analyze_interval_scheduling()
    analyze_coin_change()
    analyze_mst()

    # 2. Сравнение подходов для рюкзака
    knapsack_results = compare_knapsack_approaches()

    # 3. Измерение производительности Хаффмана
    sizes, times = benchmark_huffman(max_size=50000, step=5000)

    # 4. Визуализация
    print("\n" + "=" * 80)
    print("СОЗДАНИЕ ГРАФИКОВ")
    print("=" * 80)
    plot_huffman_performance(sizes, times)
    plot_knapsack_comparison()

    print("\n" + "=" * 80)
    print("АНАЛИЗ ЗАВЕРШЕН")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()
