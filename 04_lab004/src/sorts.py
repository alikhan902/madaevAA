"""
Реализация пяти алгоритмов сортировки.
Для каждого указана временная и пространственная сложность.
"""

def bubble_sort(arr):
    """
    BUBBLE SORT - алгоритм сортировки методом "пузырька".
    """
    a = arr[:]  # O(n)
    n = len(a)  # O(1)
    
    for i in range(n):  # O(n) внешний цикл
        swapped = False  # O(1)
        
        for j in range(0, n - i - 1):  # O(n), O(n-1), ... в каждой итерации → O(n^2) всего
            if a[j] > a[j+1]:  # O(1)
                a[j], a[j+1] = a[j+1], a[j]  # O(1)
                swapped = True  # O(1)
        
        if not swapped:  # O(1)
            break  # O(1)
    
    return a  # O(1)


def selection_sort(arr):
    """
    SELECTION SORT - алгоритм сортировки методом выбора.
    """
    a = arr[:]  # O(n)
    n = len(a)  # O(1)
    
    for i in range(n):  # O(n) внешний цикл
        min_i = i  # O(1)
        
        for j in range(i+1, n):  # O(n), O(n-1), ... в каждой итерации → O(n^2) всего
            if a[j] < a[min_i]:  # O(1)
                min_i = j  # O(1)
        
        a[i], a[min_i] = a[min_i], a[i]  # O(1)
    
    return a  # O(1)


def insertion_sort(arr):
    """
    INSERTION SORT - алгоритм сортировки методом вставки.
    """
    # O(n) - создание копии массива
    a = arr[:]
    
    # O(1) - цикл с i = 1
    for i in range(1, len(a)):  # O(n) итераций
        # O(1) - сохранение текущего элемента для вставки
        key = a[i]
        
        # O(1) - инициализация указателя j = i - 1
        j = i - 1
        
        while j >= 0 and a[j] > key:  # Сдвигаем все элементы больше key на одну позицию вправо
            # O(1) - присваивание (сдвиг элемента)
            a[j+1] = a[j]
            # O(1) - уменьшение j
            j -= 1
        
        # O(1) - вставка key на правильную позицию
        a[j+1] = key
    
    # O(1) - возврат массива
    return a


def merge_sort(arr):
    """
    MERGE SORT - алгоритм сортировки методом слияния.
    """
    if len(arr) <= 1:  # O(1)
        return arr  # O(1)

    mid = len(arr) // 2  # O(1)
    left = merge_sort(arr[:mid])  # O(n/2) на срез + T(n/2) рекурсия
    right = merge_sort(arr[mid:])  # O(n/2) на срез + T(n/2) рекурсия
    return merge(left, right)  # O(n) объединение


def merge(left, right):
    """
    Вспомогательная функция для merge_sort - объединение двух отсортированных массивов в один.
    Использует технику "двух указателей" для эффективного слияния.
    """
    result = []  # O(1)
    i = j = 0  # O(1)

    while i < len(left) and j < len(right):  # O(min(n, m))
        if left[i] <= right[j]:  # O(1)
            result.append(left[i])  # O(1) amortized
            i += 1  # O(1)
        else:  # O(1)
            result.append(right[j])  # O(1) amortized
            j += 1  # O(1)

    result.extend(left[i:])  # O(n) в худшем случае
    result.extend(right[j:])  # O(m) в худшем случае
    return result  # O(1)


def quick_sort(arr):
    """
    QUICK SORT - алгоритм сортировки методом быстрой сортировки.
    """
    if len(arr) <= 1:  # O(1)
        return arr  # O(1)

    pivot = arr[len(arr)//2]  # O(1)
    less = [x for x in arr if x < pivot]  # O(n)
    equal = [x for x in arr if x == pivot]  # O(n)
    greater = [x for x in arr if x > pivot]  # O(n)

    return quick_sort(less) + equal + quick_sort(greater)  # T(less) + T(greater) + O(n)
