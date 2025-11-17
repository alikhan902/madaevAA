"""
Модуль для тестирования производительности алгоритмов сортировки.
Измеряет время выполнения каждого алгоритма на различных размерах и типах данных.
"""

import timeit  # O(1)
import json  # O(1)
from sorts import *  # O(1)
import generate_data as gen  # O(1)

sizes = [100, 1000, 5000, 10000]  # O(1)
types = {  # O(1)
    "random": gen.generate_random,
    "sorted": gen.generate_sorted,
    "reversed": gen.generate_reversed,
    "almost_sorted": gen.generate_almost_sorted
}

algorithms = {  # O(1)
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort
}

results = {}  # O(1)

for tname, tfunc in types.items():  # O(4) внешний цикл по 4 типам данных
    results[tname] = {}  # O(1)
    for n in sizes:  # O(4) цикл по 4 размерам
        arr = tfunc(n)  # O(n) генерация массива размера n
        print(f"Testing {tname}, n={n}")  # O(1)

        results[tname][n] = {}  # O(1)

        for aname, afunc in algorithms.items():  # O(5) цикл по 5 алгоритмам

            def test():  # O(1)
                afunc(arr[:])  # O(n) копирование массива + O(T(n)) сортировка, где T(n) - сложность алгоритма

            duration = timeit.timeit(test, number=5)  # O(5 * T(n)) выполнение тестовой функции 5 раз
            results[tname][n][aname] = duration  # O(1)

with open("results.json", "w") as f:  # O(1)
    json.dump(results, f, indent=4)  # O(r) где r - размер результирующего JSON
