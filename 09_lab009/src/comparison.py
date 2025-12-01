"""
Модуль сравнения подходов динамического программирования.

Включает:
1. Сравнение нисходящего (мемоизация) и восходящего подходов для Фибоначчи
2. Сравнение DP с жадным алгоритмом для непрерывного рюкзака
3. Исследование масштабируемости алгоритмов
4. Анализ использования памяти
5. Визуализация результатов
"""

import time
import sys
import psutil
import os
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
from datetime import datetime

from dynamic_programming import (
    Fibonacci,
    KnapsackZeroOne,
    LongestCommonSubsequence,
    EditDistance,
    CoinChange,
    LongestIncreasingSubsequence
)


# ============================================================================
# КЛАСС ДЛЯ ИЗМЕРЕНИЯ ПРОИЗВОДИТЕЛЬНОСТИ
# ============================================================================

class PerformanceMonitor:
    """Класс для мониторинга производительности алгоритмов"""

    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.start_time = None
        self.start_memory = None

    def start(self):
        """Начать мониторинг"""
        self.start_time = time.perf_counter()
        self.start_memory = self.process.memory_info().rss / 1024 / 1024  # MB

    def stop(self) -> Tuple[float, float]:
        """
        Остановить мониторинг.
        
        Returns:
            (время в секундах, использованная память в МБ)
        """
        elapsed_time = time.perf_counter() - self.start_time
        end_memory = self.process.memory_info().rss / 1024 / 1024
        used_memory = end_memory - self.start_memory
        return elapsed_time, max(used_memory, 0)


# ============================================================================
# СРАВНЕНИЕ ПОДХОДОВ ФИБОНАЧЧИ
# ============================================================================

def compare_fibonacci_approaches(max_n: int = 35) -> Dict:
    """
    Сравнить производительность трёх подходов к вычислению Фибоначчи.
    
    Args:
        max_n: максимальный номер Фибоначчи для тестирования
        
    Returns:
        словарь с результатами сравнения
    """
    print("\n" + "="*70)
    print("СРАВНЕНИЕ ПОДХОДОВ: ЧИСЛА ФИБОНАЧЧИ")
    print("="*70)
    
    results = {
        'n': [],
        'naive': [],
        'memoization': [],
        'tabular': []
    }
    
    for n in range(5, max_n + 1, 2):
        print(f"\nТестирование для n = {n}:")
        
        # Наивный подход (только для малых n)
        if n <= 30:
            monitor = PerformanceMonitor()
            monitor.start()
            result_naive = Fibonacci.naive(n)
            time_naive, mem_naive = monitor.stop()
            print(f"  Наивная рекурсия: {time_naive:.6f}s, память: {mem_naive:.2f}MB")
            results['naive'].append(time_naive)
        else:
            print(f"  Наивная рекурсия: слишком медленно (пропущена)")
            results['naive'].append(None)
        
        # Мемоизация (нисходящий подход)
        monitor = PerformanceMonitor()
        monitor.start()
        result_memo = Fibonacci.memoization(n)
        time_memo, mem_memo = monitor.stop()
        print(f"  Мемоизация:       {time_memo:.6f}s, память: {mem_memo:.2f}MB")
        results['memoization'].append(time_memo)
        
        # Табличный подход (восходящий)
        monitor = PerformanceMonitor()
        monitor.start()
        result_tabular = Fibonacci.tabular(n)
        time_tabular, mem_tabular = monitor.stop()
        print(f"  Табличный:        {time_tabular:.6f}s, память: {mem_tabular:.2f}MB")
        results['tabular'].append(time_tabular)
        
        results['n'].append(n)
        
        # Проверка корректности
        assert result_memo == result_tabular, f"Результаты не совпадают для n={n}"
        print(f"  Результат: F({n}) = {result_tabular}")
    
    return results


# ============================================================================
# СРАВНЕНИЕ РЮКЗАКА ДП vs ЖАДНЫЙ АЛГОРИТМ
# ============================================================================

def compare_knapsack_dp_vs_greedy():
    """
    Сравнить результаты DP для 0-1 рюкзака с жадным алгоритмом для непрерывного.
    """
    print("\n" + "="*70)
    print("СРАВНЕНИЕ: ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ vs ЖАДНЫЙ АЛГОРИТМ")
    print("="*70)
    
    # Пример 1: классический случай
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 8
    
    print(f"\nПример 1:")
    print(f"Вес предметов: {weights}")
    print(f"Стоимость:     {values}")
    print(f"Вместимость:   {capacity}")
    
    # DP для 0-1 рюкзака
    dp_value, dp_items = KnapsackZeroOne.solve_with_recovery(weights, values, capacity)
    dp_weight = sum(weights[i] for i in dp_items)
    
    print(f"\nДП (0-1 рюкзак):")
    print(f"  Стоимость: {dp_value}")
    print(f"  Вес: {dp_weight}")
    print(f"  Предметы (индексы): {dp_items}")
    print(f"  Детали: {[(weights[i], values[i]) for i in dp_items]}")
    
    # Жадный алгоритм для непрерывного рюкзака
    # Стратегия: отношение стоимость/вес
    items_by_ratio = sorted(
        enumerate(zip(weights, values)),
        key=lambda x: x[1][1] / x[1][0],
        reverse=True
    )
    
    greedy_value = 0
    greedy_weight = 0
    greedy_items = []
    
    for idx, (w, v) in items_by_ratio:
        if greedy_weight + w <= capacity:
            greedy_items.append(idx)
            greedy_weight += w
            greedy_value += v
    
    print(f"\nЖадный алгоритм (непрерывный рюкзак):")
    print(f"  Стоимость: {greedy_value}")
    print(f"  Вес: {greedy_weight}")
    print(f"  Предметы (индексы): {greedy_items}")
    print(f"  Детали: {[(weights[i], values[i]) for i in greedy_items]}")
    
    print(f"\nВывод: DP дает оптимальное решение {dp_value}, "
          f"жадный алгоритм дает {greedy_value}")
    
    # Пример 2: случай, где жадный не работает
    print("\n" + "-"*70)
    print("\nПример 2 (жадный алгоритм неоптимален):")
    
    weights2 = [10, 20, 30]
    values2 = [60, 100, 120]
    capacity2 = 50
    
    print(f"Вес предметов: {weights2}")
    print(f"Стоимость:     {values2}")
    print(f"Вместимость:   {capacity2}")
    
    # DP решение
    dp_value2, dp_items2 = KnapsackZeroOne.solve_with_recovery(weights2, values2, capacity2)
    dp_weight2 = sum(weights2[i] for i in dp_items2)
    
    print(f"\nДП (0-1 рюкзак):")
    print(f"  Стоимость: {dp_value2}")
    print(f"  Вес: {dp_weight2}")
    print(f"  Предметы: {dp_items2}")
    
    # Жадный для непрерывного
    items_by_ratio2 = sorted(
        enumerate(zip(weights2, values2)),
        key=lambda x: x[1][1] / x[1][0],
        reverse=True
    )
    
    greedy_value2 = 0
    greedy_weight2 = 0
    greedy_items2 = []
    
    for idx, (w, v) in items_by_ratio2:
        if greedy_weight2 + w <= capacity2:
            greedy_items2.append(idx)
            greedy_weight2 += w
            greedy_value2 += v
    
    print(f"\nЖадный алгоритм:")
    print(f"  Стоимость: {greedy_value2}")
    print(f"  Вес: {greedy_weight2}")
    print(f"  Предметы: {greedy_items2}")


# ============================================================================
# ИССЛЕДОВАНИЕ МАСШТАБИРУЕМОСТИ
# ============================================================================

def test_knapsack_scalability():
    """Исследовать масштабируемость алгоритма 0-1 рюкзака"""
    print("\n" + "="*70)
    print("ИССЛЕДОВАНИЕ МАСШТАБИРУЕМОСТИ: KNAPSACK 0-1")
    print("="*70)
    
    results = {
        'n_items': [],
        'capacity': [],
        'time_full': [],
        'time_optimized': [],
        'memory_full': [],
        'memory_optimized': []
    }
    
    test_cases = [
        (10, 50),
        (20, 100),
        (30, 150),
        (40, 200),
        (50, 250),
        (75, 375),
        (100, 500),
    ]
    
    for n_items, capacity in test_cases:
        print(f"\nТест: n_items={n_items}, capacity={capacity}")
        
        # Генерируем случайные данные
        import random
        random.seed(42)
        weights = [random.randint(5, 50) for _ in range(n_items)]
        values = [random.randint(10, 100) for _ in range(n_items)]
        
        # Полный табличный подход O(n*W)
        monitor = PerformanceMonitor()
        monitor.start()
        result_full = KnapsackZeroOne.solve(weights, values, capacity)
        time_full, mem_full = monitor.stop()
        print(f"  Полный подход:    {time_full:.6f}s, память: {mem_full:.2f}MB")
        
        # Оптимизированный подход O(W)
        monitor = PerformanceMonitor()
        monitor.start()
        result_opt = KnapsackZeroOne.solve_optimized(weights, values, capacity)
        time_opt, mem_opt = monitor.stop()
        print(f"  Оптимизированный: {time_opt:.6f}s, память: {mem_opt:.2f}MB")
        
        # Проверка корректности
        assert result_full == result_opt, f"Результаты не совпадают!"
        print(f"  Результат: максимальная стоимость = {result_full}")
        
        results['n_items'].append(n_items)
        results['capacity'].append(capacity)
        results['time_full'].append(time_full)
        results['time_optimized'].append(time_opt)
        results['memory_full'].append(mem_full)
        results['memory_optimized'].append(mem_opt)
    
    return results


# ============================================================================
# СРАВНЕНИЕ РЕДАКЦИОННОГО РАССТОЯНИЯ
# ============================================================================

def test_edit_distance_optimization():
    """Сравнить полный и оптимизированный подходы редакционного расстояния"""
    print("\n" + "="*70)
    print("СРАВНЕНИЕ ПОДХОДОВ: РЕДАКЦИОННОЕ РАССТОЯНИЕ (ЛЕВЕНШТЕЙН)")
    print("="*70)
    
    test_strings = [
        ("kitten", "sitting"),
        ("saturday", "sunday"),
        ("abc", "def"),
        ("pneumonoultramicroscopicsilicovolcanoconiosis", "pneumonoultramicroscopicsilicovoxfuckinconiosis"),
    ]
    
    results = {
        'strings': [],
        'full': [],
        'optimized': []
    }
    
    for s1, s2 in test_strings:
        print(f"\nСравнение '{s1}' и '{s2}':")
        
        # Полный подход
        monitor = PerformanceMonitor()
        monitor.start()
        dist_full = EditDistance.distance(s1, s2)
        time_full, mem_full = monitor.stop()
        print(f"  Полный подход:    расстояние={dist_full}, {time_full:.6f}s, память: {mem_full:.2f}MB")
        
        # Оптимизированный подход
        monitor = PerformanceMonitor()
        monitor.start()
        dist_opt = EditDistance.distance_optimized(s1, s2)
        time_opt, mem_opt = monitor.stop()
        print(f"  Оптимизированный: расстояние={dist_opt}, {time_opt:.6f}s, память: {mem_opt:.2f}MB")
        
        assert dist_full == dist_opt, "Результаты не совпадают!"
        
        results['strings'].append(f"'{s1[:10]}...'-'{s2[:10]}...'")
        results['full'].append(time_full)
        results['optimized'].append(time_opt)
    
    return results


# ============================================================================
# ДРУГИЕ ПРАКТИЧЕСКИЕ ЗАДАЧИ
# ============================================================================

def test_practical_problems():
    """Тестирование практических задач"""
    print("\n" + "="*70)
    print("ПРАКТИЧЕСКИЕ ЗАДАЧИ")
    print("="*70)
    
    # Размен монет
    print("\n1. ЗАДАЧА О РАЗМЕНЕ МОНЕТ")
    print("-" * 40)
    
    coins = [1, 2, 5, 10]
    amount = 27
    
    min_count, used_coins = CoinChange.min_coins_with_coins(coins, amount)
    print(f"Номиналы монет: {coins}")
    print(f"Сумма: {amount}")
    print(f"Минимальное количество монет: {min_count}")
    print(f"Использованные монеты: {used_coins}")
    print(f"Проверка: {sum(used_coins)} = {amount}")
    
    # Количество комбинаций монет
    combinations = CoinChange.count_combinations(coins, amount)
    print(f"Количество способов образить сумму {amount}: {combinations}")
    
    # Наибольшая возрастающая подпоследовательность
    print("\n2. НАИБОЛЬШАЯ ВОЗРАСТАЮЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ (LIS)")
    print("-" * 40)
    
    test_arrays = [
        [10, 9, 2, 5, 3, 7, 101, 18],
        [0, 1, 0, 4, 4, 4, 3, 5, 1],
        [1, 3, 6, 7, 9, 4, 10, 5, 5],
    ]
    
    for arr in test_arrays:
        lis = LongestIncreasingSubsequence.find(arr)
        length = LongestIncreasingSubsequence.length(arr)
        length_opt = LongestIncreasingSubsequence.length_optimized(arr)
        
        print(f"\nМассив: {arr}")
        print(f"LIS: {lis} (длина = {length})")
        print(f"Длина O(n log n): {length_opt}")
        assert length == length_opt, "Результаты не совпадают!"
    
    # LCS
    print("\n3. НАИБОЛЬШАЯ ОБЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ (LCS)")
    print("-" * 40)
    
    pairs = [
        ("abcde", "ace"),
        ("oxcpqrsvwf", "sxyspmqo"),
        ("AGGTAB", "GXTXAYB"),
    ]
    
    for s1, s2 in pairs:
        lcs = LongestCommonSubsequence.find(s1, s2)
        length = LongestCommonSubsequence.length(s1, s2)
        print(f"\nСтроки: '{s1}' и '{s2}'")
        print(f"LCS: '{lcs}' (длина = {length})")


# ============================================================================
# ВИЗУАЛИЗАЦИЯ ТАБЛИЦ ДП
# ============================================================================

def visualize_dp_tables():
    """Визуализировать процесс заполнения таблиц DP"""
    print("\n" + "="*70)
    print("ВИЗУАЛИЗАЦИЯ ТАБЛИЦ ДИНАМИЧЕСКОГО ПРОГРАММИРОВАНИЯ")
    print("="*70)
    
    # LCS таблица
    print("\n1. ТАБЛИЦА LCS")
    print("-" * 40)
    text1, text2 = "AGGTAB", "GXTXAYB"
    
    table = LongestCommonSubsequence.get_table(text1, text2)
    print(f"\nСтроки: '{text1}' и '{text2}'")
    print(f"\nТаблица DP (индексы строк и столбцов):")
    print(f"      {'':>3}", end="")
    for j, c in enumerate(text2):
        print(f"{c:>3}", end="")
    print()
    
    for i, c in enumerate(text1):
        print(f"{c:>3}:", end="")
        for j in range(len(text2) + 1):
            print(f"{table[i][j]:>3}", end="")
        print()
    
    # Редакционное расстояние таблица
    print("\n2. ТАБЛИЦА РЕДАКЦИОННОГО РАССТОЯНИЯ (ЛЕВЕНШТЕЙН)")
    print("-" * 40)
    word1, word2 = "kitten", "sitting"
    
    table = EditDistance.get_table(word1, word2)
    print(f"\nСлова: '{word1}' и '{word2}'")
    print(f"\nТаблица DP:")
    print(f"      {'':>3}", end="")
    for j, c in enumerate(word2):
        print(f"{c:>3}", end="")
    print()
    
    for i, c in enumerate(word1):
        print(f"{c:>3}:", end="")
        for j in range(len(word2) + 1):
            print(f"{table[i][j]:>3}", end="")
        print()


# ============================================================================
# ГРАФИКИ
# ============================================================================

def plot_fibonacci_comparison(results: Dict):
    """Построить график сравнения подходов Фибоначчи"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # График времени
    ax = axes[0]
    ax.plot(results['n'], results['memoization'], 'o-', label='Мемоизация', linewidth=2)
    ax.plot(results['n'], results['tabular'], 's-', label='Табличный подход', linewidth=2)
    
    # Добавить наивный если есть данные
    naive_data = [(n, t) for n, t in zip(results['n'], results['naive']) if t is not None]
    if naive_data:
        ns, ts = zip(*naive_data)
        ax.plot(ns, ts, '^-', label='Наивная рекурсия', linewidth=2)
    
    ax.set_xlabel('n', fontsize=12)
    ax.set_ylabel('Время (секунды)', fontsize=12)
    ax.set_title('Сравнение подходов: Числа Фибоначчи (время)', fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    
    # График памяти (если будет доступна)
    ax = axes[1]
    ax.text(0.5, 0.5, 'Информация о памяти\nиспользуется из системы мониторинга',
            ha='center', va='center', transform=ax.transAxes, fontsize=11)
    ax.set_title('Анализ памяти', fontsize=12, fontweight='bold')
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('c:\\Users\\user\\Desktop\\09_lab009\\fibonacci_comparison.png', dpi=300)
    print("\nГрафик сохранён: fibonacci_comparison.png")
    plt.close()


def plot_knapsack_scalability(results: Dict):
    """Построить график масштабируемости рюкзака"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # График времени
    ax = axes[0]
    x = range(len(results['n_items']))
    width = 0.35
    ax.bar([i - width/2 for i in x], results['time_full'], width, label='Полный подход O(n*W)', alpha=0.8)
    ax.bar([i + width/2 for i in x], results['time_optimized'], width, label='Оптимизированный O(W)', alpha=0.8)
    
    ax.set_xlabel('Размер задачи (n, W)', fontsize=12)
    ax.set_ylabel('Время (секунды)', fontsize=12)
    ax.set_title('Масштабируемость: 0-1 Knapsack (время)', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f"{n},{w}" for n, w in zip(results['n_items'], results['capacity'])], rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # График памяти
    ax = axes[1]
    ax.bar([i - width/2 for i in x], results['memory_full'], width, label='Полный подход', alpha=0.8)
    ax.bar([i + width/2 for i in x], results['memory_optimized'], width, label='Оптимизированный', alpha=0.8)
    
    ax.set_xlabel('Размер задачи (n, W)', fontsize=12)
    ax.set_ylabel('Память (МБ)', fontsize=12)
    ax.set_title('Масштабируемость: 0-1 Knapsack (память)', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([f"{n},{w}" for n, w in zip(results['n_items'], results['capacity'])], rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('c:\\Users\\user\\Desktop\\09_lab009\\knapsack_scalability.png', dpi=300)
    print("График сохранён: knapsack_scalability.png")
    plt.close()


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main():
    """Главная функция для запуска всех тестов"""
    print("=" * 70)
    print("ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ: СРАВНИТЕЛЬНЫЙ АНАЛИЗ")
    print("=" * 70)
    print(f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Сравнение подходов Фибоначчи
    fib_results = compare_fibonacci_approaches()
    
    # Сравнение рюкзака DP vs жадный
    compare_knapsack_dp_vs_greedy()
    
    # Масштабируемость рюкзака
    knapsack_results = test_knapsack_scalability()
    
    # Редакционное расстояние
    edit_results = test_edit_distance_optimization()
    
    # Практические задачи
    test_practical_problems()
    
    # Визуализация таблиц
    visualize_dp_tables()
    
    # Графики
    try:
        plot_fibonacci_comparison(fib_results)
        plot_knapsack_scalability(knapsack_results)
    except Exception as e:
        print(f"\nОшибка при создании графиков: {e}")
    
    print("\n" + "="*70)
    print("ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
    print("="*70)


if __name__ == "__main__":
    main()
