"""
Сравнительный анализ производительности алгоритмов поиска подстроки.

Проводит бенчмарки на различных типах данных:
1. Случайные строки
2. Периодические строки
3. Строки с повторениями
4. Худший случай (нет совпадений в конце)

Включает системную информацию о тестировании.
"""

import time
import random
import string
import json
from typing import Callable, Dict, Tuple, List
from datetime import datetime
import platform
import psutil

from kmp_search import kmp_search, kmp_search_first
from z_function import z_search
from string_matching import boyer_moore_search, rabin_karp_search


# Генераторы тестовых данных
def generate_random_string(length: int, alphabet_size: int = 4) -> str:
    """Генерирует случайную строку с заданным размером алфавита."""
    alphabet = string.ascii_uppercase[:alphabet_size]
    return ''.join(random.choice(alphabet) for _ in range(length))


def generate_periodic_string(pattern: str, repetitions: int) -> str:
    """Генерирует периодическую строку."""
    return pattern * repetitions


def generate_repeating_string(char: str, length: int) -> str:
    """Генерирует строку с повторениями одного символа."""
    return char * length


def generate_worst_case_string(pattern: str, text_length: int) -> str:
    """
    Генерирует худший случай: текст, где паттерн не найден.
    Используем символ, который не входит в паттерн.
    """
    if len(pattern) == 0:
        return ""
    
    # Используем символ, которого нет в паттерне
    used_chars = set(pattern)
    # Выбираем символ из полного алфавита, которого нет в паттерне
    for char in string.ascii_uppercase:
        if char not in used_chars:
            return char * text_length
    
    # Если все буквы используются, используем цифры
    return '0' * text_length


def benchmark_algorithm(
    algorithm: Callable,
    text: str,
    pattern: str,
    iterations: int = 1
) -> Tuple[float, List]:
    """
    Бенчмарк одного алгоритма.
    
    Returns:
        (время выполнения в секундах, результаты)
    """
    start_time = time.perf_counter()
    
    results = None
    for _ in range(iterations):
        results = algorithm(text, pattern)
    
    end_time = time.perf_counter()
    
    elapsed_time = end_time - start_time
    
    return elapsed_time, results


def run_comprehensive_benchmark() -> Dict:
    """Запускает комплексный бенчмарк всех алгоритмов."""
    
    print("\n" + "=" * 80)
    print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ АЛГОРИТМОВ ПОИСКА ПОДСТРОКИ")
    print("=" * 80)
    
    # Информация о системе
    print("\n" + "-" * 80)
    print("ХАРАКТЕРИСТИКИ ТЕСТОВОЙ МАШИНЫ:")
    print("-" * 80)
    print(f"Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"ОС: {platform.system()} {platform.release()}")
    print(f"Процессор: {platform.processor()}")
    print(f"Физическая память: {psutil.virtual_memory().total / (1024**3):.2f} GB")
    print(f"CPU count: {psutil.cpu_count()}")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "system_info": {
            "os": f"{platform.system()} {platform.release()}",
            "processor": platform.processor(),
            "ram_gb": psutil.virtual_memory().total / (1024**3),
            "cpu_count": psutil.cpu_count()
        },
        "benchmarks": {}
    }
    
    algorithms = {
        "KMP": kmp_search,
        "Z-function": z_search,
        "Boyer-Moore": boyer_moore_search,
        "Rabin-Karp": rabin_karp_search,
    }
    
    # Тестовые наборы
    test_sets = {
        "Случайная строка (малый алфавит)": {
            "text": generate_random_string(10000, alphabet_size=4),
            "pattern": generate_random_string(10, alphabet_size=4),
            "description": "Строка из 10000 символов, алфавит 4 символа"
        },
        "Случайная строка (большой алфавит)": {
            "text": generate_random_string(10000, alphabet_size=26),
            "pattern": generate_random_string(10, alphabet_size=26),
            "description": "Строка из 10000 символов, алфавит 26 символов"
        },
        "Периодическая строка": {
            "text": generate_periodic_string("ABC", 3000),
            "pattern": "ABCABC",
            "description": "Периодическая строка 'ABC' повторённая 3000 раз"
        },
        "Строка с повторениями": {
            "text": generate_repeating_string("A", 10000),
            "pattern": "AAA",
            "description": "10000 символов 'A'"
        },
        "Худший случай (нет совпадений)": {
            "text": generate_worst_case_string("ABC", 10000),
            "pattern": "ABC",
            "description": "Текст без паттерна (худший случай)"
        }
    }
    
    # Запуск бенчмарков
    for test_name, test_data in test_sets.items():
        print(f"\n" + "-" * 80)
        print(f"ТЕСТ: {test_name}")
        print("-" * 80)
        print(f"Описание: {test_data['description']}")
        print(f"Длина текста: {len(test_data['text'])}")
        print(f"Длина паттерна: {len(test_data['pattern'])}")
        print(f"Паттерн: {test_data['pattern'][:50]}{'...' if len(test_data['pattern']) > 50 else ''}")
        
        test_results = {}
        
        for algo_name, algo_func in algorithms.items():
            # Определяем количество итераций в зависимости от типа теста
            iterations = 100 if len(test_data['text']) < 1000 else 10
            
            elapsed_time, matches = benchmark_algorithm(
                algo_func,
                test_data['text'],
                test_data['pattern'],
                iterations=iterations
            )
            
            # Нормализуем время на одну итерацию
            time_per_iteration = elapsed_time / iterations
            
            test_results[algo_name] = {
                "total_time": elapsed_time,
                "time_per_iteration": time_per_iteration,
                "iterations": iterations,
                "matches_count": len(matches) if matches else 0
            }
            
            print(f"\n  {algo_name}:")
            print(f"    Время на итерацию: {time_per_iteration * 1e6:.3f} мкс")
            print(f"    Найдено вхождений: {len(matches) if matches else 0}")
        
        results["benchmarks"][test_name] = test_results
        
        # Определяем лучший алгоритм для этого теста
        fastest = min(test_results.items(), key=lambda x: x[1]['time_per_iteration'])
        print(f"\n  BEST: {fastest[0]} ({fastest[1]['time_per_iteration'] * 1e6:.3f} мкс)")
    
    return results


def run_scalability_test() -> Dict:
    """Тест масштабируемости: как меняется время с увеличением размера."""
    
    print("\n" + "=" * 80)
    print("ТЕСТ МАСШТАБИРУЕМОСТИ")
    print("=" * 80)
    
    results = {"scalability": {}}
    
    # Размеры текстов для тестирования
    text_sizes = [1000, 5000, 10000, 50000, 100000]
    pattern = "ABCDE"
    
    algorithms = {
        "KMP": kmp_search,
        "Z-function": z_search,
        "Rabin-Karp": rabin_karp_search,
    }
    
    print(f"\nПаттерн: '{pattern}'")
    print(f"Тип текста: Случайная строка (алфавит 5 символов)\n")
    
    for size in text_sizes:
        print(f"Размер текста: {size:6d} - ", end="", flush=True)
        text = generate_random_string(size, alphabet_size=5)
        
        size_results = {}
        
        for algo_name, algo_func in algorithms.items():
            start = time.perf_counter()
            algo_func(text, pattern)
            elapsed = time.perf_counter() - start
            
            size_results[algo_name] = elapsed * 1e6  # в микросекундах
            print(f"{algo_name}: {elapsed*1e6:8.2f} мкс | ", end="", flush=True)
        
        print()
        results["scalability"][size] = size_results
    
    return results


def run_worst_case_analysis() -> Dict:
    """Анализ поведения в худшем случае."""
    
    print("\n" + "=" * 80)
    print("АНАЛИЗ ХУДШЕГО СЛУЧАЯ")
    print("=" * 80)
    
    results = {"worst_case": {}}
    
    # Худший случай для КМП - паттерн в конце текста или не найден
    test_cases = {
        "Паттерн в начале": ("ABCDEF" + generate_random_string(5000, 4), "ABC"),
        "Паттерн в конце": (generate_random_string(5000, 4) + "ABCDEF", "ABC"),
        "Паттерн не найден": (generate_random_string(5000, 4), "XYZ"),
        "Много ложных совпадений": (generate_periodic_string("AABAAAB", 500), "AABAAC"),
    }
    
    algorithms = {
        "KMP": kmp_search,
        "Z-function": z_search,
        "Boyer-Moore": boyer_moore_search,
        "Rabin-Karp": rabin_karp_search,
    }
    
    for test_name, (text, pattern) in test_cases.items():
        print(f"\n{test_name}:")
        print(f"  Длина текста: {len(text)}, Паттерн: {pattern}")
        
        case_results = {}
        
        for algo_name, algo_func in algorithms.items():
            start = time.perf_counter()
            result = algo_func(text, pattern)
            elapsed = time.perf_counter() - start
            
            case_results[algo_name] = {
                "time_us": elapsed * 1e6,
                "matches": len(result) if result else 0
            }
            
            print(f"  {algo_name:15s}: {elapsed*1e6:10.2f} мкс ({len(result) if result else 0} совпадений)")
        
        results["worst_case"][test_name] = case_results
    
    return results


def run_pattern_size_analysis() -> Dict:
    """Анализ влияния длины паттерна на производительность."""
    
    print("\n" + "=" * 80)
    print("АНАЛИЗ ВЛИЯНИЯ ДЛИНЫ ПАТТЕРНА")
    print("=" * 80)
    
    results = {"pattern_size_influence": {}}
    
    text = generate_random_string(50000, alphabet_size=4)
    pattern_sizes = [1, 3, 5, 10, 20, 50, 100]
    
    algorithms = {
        "KMP": kmp_search,
        "Z-function": z_search,
        "Rabin-Karp": rabin_karp_search,
    }
    
    print(f"Размер текста: {len(text)}\n")
    
    for pattern_size in pattern_sizes:
        print(f"Размер паттерна: {pattern_size:3d} - ", end="", flush=True)
        pattern = generate_random_string(pattern_size, alphabet_size=4)
        
        size_results = {}
        
        for algo_name, algo_func in algorithms.items():
            start = time.perf_counter()
            algo_func(text, pattern)
            elapsed = time.perf_counter() - start
            
            size_results[algo_name] = elapsed * 1e6
            print(f"{algo_name}: {elapsed*1e6:8.2f} мкс | ", end="", flush=True)
        
        print()
        results["pattern_size_influence"][pattern_size] = size_results
    
    return results


# Главная функция
if __name__ == "__main__":
    all_results = {}
    
    # Основной бенчмарк
    all_results.update(run_comprehensive_benchmark())
    
    # Тест масштабируемости
    scalability = run_scalability_test()
    all_results.update(scalability)
    
    # Анализ худшего случая
    worst_case = run_worst_case_analysis()
    all_results.update(worst_case)
    
    # Анализ влияния размера паттерна
    pattern_analysis = run_pattern_size_analysis()
    all_results.update(pattern_analysis)
    
    # Сохранение результатов в JSON
    print("\n" + "=" * 80)
    print("СОХРАНЕНИЕ РЕЗУЛЬТАТОВ")
    print("=" * 80)
    
    with open("benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print("\n✓ Результаты сохранены в 'benchmark_results.json'")
