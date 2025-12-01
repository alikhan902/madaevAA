# plot_results.py
# Модуль для визуализации результатов производительности хеш-таблиц

import json  # O(1) импорт
import matplotlib.pyplot as plt  # O(1) импорт
import numpy as np  # O(1) импорт

with open("hash_perf_results.json") as f:  # O(1) открытие файла
    data = json.load(f)  # O(результаты) парсинг JSON

results = data.get("results", data)  # O(1) получение словаря

# Построим: для каждой таблицы и хеш-функции — insert per-op median vs load_factor
for hf in results:  # O(3) цикл по хеш-функциям
    plt.figure(figsize=(8,5))  # O(1) создание фигуры
    for tbl in results[hf]:  # O(3) цикл по таблицам
        lfs = sorted((float(k) for k in results[hf][tbl].keys()))  # O(4*log(4)) сортировка
        times = []  # O(1) инициализация списка
        for lf in lfs:  # O(4) цикл
            entry = results[hf][tbl][str(lf)]  # O(1) доступ
            # support both old and new formats
            if "insert" in entry:  # O(1) проверка
                times.append(entry["insert"]["per_op_median"])  # O(1) добавление
            else:  # O(1)
                times.append(entry.get("insert_time", 0) / 500)  # O(1) деление
        plt.plot(lfs, times, marker='o', label=tbl)  # O(4) построение графика
    plt.xlabel("Load factor")  # O(1) установка метки
    plt.ylabel("Insert time per op (s)")  # O(1)
    plt.title(f"Insert per-op median vs load factor — hash {hf}")  # O(1) заголовок
    plt.grid(True)  # O(1) сетка
    plt.legend()  # O(1) легенда
    plt.savefig(f"insert_vs_load_{hf}.png")  # O(1) сохранение
    plt.close()  # O(1) закрытие

# Гистограммы коллизий для каждой hash function + таблица
for hf in results:  # O(3) цикл по хеш-функциям
    plt.figure(figsize=(10,5))  # O(1) создание фигуры
    labels = []  # O(1) инициализация списка
    collisions_vals = []  # O(1)
    for tbl in results[hf]:  # O(3) цикл по таблицам
        for lf in sorted(results[hf][tbl].keys(), key=lambda x: float(x)):  # O(4*log(4)) сортировка
            labels.append(f"{tbl}\n{lf}")  # O(1) добавление
            collisions_vals.append(results[hf][tbl][lf].get("collisions", 0) or 0)  # O(1) добавление
    plt.bar(labels, collisions_vals)  # O(12) построение гистограммы
    plt.title(f"Collisions histogram — hash {hf}")  # O(1) заголовок
    plt.xticks(rotation=45)  # O(1) ротация меток
    plt.tight_layout()  # O(1) автоматическое расположение
    plt.savefig(f"collisions_{hf}.png")  # O(1) сохранение
    plt.close()  # O(1) закрытие
