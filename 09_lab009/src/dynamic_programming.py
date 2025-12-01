"""
Модуль реализации классических алгоритмов динамического программирования.

Содержит реализации:
1. Числа Фибоначчи (наивная рекурсия, мемоизация, табличный подход)
2. Задача о рюкзаке 0-1 (табличный подход)
3. Наибольшая общая подпоследовательность LCS (табличный подход)
4. Расстояние Левенштейна (табличный подход)
5. Размен монет (табличный подход)
6. Наибольшая возрастающая подпоследовательность LIS (табличный подход)
"""

import sys
from typing import Dict, List, Tuple


# ============================================================================
# ЧАСТЬ 1: ЧИСЛА ФИБОНАЧЧИ
# ============================================================================

class Fibonacci:
    """Три подхода к вычислению чисел Фибоначчи"""

    @staticmethod
    def naive(n: int) -> int:
        """
        Наивная рекурсия.
        
        Временная сложность: O(2^n) - экспоненциальная
        Пространственная сложность: O(n) - глубина рекурсии
        
        Args:
            n: порядковый номер чисел Фибоначчи
            
        Returns:
            n-е число Фибоначчи
        """
        if n <= 1:
            return n
        return Fibonacci.naive(n - 1) + Fibonacci.naive(n - 2)

    @staticmethod
    def memoization(n: int, memo: Dict[int, int] = None) -> int:
        """
        Рекурсия с мемоизацией (Top-Down подход).
        
        Временная сложность: O(n) - каждое значение вычисляется один раз
        Пространственная сложность: O(n) - хранилище мемо + стек рекурсии
        
        Args:
            n: порядковый номер чисел Фибоначчи
            memo: словарь для кэширования результатов
            
        Returns:
            n-е число Фибоначчи
        """
        if memo is None:
            memo = {}
        
        if n in memo:
            return memo[n]
        
        if n <= 1:
            return n
        
        memo[n] = Fibonacci.memoization(n - 1, memo) + Fibonacci.memoization(n - 2, memo)
        return memo[n]

    @staticmethod
    def tabular(n: int) -> int:
        """
        Табличный подход (Bottom-Up).
        
        Временная сложность: O(n)
        Пространственная сложность: O(n)
        
        Args:
            n: порядковый номер чисел Фибоначчи
            
        Returns:
            n-е число Фибоначчи
        """
        if n <= 1:
            return n
        
        dp = [0] * (n + 1)
        dp[1] = 1
        
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        
        return dp[n]

    @staticmethod
    def tabular_optimized(n: int) -> int:
        """
        Оптимизированный табличный подход (O(1) память).
        
        Временная сложность: O(n)
        Пространственная сложность: O(1)
        
        Args:
            n: порядковый номер чисел Фибоначчи
            
        Returns:
            n-е число Фибоначчи
        """
        if n <= 1:
            return n
        
        prev, curr = 0, 1
        for _ in range(2, n + 1):
            prev, curr = curr, prev + curr
        
        return curr


# ============================================================================
# ЧАСТЬ 2: ЗАДАЧА О РЮКЗАКЕ 0-1 (Knapsack Problem)
# ============================================================================

class KnapsackZeroOne:
    """Решение задачи о рюкзаке 0-1 с помощью динамического программирования"""

    @staticmethod
    def solve(weights: List[int], values: List[int], capacity: int) -> int:
        """
        Найти максимальную стоимость предметов, которые можно поместить в рюкзак.
        
        Временная сложность: O(n * capacity)
        Пространственная сложность: O(n * capacity)
        
        Args:
            weights: список весов предметов
            values: список стоимостей предметов
            capacity: вместимость рюкзака
            
        Returns:
            максимальная стоимость
        """
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        
        # Заполнение таблицы DP
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                # Если предмет не поместится
                if weights[i - 1] <= w:
                    # Выбираем максимум: берём предмет или не берём
                    dp[i][w] = max(
                        values[i - 1] + dp[i - 1][w - weights[i - 1]],
                        dp[i - 1][w]
                    )
                else:
                    # Не можем взять, берём результат без этого предмета
                    dp[i][w] = dp[i - 1][w]
        
        return dp[n][capacity]

    @staticmethod
    def solve_with_recovery(
        weights: List[int],
        values: List[int],
        capacity: int
    ) -> Tuple[int, List[int]]:
        """
        Найти максимальную стоимость и восстановить список включённых предметов.
        
        Временная сложность: O(n * capacity)
        Пространственная сложность: O(n * capacity)
        
        Args:
            weights: список весов предметов
            values: список стоимостей предметов
            capacity: вместимость рюкзака
            
        Returns:
            (максимальная стоимость, список индексов включённых предметов)
        """
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        
        # Заполнение таблицы DP
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if weights[i - 1] <= w:
                    dp[i][w] = max(
                        values[i - 1] + dp[i - 1][w - weights[i - 1]],
                        dp[i - 1][w]
                    )
                else:
                    dp[i][w] = dp[i - 1][w]
        
        # Восстановление решения
        items = []
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                items.append(i - 1)  # Индекс предмета
                w -= weights[i - 1]
        
        items.reverse()
        return dp[n][capacity], items

    @staticmethod
    def solve_optimized(weights: List[int], values: List[int], capacity: int) -> int:
        """
        Оптимизированное решение с использованием одномерного массива.
        
        Временная сложность: O(n * capacity)
        Пространственная сложность: O(capacity)
        
        Args:
            weights: список весов предметов
            values: список стоимостей предметов
            capacity: вместимость рюкзака
            
        Returns:
            максимальная стоимость
        """
        n = len(weights)
        dp = [0] * (capacity + 1)
        
        for i in range(n):
            # Идем справа налево, чтобы не использовать уже обновленные значения
            for w in range(capacity, weights[i] - 1, -1):
                dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
        
        return dp[capacity]

    @staticmethod
    def solve_optimized_with_recovery(
        weights: List[int],
        values: List[int],
        capacity: int
    ) -> Tuple[int, List[int]]:
        """
        Оптимизированное решение с восстановлением списка предметов.
        
        Использует полную таблицу для восстановления, затем возвращает результат.
        
        Временная сложность: O(n * capacity)
        Пространственная сложность: O(n * capacity)
        
        Args:
            weights: список весов предметов
            values: список стоимостей предметов
            capacity: вместимость рюкзака
            
        Returns:
            (максимальная стоимость, список индексов включённых предметов)
        """
        # Используем полную таблицу для возможности восстановления
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if weights[i - 1] <= w:
                    dp[i][w] = max(
                        values[i - 1] + dp[i - 1][w - weights[i - 1]],
                        dp[i - 1][w]
                    )
                else:
                    dp[i][w] = dp[i - 1][w]
        
        # Восстановление
        items = []
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                items.append(i - 1)
                w -= weights[i - 1]
        
        items.reverse()
        return dp[n][capacity], items


# ============================================================================
# ЧАСТЬ 3: НАИБОЛЬШАЯ ОБЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ (LCS)
# ============================================================================

class LongestCommonSubsequence:
    """Решение задачи LCS с помощью динамического программирования"""

    @staticmethod
    def length(text1: str, text2: str) -> int:
        """
        Найти длину наибольшей общей подпоследовательности.
        
        Временная сложность: O(m * n)
        Пространственная сложность: O(m * n)
        
        Args:
            text1: первая строка
            text2: вторая строка
            
        Returns:
            длина LCS
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        return dp[m][n]

    @staticmethod
    def find(text1: str, text2: str) -> str:
        """
        Найти и восстановить саму наибольшую общую подпоследовательность.
        
        Временная сложность: O(m * n)
        Пространственная сложность: O(m * n)
        
        Args:
            text1: первая строка
            text2: вторая строка
            
        Returns:
            LCS как строка
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Заполнение таблицы DP
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        # Восстановление LCS
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if text1[i - 1] == text2[j - 1]:
                lcs.append(text1[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1
        
        return ''.join(reversed(lcs))

    @staticmethod
    def get_table(text1: str, text2: str) -> List[List[int]]:
        """
        Получить таблицу DP для визуализации процесса.
        
        Args:
            text1: первая строка
            text2: вторая строка
            
        Returns:
            таблица DP
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        return dp


# ============================================================================
# ЧАСТЬ 4: РАССТОЯНИЕ ЛЕВЕНШТЕЙНА (Edit Distance)
# ============================================================================

class EditDistance:
    """Решение задачи на расстояние Левенштейна"""

    @staticmethod
    def distance(word1: str, word2: str) -> int:
        """
        Вычислить минимальное расстояние редактирования между двумя строками.
        
        Допустимые операции: вставка, удаление, замена символа.
        
        Временная сложность: O(m * n)
        Пространственная сложность: O(m * n)
        
        Args:
            word1: первая строка
            word2: вторая строка
            
        Returns:
            расстояние Левенштейна
        """
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Инициализация первых строки и столбца
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        # Заполнение таблицы DP
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i - 1][j],      # удаление
                        dp[i][j - 1],      # вставка
                        dp[i - 1][j - 1]   # замена
                    )
        
        return dp[m][n]

    @staticmethod
    def distance_optimized(word1: str, word2: str) -> int:
        """
        Оптимизированное решение с использованием одномерного массива.
        
        Временная сложность: O(m * n)
        Пространственная сложность: O(n)
        
        Args:
            word1: первая строка
            word2: вторая строка
            
        Returns:
            расстояние Левенштейна
        """
        m, n = len(word1), len(word2)
        
        # Убеждаемся, что word2 короче для экономии памяти
        if m < n:
            word1, word2 = word2, word1
            m, n = n, m
        
        prev = list(range(n + 1))
        curr = [0] * (n + 1)
        
        for i in range(1, m + 1):
            curr[0] = i
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    curr[j] = prev[j - 1]
                else:
                    curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
            
            prev, curr = curr, prev
        
        return prev[n]

    @staticmethod
    def get_table(word1: str, word2: str) -> List[List[int]]:
        """
        Получить таблицу DP для визуализации.
        
        Args:
            word1: первая строка
            word2: вторая строка
            
        Returns:
            таблица DP
        """
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        
        return dp


# ============================================================================
# ЧАСТЬ 5: РАЗМЕН МОНЕТ (Coin Change)
# ============================================================================

class CoinChange:
    """Решение задачи о размене монет"""

    @staticmethod
    def min_coins(coins: List[int], amount: int) -> int:
        """
        Найти минимальное количество монет для образования суммы.
        
        Временная сложность: O(n * amount)
        Пространственная сложность: O(amount)
        
        Args:
            coins: список номиналов монет
            amount: целевая сумма
            
        Returns:
            минимальное количество монет или -1, если невозможно
        """
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        
        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i:
                    dp[i] = min(dp[i], dp[i - coin] + 1)
        
        return dp[amount] if dp[amount] != float('inf') else -1

    @staticmethod
    def min_coins_with_coins(coins: List[int], amount: int) -> Tuple[int, List[int]]:
        """
        Найти минимальное количество монет и восстановить сам набор.
        
        Временная сложность: O(n * amount)
        Пространственная сложность: O(amount)
        
        Args:
            coins: список номиналов монет
            amount: целевая сумма
            
        Returns:
            (минимальное количество монет, список использованных монет)
        """
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        parent = [-1] * (amount + 1)
        
        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i and dp[i - coin] + 1 < dp[i]:
                    dp[i] = dp[i - coin] + 1
                    parent[i] = coin
        
        if dp[amount] == float('inf'):
            return -1, []
        
        # Восстановление монет
        used_coins = []
        current = amount
        while current > 0:
            coin = parent[current]
            used_coins.append(coin)
            current -= coin
        
        return dp[amount], used_coins

    @staticmethod
    def count_combinations(coins: List[int], amount: int) -> int:
        """
        Найти количество способов образования суммы.
        
        Временная сложность: O(n * amount)
        Пространственная сложность: O(amount)
        
        Args:
            coins: список номиналов монет
            amount: целевая сумма
            
        Returns:
            количество способов
        """
        dp = [0] * (amount + 1)
        dp[0] = 1
        
        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] += dp[i - coin]
        
        return dp[amount]


# ============================================================================
# ЧАСТЬ 6: НАИБОЛЬШАЯ ВОЗРАСТАЮЩАЯ ПОДПОСЛЕДОВАТЕЛЬНОСТЬ (LIS)
# ============================================================================

class LongestIncreasingSubsequence:
    """Решение задачи о наибольшей возрастающей подпоследовательности"""

    @staticmethod
    def length(arr: List[int]) -> int:
        """
        Найти длину наибольшей возрастающей подпоследовательности.
        
        Временная сложность: O(n^2)
        Пространственная сложность: O(n)
        
        Args:
            arr: входной массив
            
        Returns:
            длина LIS
        """
        n = len(arr)
        if n == 0:
            return 0
        
        dp = [1] * n
        
        for i in range(1, n):
            for j in range(i):
                if arr[j] < arr[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        
        return max(dp)

    @staticmethod
    def find(arr: List[int]) -> List[int]:
        """
        Найти и восстановить саму наибольшую возрастающую подпоследовательность.
        
        Временная сложность: O(n^2)
        Пространственная сложность: O(n)
        
        Args:
            arr: входной массив
            
        Returns:
            список элементов LIS
        """
        n = len(arr)
        if n == 0:
            return []
        
        dp = [1] * n
        parent = [-1] * n
        
        for i in range(1, n):
            for j in range(i):
                if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j
        
        # Найти индекс максимальной длины
        max_length = max(dp)
        max_idx = dp.index(max_length)
        
        # Восстановить подпоследовательность
        lis = []
        idx = max_idx
        while idx != -1:
            lis.append(arr[idx])
            idx = parent[idx]
        
        lis.reverse()
        return lis

    @staticmethod
    def length_optimized(arr: List[int]) -> int:
        """
        Оптимизированное решение с использованием двоичного поиска.
        
        Временная сложность: O(n log n)
        Пространственная сложность: O(n)
        
        Args:
            arr: входной массив
            
        Returns:
            длина LIS
        """
        import bisect
        
        tails = []
        
        for num in arr:
            pos = bisect.bisect_left(tails, num)
            if pos == len(tails):
                tails.append(num)
            else:
                tails[pos] = num
        
        return len(tails)


# ============================================================================
# УТИЛИТЫ ДЛЯ ВИЗУАЛИЗАЦИИ
# ============================================================================

def print_table(table: List[List[int]], row_label: str = "", col_label: str = "") -> None:
    """
    Красиво вывести таблицу DP.
    
    Args:
        table: двумерный массив (таблица DP)
        row_label: строка для маркировки строк
        col_label: строка для маркировки столбцов
    """
    if not table:
        return
    
    # Вычислить ширину столбцов
    width = max(max(len(str(cell)) for row in table for cell in row), 4)
    
    # Вывести заголовок столбцов
    if col_label:
        print("  " + col_label[:width], end="")
        for j in range(len(table[0])):
            print(f"{j:{width}}", end="")
        print()
    
    # Вывести строки таблицы
    for i, row in enumerate(table):
        if row_label:
            print(f"{i}{row_label[min(i, len(row_label)-1)]}", end=" ")
        for cell in row:
            print(f"{cell:{width}}", end="")
        print()
