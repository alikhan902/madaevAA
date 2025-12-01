# Замеры времени для Heapsort и других алгоритмов сортировки.
# Добавлены комментарии и оценки сложности для каждой строки.
import time  # O(1) импорт модуля для работы со временем
import random  # O(1) импорт модуля для генерации случайных данных
import matplotlib.pyplot as plt  # O(1) импорт для построения графиков

from heapsort import heapsort  # O(1) импорт функции heapsort из модуля


def measure_time():  # O(1) определение функции измерения времени
    sizes = [100, 200, 500, 1000, 2000]  # O(1) список размеров входных данных (константа)
    heapsort_times = []  # O(1) список для хранения времен Heapsort
    quicksort_times = []  # O(1) список для хранения времен встроенной сортировки
    merge_sort_times = []  # O(1) список для хранения времен sorted()

    for size in sizes:  # O(len(sizes)) итерация по размерам (len(sizes) — константа здесь)
        array = random.sample(range(size * 10), size)  # O(size) создание случайного массива
        
        # Замер Heapsort
        start = time.time()  # O(1) фиксация времени начала
        heapsort(array)  # O(n log n) запуск heapsort на массиве длины n
        heapsort_times.append(time.time() - start)  # O(1) добавление результата
        
        # Замер QuickSort (встроенный .sort())
        start = time.time()  # O(1) фиксация времени начала
        array.sort()  # O(n log n) встроенная сортировка (обычно Timsort)  
        quicksort_times.append(time.time() - start)  # O(1) добавление результата
        
        # Замер MergeSort (функция sorted)
        start = time.time()  # O(1) фиксация времени начала
        sorted(array)  # O(n log n) создание отсортированного нового списка
        merge_sort_times.append(time.time() - start)  # O(1) добавление результата

    # Построение графиков
    plt.plot(sizes, heapsort_times, label='Heapsort')  # O(len(sizes)) построение линии
    plt.plot(sizes, quicksort_times, label='QuickSort')  # O(len(sizes)) построение линии
    plt.plot(sizes, merge_sort_times, label='MergeSort')  # O(len(sizes)) построение линии
    plt.xlabel('Размер массива')  # O(1) подпись оси X
    plt.ylabel('Время (сек)')  # O(1) подпись оси Y
    plt.legend()  # O(1) отображение легенды
    plt.show()  # вывод графика — строка вывода, сложность не проставлена


measure_time()  # O(1) вызов функции измерения времени (запуск эксперимента)
