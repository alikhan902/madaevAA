"""
Примеры использования и модульные тесты алгоритмов ДП.

Этот файл содержит:
1. Подробные примеры использования каждого алгоритма
2. Юнит-тесты для проверки корректности
3. Демонстрацию различных случаев применения
"""

import unittest
from typing import List
from dynamic_programming import (
    Fibonacci,
    KnapsackZeroOne,
    LongestCommonSubsequence,
    EditDistance,
    CoinChange,
    LongestIncreasingSubsequence,
    print_table
)


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

def example_fibonacci():
    """Примеры вычисления чисел Фибоначчи"""
    print("\n" + "="*70)
    print("ПРИМЕР 1: ЧИСЛА ФИБОНАЧЧИ")
    print("="*70)
    
    n = 10
    print(f"\nВычисление F({n}):")
    
    # Наивный подход
    result_naive = Fibonacci.naive(n)
    print(f"1. Наивная рекурсия: F({n}) = {result_naive}")
    
    # Мемоизация
    result_memo = Fibonacci.memoization(n)
    print(f"2. С мемоизацией:    F({n}) = {result_memo}")
    
    # Табличный подход
    result_tabular = Fibonacci.tabular(n)
    print(f"3. Табличный подход: F({n}) = {result_tabular}")
    
    # Оптимизированный
    result_opt = Fibonacci.tabular_optimized(n)
    print(f"4. Оптимизированный: F({n}) = {result_opt}")
    
    print(f"\nПервые 15 чисел Фибоначчи:")
    fibs = [Fibonacci.tabular(i) for i in range(15)]
    print(fibs)


def example_knapsack():
    """Пример задачи о рюкзаке 0-1"""
    print("\n" + "="*70)
    print("ПРИМЕР 2: ЗАДАЧА О РЮКЗАКЕ 0-1")
    print("="*70)
    
    # Пример 1: классический случай
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 8
    
    print(f"\nДанные:")
    print(f"Предметы: {list(zip(range(len(weights)), weights, values))}")
    print(f"  (индекс: (вес, стоимость))")
    print(f"Вместимость рюкзака: {capacity}")
    
    # Решение только с максимальной стоимостью
    max_value = KnapsackZeroOne.solve(weights, values, capacity)
    print(f"\nМаксимальная стоимость: {max_value}")
    
    # Решение с восстановлением
    max_value, items = KnapsackZeroOne.solve_with_recovery(weights, values, capacity)
    print(f"\nС восстановлением решения:")
    print(f"Максимальная стоимость: {max_value}")
    print(f"Включённые предметы (индексы): {items}")
    print(f"Детали:")
    total_weight = 0
    total_value = 0
    for i in items:
        print(f"  Предмет {i}: вес={weights[i]}, стоимость={values[i]}")
        total_weight += weights[i]
        total_value += values[i]
    print(f"Итого: вес={total_weight}, стоимость={total_value}")
    
    # Пример 2: более сложный случай
    print("\n" + "-"*70)
    print("\nПример 2:")
    weights2 = [6, 3, 4, 2]
    values2 = [30, 14, 16, 9]
    capacity2 = 10
    
    print(f"Предметы: {list(zip(range(len(weights2)), weights2, values2))}")
    print(f"Вместимость: {capacity2}")
    
    max_value2, items2 = KnapsackZeroOne.solve_with_recovery(weights2, values2, capacity2)
    print(f"Максимальная стоимость: {max_value2}")
    print(f"Включённые предметы: {items2}")


def example_lcs():
    """Пример задачи наибольшей общей подпоследовательности"""
    print("\n" + "="*70)
    print("ПРИМЕР 3: НАИБОЛЬШАЯ ОБЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ (LCS)")
    print("="*70)
    
    test_cases = [
        ("abcde", "ace"),
        ("AGGTAB", "GXTXAYB"),
        ("hello", "world"),
    ]
    
    for text1, text2 in test_cases:
        print(f"\nСтроки: '{text1}' и '{text2}'")
        
        # Длина LCS
        length = LongestCommonSubsequence.length(text1, text2)
        print(f"Длина LCS: {length}")
        
        # Сама LCS
        lcs = LongestCommonSubsequence.find(text1, text2)
        print(f"LCS: '{lcs}'")


def example_edit_distance():
    """Пример расстояния Левенштейна"""
    print("\n" + "="*70)
    print("ПРИМЕР 4: РАССТОЯНИЕ ЛЕВЕНШТЕЙНА (EDIT DISTANCE)")
    print("="*70)
    
    test_cases = [
        ("kitten", "sitting"),
        ("saturday", "sunday"),
        ("", "a"),
        ("a", ""),
    ]
    
    for word1, word2 in test_cases:
        print(f"\nПреобразование '{word1}' -> '{word2}':")
        
        distance = EditDistance.distance(word1, word2)
        print(f"Расстояние Левенштейна: {distance}")


def example_coin_change():
    """Пример размена монет"""
    print("\n" + "="*70)
    print("ПРИМЕР 5: РАЗМЕН МОНЕТ")
    print("="*70)
    
    coins = [1, 2, 5, 10]
    amount = 17
    
    print(f"Номиналы монет: {coins}")
    print(f"Целевая сумма: {amount}")
    
    # Минимальное количество монет
    min_count = CoinChange.min_coins(coins, amount)
    print(f"\nМинимальное количество монет: {min_count}")
    
    # С восстановлением
    min_count, used_coins = CoinChange.min_coins_with_coins(coins, amount)
    print(f"Используемые монеты: {used_coins}")
    print(f"Проверка: {' + '.join(map(str, used_coins))} = {sum(used_coins)}")
    
    # Количество способов
    print(f"\nКоличество различных способов образить сумму {amount}:")
    combinations = CoinChange.count_combinations(coins, amount)
    print(f"{combinations} способов")


def example_lis():
    """Пример наибольшей возрастающей подпоследовательности"""
    print("\n" + "="*70)
    print("ПРИМЕР 6: НАИБОЛЬШАЯ ВОЗРАСТАЮЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ (LIS)")
    print("="*70)
    
    test_arrays = [
        [10, 9, 2, 5, 3, 7, 101, 18],
        [0, 1, 0, 4, 4, 4, 3, 5, 1],
        [5, 4, 3, 2, 1],
    ]
    
    for arr in test_arrays:
        print(f"\nМассив: {arr}")
        
        # Длина
        length = LongestIncreasingSubsequence.length(arr)
        print(f"Длина LIS: {length}")
        
        # Сама LIS
        lis = LongestIncreasingSubsequence.find(arr)
        print(f"LIS: {lis}")
        
        # Оптимизированная версия O(n log n)
        length_opt = LongestIncreasingSubsequence.length_optimized(arr)
        print(f"Длина (O(n log n)): {length_opt}")


# ============================================================================
# ЮНИТ-ТЕСТЫ
# ============================================================================

class TestFibonacci(unittest.TestCase):
    """Тесты для вычисления чисел Фибоначчи"""
    
    def test_base_cases(self):
        """Проверка базовых случаев"""
        self.assertEqual(Fibonacci.naive(0), 0)
        self.assertEqual(Fibonacci.naive(1), 1)
        self.assertEqual(Fibonacci.memoization(0), 0)
        self.assertEqual(Fibonacci.memoization(1), 1)
        self.assertEqual(Fibonacci.tabular(0), 0)
        self.assertEqual(Fibonacci.tabular(1), 1)
    
    def test_consistency(self):
        """Проверка, что все подходы дают одинаковый результат"""
        for n in range(2, 20):
            result_naive = Fibonacci.naive(n)
            result_memo = Fibonacci.memoization(n)
            result_tabular = Fibonacci.tabular(n)
            result_opt = Fibonacci.tabular_optimized(n)
            
            self.assertEqual(result_naive, result_memo)
            self.assertEqual(result_memo, result_tabular)
            self.assertEqual(result_tabular, result_opt)
    
    def test_known_values(self):
        """Проверка известных значений"""
        expected = {
            5: 5,
            10: 55,
            15: 610,
            20: 6765
        }
        
        for n, expected_value in expected.items():
            self.assertEqual(Fibonacci.tabular(n), expected_value)


class TestKnapsack(unittest.TestCase):
    """Тесты для задачи о рюкзаке"""
    
    def test_empty_knapsack(self):
        """Тест с нулевой вместимостью"""
        weights = [1, 2, 3]
        values = [1, 2, 3]
        capacity = 0
        
        result = KnapsackZeroOne.solve(weights, values, capacity)
        self.assertEqual(result, 0)
    
    def test_single_item(self):
        """Тест с одним предметом"""
        weights = [5]
        values = [10]
        capacity = 10
        
        result = KnapsackZeroOne.solve(weights, values, capacity)
        self.assertEqual(result, 10)
    
    def test_insufficient_capacity(self):
        """Тест, когда рюкзак слишком мал"""
        weights = [10, 20]
        values = [5, 10]
        capacity = 5
        
        result = KnapsackZeroOne.solve(weights, values, capacity)
        self.assertEqual(result, 0)
    
    def test_consistency_with_recovery(self):
        """Проверка, что решение с восстановлением соответствует обычному"""
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 6]
        capacity = 8
        
        value1 = KnapsackZeroOne.solve(weights, values, capacity)
        value2, items = KnapsackZeroOne.solve_with_recovery(weights, values, capacity)
        
        self.assertEqual(value1, value2)
    
    def test_optimized_consistency(self):
        """Проверка, что оптимизированный подход дает тот же результат"""
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 6]
        capacity = 8
        
        value1 = KnapsackZeroOne.solve(weights, values, capacity)
        value2 = KnapsackZeroOne.solve_optimized(weights, values, capacity)
        
        self.assertEqual(value1, value2)


class TestLCS(unittest.TestCase):
    """Тесты для наибольшей общей подпоследовательности"""
    
    def test_identical_strings(self):
        """Тест с идентичными строками"""
        text = "hello"
        length = LongestCommonSubsequence.length(text, text)
        lcs = LongestCommonSubsequence.find(text, text)
        
        self.assertEqual(length, len(text))
        self.assertEqual(lcs, text)
    
    def test_empty_strings(self):
        """Тест с пустыми строками"""
        length = LongestCommonSubsequence.length("", "")
        lcs = LongestCommonSubsequence.find("", "")
        
        self.assertEqual(length, 0)
        self.assertEqual(lcs, "")
    
    def test_no_common_subsequence(self):
        """Тест без общей подпоследовательности"""
        length = LongestCommonSubsequence.length("abc", "def")
        lcs = LongestCommonSubsequence.find("abc", "def")
        
        self.assertEqual(length, 0)
        self.assertEqual(lcs, "")
    
    def test_known_cases(self):
        """Тест с известными случаями"""
        test_cases = [
            ("abcde", "ace", "ace"),
            ("AGGTAB", "GXTXAYB", "GTAB"),
        ]
        
        for text1, text2, expected_lcs in test_cases:
            lcs = LongestCommonSubsequence.find(text1, text2)
            self.assertEqual(lcs, expected_lcs)


class TestEditDistance(unittest.TestCase):
    """Тесты для расстояния Левенштейна"""
    
    def test_identical_words(self):
        """Тест с идентичными словами"""
        distance = EditDistance.distance("hello", "hello")
        self.assertEqual(distance, 0)
    
    def test_empty_strings(self):
        """Тест с пустыми строками"""
        self.assertEqual(EditDistance.distance("", ""), 0)
        self.assertEqual(EditDistance.distance("a", ""), 1)
        self.assertEqual(EditDistance.distance("", "a"), 1)
    
    def test_single_character_difference(self):
        """Тест с одной операцией"""
        # Замена
        distance = EditDistance.distance("a", "b")
        self.assertEqual(distance, 1)
        
        # Вставка
        distance = EditDistance.distance("a", "ab")
        self.assertEqual(distance, 1)
        
        # Удаление
        distance = EditDistance.distance("ab", "a")
        self.assertEqual(distance, 1)
    
    def test_consistency(self):
        """Проверка консистентности полного и оптимизированного подходов"""
        test_cases = [
            ("kitten", "sitting"),
            ("saturday", "sunday"),
            ("abcdef", "fedcba"),
        ]
        
        for word1, word2 in test_cases:
            dist1 = EditDistance.distance(word1, word2)
            dist2 = EditDistance.distance_optimized(word1, word2)
            self.assertEqual(dist1, dist2)
    
    def test_symmetry(self):
        """Расстояние должно быть симметричным"""
        word1, word2 = "hello", "world"
        
        dist1 = EditDistance.distance(word1, word2)
        dist2 = EditDistance.distance(word2, word1)
        
        self.assertEqual(dist1, dist2)


class TestCoinChange(unittest.TestCase):
    """Тесты для задачи размена монет"""
    
    def test_zero_amount(self):
        """Тест с нулевой суммой"""
        coins = [1, 2, 5]
        count = CoinChange.min_coins(coins, 0)
        self.assertEqual(count, 0)
    
    def test_single_coin(self):
        """Тест когда нужна одна монета"""
        coins = [1, 2, 5]
        count = CoinChange.min_coins(coins, 5)
        self.assertEqual(count, 1)
    
    def test_impossible(self):
        """Тест невозможного случая"""
        coins = [2, 5]
        count = CoinChange.min_coins(coins, 3)
        self.assertEqual(count, -1)
    
    def test_with_recovery(self):
        """Тест восстановления монет"""
        coins = [1, 2, 5]
        amount = 10
        
        count, used_coins = CoinChange.min_coins_with_coins(coins, amount)
        self.assertEqual(count, len(used_coins))
        self.assertEqual(sum(used_coins), amount)
    
    def test_combinations(self):
        """Тест подсчёта комбинаций"""
        coins = [1, 2, 5]
        amount = 5
        
        combinations = CoinChange.count_combinations(coins, amount)
        # Способы: [5], [2,2,1], [2,1,1,1], [1,1,1,1,1]
        self.assertEqual(combinations, 4)


class TestLIS(unittest.TestCase):
    """Тесты для наибольшей возрастающей подпоследовательности"""
    
    def test_empty_array(self):
        """Тест с пустым массивом"""
        length = LongestIncreasingSubsequence.length([])
        self.assertEqual(length, 0)
    
    def test_single_element(self):
        """Тест с одним элементом"""
        length = LongestIncreasingSubsequence.length([5])
        self.assertEqual(length, 1)
        
        lis = LongestIncreasingSubsequence.find([5])
        self.assertEqual(lis, [5])
    
    def test_decreasing_sequence(self):
        """Тест с убывающей последовательностью"""
        arr = [5, 4, 3, 2, 1]
        length = LongestIncreasingSubsequence.length(arr)
        self.assertEqual(length, 1)
    
    def test_increasing_sequence(self):
        """Тест с возрастающей последовательностью"""
        arr = [1, 2, 3, 4, 5]
        length = LongestIncreasingSubsequence.length(arr)
        self.assertEqual(length, 5)
        
        lis = LongestIncreasingSubsequence.find(arr)
        self.assertEqual(lis, arr)
    
    def test_consistency(self):
        """Проверка консистентности O(n^2) и O(n log n) подходов"""
        test_arrays = [
            [10, 9, 2, 5, 3, 7, 101, 18],
            [0, 1, 0, 4, 4, 4, 3, 5, 1],
        ]
        
        for arr in test_arrays:
            len1 = LongestIncreasingSubsequence.length(arr)
            len2 = LongestIncreasingSubsequence.length_optimized(arr)
            self.assertEqual(len1, len2)


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main():
    """Запуск примеров и тестов"""
    print("\n" + "="*70)
    print("ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ: ПРИМЕРЫ И ТЕСТЫ")
    print("="*70)
    
    # Примеры
    example_fibonacci()
    example_knapsack()
    example_lcs()
    example_edit_distance()
    example_coin_change()
    example_lis()
    
    # Тесты
    print("\n" + "="*70)
    print("ЗАПУСК ЮНИТ-ТЕСТОВ")
    print("="*70)
    
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == "__main__":
    main()
