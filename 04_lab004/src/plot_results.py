"""
Модуль для визуализации результатов тестирования производительности алгоритмов сортировки.
Читает результаты из файла results.json и создает два графика:
1. График зависимости времени выполнения от размера массива для случайных данных
2. График зависимости времени выполнения от типа данных при фиксированном размере
"""

import json  # O(1)
import matplotlib.pyplot as plt  # O(1)

with open("results.json") as f:  # O(1)
    data = json.load(f)  # O(m) где m - размер файла, практически O(1)

sizes = [100, 1000, 5000, 10000]  # O(1)
algs = ["bubble", "selection", "insertion", "merge", "quick"]  # O(1)

# ===== ПЕРВЫЙ ГРАФИК: время vs размер массива для случайных данных =====

random_data = data["random"]  # O(1)
plt.figure(figsize=(10, 6))  # O(1)

for alg in algs:  # O(5) = O(1)
    plt.plot(sizes, [random_data[str(s)][alg] for s in sizes], label=alg)  # O(4) = O(1)

plt.xlabel("Размер массива")  # O(1)
plt.ylabel("Время (сек)")  # O(1)
plt.title("Производительность алгоритмов сортировки (random)")  # O(1)
plt.legend()  # O(1)
plt.grid()  # O(1)
plt.savefig("plot_random.png")  # O(p) размер пикселей
plt.close()  # O(1)

# ===== ВТОРОЙ ГРАФИК: время vs тип данных при n = 5000 =====

n = 5000  # O(1)
plt.figure(figsize=(10, 6))  # O(1)

for alg in algs:  # O(5) = O(1)
    plt.plot(  # O(1)
        ["random", "sorted", "reversed", "almost_sorted"],  # O(1)
        [data[t][str(n)][alg] for t in data],  # O(4) = O(1)
        label=alg  # O(1)
    )

plt.xlabel("Тип данных")  # O(1)
plt.ylabel("Время (сек)")  # O(1)
plt.title("Зависимость скорости от типа данных (n=5000)")  # O(1)
plt.legend()  # O(1)
plt.grid()  # O(1)
plt.savefig("plot_types.png")  # O(p) размер пикселей
plt.close()  # O(1)
