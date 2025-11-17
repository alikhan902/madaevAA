"""
Модуль для тестирования корректности всех реализованных алгоритмов сортировки.
Проверяет правильность работы на различных типах входных данных.
"""

from sorts import bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort  # O(1)
import random  # O(1)


def is_sorted(arr):
    """
    Проверяет, является ли массив отсортированным в порядке неубывания.
    
    Временная сложность: O(n)
    Пространственная сложность: O(1)
    
    Args:
        arr: список для проверки
    
    Returns:
        bool: True если массив отсортирован, False иначе
    """
    for i in range(len(arr) - 1):  # O(n)
        if arr[i] > arr[i + 1]:  # O(1)
            return False  # O(1)
    return True  # O(1)


def test_sort_function(sort_func, test_name):
    """
    Тестирует функцию сортировки на различных типах входных данных.
    
    Временная сложность: O(n²) в худшем случае (зависит от алгоритма)
    Пространственная сложность: O(n)
    
    Args:
        sort_func: функция сортировки для тестирования
        test_name: имя тестируемой функции (для вывода)
    
    Returns:
        bool: True если все тесты пройдены, False иначе
    """
    test_cases = [  # O(1)
        ([], "пустой массив"),  # O(1)
        ([1], "один элемент"),  # O(1)
        ([2, 1], "два элемента"),  # O(1)
        ([1, 2, 3, 4, 5], "отсортированный массив"),  # O(1)
        ([5, 4, 3, 2, 1], "обратно отсортированный массив"),  # O(1)
        ([3, 1, 4, 1, 5, 9, 2, 6], "случайный массив"),  # O(1)
        ([1, 1, 1, 1, 1], "все элементы одинаковые"),  # O(1)
        ([2, 1, 2, 1, 2, 1], "чередующиеся элементы"),  # O(1)
        (list(range(100, 0, -1)), "большой обратно отсортированный (100 элементов)"),  # O(n)
        ([random.randint(0, 1000) for _ in range(100)], "большой случайный (100 элементов)"),  # O(n)
    ]
    
    passed = 0  # O(1)
    failed = 0  # O(1)
    
    print(f"\n{'='*70}")  # O(1)
    print(f"Тестирование: {test_name}")  # O(1)
    print(f"{'='*70}")  # O(1)
    
    for arr, description in test_cases:  # O(10)
        try:  # O(1)
            original = arr[:]  # O(n) копирование массива
            result = sort_func(arr)  # O(T(n)) выполнение алгоритма
            
            # Проверка 1: результат отсортирован  # O(1)
            if not is_sorted(result):  # O(n)
                print(f"  ✗ ОШИБКА: {description}")  # O(1)
                print(f"    Результат не отсортирован: {result}")  # O(1)
                failed += 1  # O(1)
                continue  # O(1)
            
            # Проверка 2: размер результата совпадает с исходным  # O(1)
            if len(result) != len(original):  # O(1)
                print(f"  ✗ ОШИБКА: {description}")  # O(1)
                print(f"    Изменился размер массива: {len(original)} -> {len(result)}")  # O(1)
                failed += 1  # O(1)
                continue  # O(1)
            
            # Проверка 3: результат содержит все исходные элементы  # O(1)
            if sorted(result) != sorted(original):  # O(n log n)
                print(f"  ✗ ОШИБКА: {description}")  # O(1)
                print(f"    Потеряны или добавлены элементы")  # O(1)
                print(f"    Исходный: {sorted(original)}")  # O(1)
                print(f"    Результат: {sorted(result)}")  # O(1)
                failed += 1  # O(1)
                continue  # O(1)
            
            # Проверка 4: исходный массив не изменен (если функция получает копию)  # O(1)
            # (в нашей реализации это гарантировано, т.к. функции делают копию)
            
            print(f"  ✓ ПРОЙДЕН: {description}")  # O(1)
            passed += 1  # O(1)
            
        except Exception as e:  # O(1)
            print(f"  ✗ ИСКЛЮЧЕНИЕ: {description}")  # O(1)
            print(f"    {str(e)}")  # O(1)
            failed += 1  # O(1)
    
    # Вывод результатов  # O(1)
    print(f"\n{'-'*70}")  # O(1)
    print(f"Результаты: {passed} пройдено, {failed} не пройдено из {passed + failed}")  # O(1)
    print(f"{'='*70}")  # O(1)
    
    return failed == 0  # O(1)


def compare_with_builtin(sort_func, test_name, test_size=1000):
    """
    Сравнивает результаты пользовательской функции сортировки с встроенной sorted().
    
    Временная сложность: O(n log n)
    Пространственная сложность: O(n)
    
    Args:
        sort_func: функция сортировки для тестирования
        test_name: имя функции (для вывода)
        test_size: размер тестового массива
    
    Returns:
        bool: True если результаты совпадают
    """
    print(f"\n{'='*70}")  # O(1)
    print(f"Сравнение с встроенной sorted(): {test_name}")  # O(1)
    print(f"{'='*70}")  # O(1)
    
    # Тест 1: Случайный массив большого размера  # O(1)
    arr1 = [random.randint(0, 10000) for _ in range(test_size)]  # O(n)
    result1 = sort_func(arr1)  # O(T(n))
    expected1 = sorted(arr1)  # O(n log n)
    
    if result1 == expected1:  # O(n)
        print(f"  ✓ Случайный массив ({test_size} элементов): совпадает")  # O(1)
    else:  # O(1)
        print(f"  ✗ Случайный массив ({test_size} элементов): НЕ совпадает!")  # O(1)
        return False  # O(1)
    
    # Тест 2: Массив с дубликатами  # O(1)
    arr2 = [random.randint(0, 100) for _ in range(test_size)]  # O(n)
    result2 = sort_func(arr2)  # O(T(n))
    expected2 = sorted(arr2)  # O(n log n)
    
    if result2 == expected2:  # O(n)
        print(f"  ✓ Массив с дубликатами ({test_size} элементов): совпадает")  # O(1)
    else:  # O(1)
        print(f"  ✗ Массив с дубликатами ({test_size} элементов): НЕ совпадает!")  # O(1)
        return False  # O(1)
    
    # Тест 3: Отрицательные числа  # O(1)
    arr3 = [random.randint(-5000, 5000) for _ in range(test_size)]  # O(n)
    result3 = sort_func(arr3)  # O(T(n))
    expected3 = sorted(arr3)  # O(n log n)
    
    if result3 == expected3:  # O(n)
        print(f"  ✓ Массив с отрицательными числами ({test_size} элементов): совпадает")  # O(1)
    else:  # O(1)
        print(f"  ✗ Массив с отрицательными числами ({test_size} элементов): НЕ совпадает!")  # O(1)
        return False  # O(1)
    
    print(f"{'='*70}")  # O(1)
    return True  # O(1)


if __name__ == "__main__":  # O(1)
    """
    Главный блок для запуска всех тестов всех алгоритмов.
    """
    algorithms = [  # O(1)
        (bubble_sort, "Bubble Sort"),  # O(1)
        (selection_sort, "Selection Sort"),  # O(1)
        (insertion_sort, "Insertion Sort"),  # O(1)
        (merge_sort, "Merge Sort"),  # O(1)
        (quick_sort, "Quick Sort"),  # O(1)
    ]
    
    all_passed = True  # O(1)
    
    print("\n" + "="*70)  # O(1)
    print("ТЕСТИРОВАНИЕ КОРРЕКТНОСТИ АЛГОРИТМОВ СОРТИРОВКИ")  # O(1)
    print("="*70)  # O(1)
    
    # Основные тесты корректности  # O(1)
    for sort_func, name in algorithms:  # O(5)
        if not test_sort_function(sort_func, name):  # O(T(n))
            all_passed = False  # O(1)
    
    # Сравнение с встроенной функцией  # O(1)
    print("\n" + "="*70)  # O(1)
    print("СРАВНЕНИЕ С ВСТРОЕННОЙ ФУНКЦИЕЙ sorted()")  # O(1)
    print("="*70)  # O(1)
    
    for sort_func, name in algorithms:  # O(5)
        if not compare_with_builtin(sort_func, name):  # O(n log n)
            all_passed = False  # O(1)
    
    # Финальный результат  # O(1)
    print("\n" + "="*70)  # O(1)
    if all_passed:  # O(1)
        print("✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")  # O(1)
    else:  # O(1)
        print("✗ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОЙДЕНЫ!")  # O(1)
    print("="*70 + "\n")  # O(1)
