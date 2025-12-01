# performance_test.py
# Модуль эмпирического анализа производительности хеш-таблиц
"""
Замеры времени вставки / поиска / удаления и числа коллизий
для:
- HashTableChaining
- HashTableOpenAddressing (linear)
- HashTableOpenAddressing (double)

Для разных коэффициентов заполнения: [0.1, 0.5, 0.7, 0.9]
И для трёх хеш-функций: simple_hash, poly_hash, djb2_hash

Скрипт генерирует random string keys и измеряет операции.
"""

import time  # O(1) импорт
import json  # O(1) импорт
import random  # O(1) импорт
import string  # O(1) импорт
import platform  # O(1) импорт
import multiprocessing  # O(1) импорт
import statistics  # O(1) импорт
from hash_functions import simple_hash, poly_hash, djb2_hash  # O(1) импорт
from hash_table_chaining import HashTableChaining  # O(1) импорт
from hash_table_open_addressing import HashTableOpenAddressing  # O(1) импорт

HASH_FUNCS = {  # O(1) словарь
    "simple": simple_hash,  # O(1)
    "poly": poly_hash,  # O(1)
    "djb2": djb2_hash  # O(1)
}

TABLE_VARIANTS = {  # O(1) словарь фабрик
    "chaining": lambda hash_function: HashTableChaining(hash_func=hash_function),  # O(1) лямбда
    "open_linear": lambda hash_function: HashTableOpenAddressing(hash_func=hash_function, mode="linear"),  # O(1)
    "open_double": lambda hash_function: HashTableOpenAddressing(hash_func=hash_function, second_hash_func=simple_hash, mode="double")  # O(1)
}

LOAD_FACTORS = [0.1, 0.5, 0.7, 0.9]  # O(1) константы
TARGET_N = 20000  # O(1) число ключей для генерации
KEY_LEN = 10  # O(1) длина ключей
REPEATS = 5  # O(1) число повторений на каждый эксперимент

def gen_random_strings(n):  # O(n*KEY_LEN)
    """Генерирует n случайных строк длины KEY_LEN"""
    alph = string.ascii_letters + string.digits  # O(1)
    return [''.join(random.choices(alph, k=KEY_LEN)) for _ in range(n)]  # O(n*KEY_LEN)

def measure():  # O(3*3*4*5*операции) главная функция для измерения производительности
    """Главная функция для измерения производительности всех комбинаций
    Выполняет эксперименты для всех комбинаций:
    - 3 хеш-функции (simple, poly, djb2)
    - 3 типа таблиц (chaining, open_linear, open_double)
    - 4 коэффициента заполнения (0.1, 0.5, 0.7, 0.9)
    - 5 повторений каждого эксперимента
    Итого: 3*3*4*5 = 180 экспериментов
    """
    random.seed(0)  # O(1) установка seed для воспроизводимости результатов
    keys = gen_random_strings(TARGET_N)  # O(TARGET_N*KEY_LEN) генерация 20000 ключей
    values = list(range(TARGET_N))  # O(TARGET_N) создание соответствующих значений
    results = {}  # O(1) инициализация словаря для хранения результатов
    # Собираем информацию о машине для документирования результатов
    machine_info = {  # O(1) создание словаря информации об оборудовании
        "platform": platform.platform(),  # O(1) операционная система и версия
        "python_version": platform.python_version(),  # O(1) версия Python
        "processor": platform.processor(),  # O(1) название процессора
        "cpu_count": multiprocessing.cpu_count()  # O(1) количество ядер CPU
    }

    for hf_name, hf in HASH_FUNCS.items():  # O(3) цикл по хеш-функциям
        results[hf_name] = {}  # O(1) инициализация словаря
        for tbl_name, tbl_ctor in TABLE_VARIANTS.items():  # O(3) цикл по типам таблиц
            results[hf_name][tbl_name] = {}  # O(1) инициализация словаря
            for lf in LOAD_FACTORS:  # O(4) цикл по коэффициентам заполнения
                # Оценка ёмкости: выбираем capacity так чтобы size/capacity ≈ lf
                m = int(TARGET_N * 0.5)  # O(1) половина TARGET_N для ускорения
                # Создаём пустую таблицу, затем вставляем до нужного load factor
                tbl = tbl_ctor(hash_function=hf)  # O(capacity) создание таблицы
                # Вставляем ключи до достижения target load factor
                # Количество вставок: примерно 2000 * lf (baseline масштабирование)
                inserted = 0  # O(1) счётчик вставленных элементов
                i = 0  # O(1) индекс в массиве ключей
                while inserted < int(2000 * lf):  # O(2000*lf) цикл вставок подготовки
                    k = keys[i]  # O(1) получение ключа
                    tbl.put(k, values[i])  # O(n) хеш + O(1+α) вставка
                    inserted += 1  # O(1) увеличение счётчика
                    i += 1  # O(1) увеличение индекса

                # Подготовка ключей для измерения: существующие и новые (для неудачного поиска)
                existing_keys = keys[:inserted]  # O(inserted) срез массива
                new_keys = gen_random_strings(500)  # O(500*KEY_LEN) генерация новых ключей

                # Попытка предварительного безопасного ресайза чтобы не измерять стоимость ресайза
                try:  # O(1) попытка безопасного ресайза
                    s = tbl.stats()  # O(capacity) получение статистики таблицы
                    desired_after = s.get("size", 0) + 500  # O(1) прогноз размера после 500 вставок
                    # Выбираем ёмкость чтобы после вставок load factor был <= 0.9
                    safe_cap = max(s.get("capacity", 8), int(desired_after / 0.9) + 1)  # O(1) расчёт безопасной ёмкости
                    tbl._resize(safe_cap)  # O(n) ресайз таблицы для избежания переполнения
                except Exception:  # O(1) обработка исключения если ресайз недоступен
                    # Игнорируем ошибку ресайза и продолжаем измерения
                    pass  # O(1) продолжаем с текущей ёмкостью

                # Выполняем REPEATS измерений и собираем времена выполнения
                insert_times = []  # O(1) список для времён вставок
                search_hit_times = []  # O(1) список для времён успешных поисков
                search_miss_times = []  # O(1) список для времён неудачных поисков
                delete_times = []  # O(1) список для времён удалений
                # Для независимости повторов (удаления не влияют на следующий проход)
                # Создаём новую таблицу для каждого повторения и заполняем её существующими ключами
                for r in range(REPEATS):  # O(REPEATS) цикл повторений эксперимента
                    tbl_r = tbl_ctor(hash_function=hf)  # O(capacity) создание новой таблицы
                    # Заполняем таблицу теми же начальными существующими ключами
                    for k_i, v_i in zip(existing_keys, values[:len(existing_keys)]):  # O(inserted) цикл заполнения
                        tbl_r.put(k_i, v_i)  # O(n) хеш-функция + O(1+α) вставка в таблицу

                    # Предварительно увеличиваем ёмкость чтобы не измерять стоимость ресайза
                    try:  # O(1) попытка безопасного ресайза
                        s_r = tbl_r.stats()  # O(capacity) получение статистики
                        desired_after = s_r.get("size", 0) + 500  # O(1) вычисление ёмкости после вставок
                        safe_cap = max(s_r.get("capacity", 8), int(desired_after / 0.9) + 1)  # O(1) выбор безопасной ёмкости
                        tbl_r._resize(safe_cap)  # O(n) ресайз для избежания переполнения
                    except Exception:  # O(1) обработка исключения если ресайз недоступен
                        pass  # O(1) игнорируем ошибку ресайза

                    new_keys_r = gen_random_strings(500)  # O(500*KEY_LEN) генерация 500 новых ключей

                    # Измерение вставки: 500 новых элементов
                    start = time.perf_counter()  # O(1) начало замера времени
                    for j in range(500):  # O(500) цикл вставок
                        tbl_r.put(new_keys_r[j], j)  # O(n) хеш + O(1+α) вставка
                    insert_times.append(time.perf_counter() - start)  # O(1) добавление результата

                    # Измерение поиска хитов: 500 успешных поисков существующих ключей
                    start = time.perf_counter()  # O(1) начало замера
                    for j in range(500):  # O(500) цикл поисков
                        _ = tbl_r.get(existing_keys[j % len(existing_keys)])  # O(n) хеш + O(1+α) поиск
                    search_hit_times.append(time.perf_counter() - start)  # O(1) добавление результата

                    # Измерение поиска промахов: 500 поисков несуществующих ключей
                    start = time.perf_counter()  # O(1) начало замера
                    for j in range(500):  # O(500) цикл попыток поиска
                        try:  # O(1) попытка поиска
                            _ = tbl_r.get(new_keys_r[j] + "_x")  # O(n) хеш + O(1+α) поиск (промах)
                        except KeyError:  # O(1) обработка исключения
                            pass  # O(1) игнорируем KeyError для промахов
                    search_miss_times.append(time.perf_counter() - start)  # O(1) добавление результата

                    # Измерение удаления: 200 удалений существующих ключей
                    start = time.perf_counter()  # O(1) начало замера
                    for j in range(200):  # O(200) цикл удалений
                        try:  # O(1) попытка удаления
                            tbl_r.delete(existing_keys[j])  # O(n) хеш + O(1+α) удаление
                        except KeyError:  # O(1) обработка исключения
                            pass  # O(1) игнорируем ошибку если ключа нет
                    delete_times.append(time.perf_counter() - start)  # O(1) добавление результата

                stats = tbl.stats()  # O(capacity) получение финальной статистики

                def summarize(times, ops):  # O(REPEATS) функция для суммаризации результатов
                    """Вычисляет статистику из массива времён выполнения"""
                    med = statistics.median(times)  # O(REPEATS) вычисление медианы
                    mean = statistics.mean(times)  # O(REPEATS) вычисление среднего
                    stdev = statistics.pstdev(times)  # O(REPEATS) вычисление стандартного отклонения
                    return {  # O(1) возврат словаря со статистикой
                        "total_median": med,  # O(1) медиана общего времени
                        "total_mean": mean,  # O(1) среднее общее время
                        "total_stdev": stdev,  # O(1) стандартное отклонение
                        "per_op_median": med / ops,  # O(1) медиана времени на одну операцию
                        "per_op_mean": mean / ops  # O(1) среднее время на одну операцию
                    }

                # Сохранение результатов для текущей комбинации (хеш-функция, таблица, load factor)
                results[hf_name][tbl_name][str(lf)] = {  # O(1) запись результатов в словарь
                    "insert": summarize(insert_times, 500),  # O(REPEATS) суммаризация вставок
                    "search_hit": summarize(search_hit_times, 500),  # O(REPEATS) суммаризация успешных поисков
                    "search_miss": summarize(search_miss_times, 500),  # O(REPEATS) суммаризация промахов поиска
                    "delete": summarize(delete_times, 200),  # O(REPEATS) суммаризация удалений
                    "collisions": stats.get("collisions", None),  # O(1) число коллизий
                    "load_factor": stats.get("load_factor", None),  # O(1) коэффициент заполнения
                    "size": stats.get("size", None),  # O(1) число элементов в таблице
                    "capacity": stats.get("capacity", None),  # O(1) ёмкость таблицы
                    "repeats": REPEATS  # O(1) число выполненных повторений
                }
                # Вывод промежуточного результата для отслеживания прогресса
                print(f"{hf_name} | {tbl_name} | lf={lf} -> insert per-op {results[hf_name][tbl_name][str(lf)]['insert']['per_op_median']:.6f}s, collisions={stats.get('collisions')}")  # O(1) печать
    # Подготовка выходного словаря с информацией о машине и результатами
    out = {  # O(1) создание итогового словаря
        "machine_info": machine_info,  # O(1) информация об оборудовании
        "results": results  # O(1) все результаты измерений
    }
    # Сохранение результатов в JSON файл
    with open("hash_perf_results.json", "w") as f:  # O(1) открытие файла для записи
        json.dump(out, f, indent=2)  # O(результаты) сериализация в JSON с форматированием

if __name__ == "__main__":  # O(1)
    measure()  # O(3*3*4*5*операции) главная функция
