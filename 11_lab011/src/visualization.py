"""
Визуализация работы алгоритмов и результатов бенчмарков.

Создаёт графики для:
1. Сравнения времени выполнения алгоритмов
2. Масштабируемости с ростом размера текста
3. Влияния длины паттерна на производительность
4. Визуализации префикс-функции и Z-функции
"""

import json
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path

# Установить кириллицу в matplotlib
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

from prefix_function import compute_prefix_function, compute_prefix_function_verbose
from z_function import compute_z_function, compute_z_function_verbose


def plot_algorithm_comparison():
    """График сравнения алгоритмов на различных типах данных."""
    
    # Данные из benchmark_results.json
    try:
        with open("benchmark_results.json", "r", encoding="utf-8") as f:
            results = json.load(f)
    except FileNotFoundError:
        print("benchmark_results.json не найден. Запустите performance_analysis.py")
        return
    
    benchmarks = results.get("benchmarks", {})
    
    # Подготовка данных
    algorithms = ["KMP", "Z-function", "Boyer-Moore", "Rabin-Karp"]
    
    # Данные для каждого теста
    test_names = list(benchmarks.keys())
    
    for algo in algorithms:
        times = []
        for test_name in test_names:
            if test_name in benchmarks:
                time_us = benchmarks[test_name].get(algo, {}).get("time_per_iteration", 0)
                times.append(time_us)
        
        if times:
            break
    
    # Создание графика
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x_pos = range(len(test_names))
    width = 0.2
    
    for i, algo in enumerate(algorithms):
        times = []
        for test_name in test_names:
            if test_name in benchmarks:
                time_us = benchmarks[test_name].get(algo, {}).get("time_per_iteration", 0)
                times.append(time_us)
        
        ax.bar([p + i * width for p in x_pos], times, width, label=algo)
    
    ax.set_xlabel("Test Type", fontsize=12)
    ax.set_ylabel("Time (microseconds)", fontsize=12)
    ax.set_title("String Matching Algorithms Comparison", fontsize=14, fontweight='bold')
    ax.set_xticks([p + width * 1.5 for p in x_pos])
    ax.set_xticklabels([name[:20] for name in test_names], rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("01_algorithm_comparison.png", dpi=150)
    print("Сохранён график: 01_algorithm_comparison.png")
    plt.close()


def plot_scalability():
    """График масштабируемости алгоритмов."""
    
    try:
        with open("benchmark_results.json", "r", encoding="utf-8") as f:
            results = json.load(f)
    except FileNotFoundError:
        print("benchmark_results.json не найден.")
        return
    
    scalability = results.get("scalability", {})
    
    if not scalability:
        print("Данные масштабируемости не найдены.")
        return
    
    # Подготовка данных
    text_sizes = sorted([int(k) for k in scalability.keys()])
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    algorithms = ["KMP", "Z-function", "Rabin-Karp"]
    
    for algo in algorithms:
        times = [scalability[str(size)].get(algo, 0) for size in text_sizes]
        ax.plot(text_sizes, times, marker='o', linewidth=2, markersize=8, label=algo)
    
    ax.set_xlabel("Text Size (characters)", fontsize=12)
    ax.set_ylabel("Time (microseconds)", fontsize=12)
    ax.set_title("Algorithm Scalability", fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # Логарифмическая шкала для лучшей видимости
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig("02_scalability.png", dpi=150)
    print("Сохранён график: 02_scalability.png")
    plt.close()


def plot_pattern_size_influence():
    """График влияния размера паттерна на производительность."""
    
    try:
        with open("benchmark_results.json", "r", encoding="utf-8") as f:
            results = json.load(f)
    except FileNotFoundError:
        return
    
    pattern_data = results.get("pattern_size_influence", {})
    
    if not pattern_data:
        return
    
    pattern_sizes = sorted([int(k) for k in pattern_data.keys()])
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    algorithms = ["KMP", "Z-function", "Rabin-Karp"]
    
    for algo in algorithms:
        times = [pattern_data[str(size)].get(algo, 0) for size in pattern_sizes]
        ax.plot(pattern_sizes, times, marker='s', linewidth=2, markersize=8, label=algo)
    
    ax.set_xlabel("Pattern Size (characters)", fontsize=12)
    ax.set_ylabel("Time (microseconds)", fontsize=12)
    ax.set_title("Pattern Size Influence on Performance", fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("03_pattern_size_influence.png", dpi=150)
    print("Сохранён график: 03_pattern_size_influence.png")
    plt.close()


def plot_worst_case_analysis():
    """График анализа худшего случая."""
    
    try:
        with open("benchmark_results.json", "r", encoding="utf-8") as f:
            results = json.load(f)
    except FileNotFoundError:
        return
    
    worst_case = results.get("worst_case", {})
    
    if not worst_case:
        return
    
    test_cases = list(worst_case.keys())
    algorithms = ["KMP", "Z-function", "Boyer-Moore", "Rabin-Karp"]
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    x_pos = range(len(test_cases))
    width = 0.2
    
    for i, algo in enumerate(algorithms):
        times = []
        for test_case in test_cases:
            time_us = worst_case[test_case].get(algo, {}).get("time_us", 0)
            times.append(time_us)
        
        ax.bar([p + i * width for p in x_pos], times, width, label=algo)
    
    ax.set_xlabel("Test Case", fontsize=12)
    ax.set_ylabel("Time (microseconds)", fontsize=12)
    ax.set_title("Worst Case Analysis", fontsize=14, fontweight='bold')
    ax.set_xticks([p + width * 1.5 for p in x_pos])
    ax.set_xticklabels(test_cases, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig("04_worst_case_analysis.png", dpi=150)
    print("Сохранён график: 04_worst_case_analysis.png")
    plt.close()


def visualize_prefix_function():
    """Визуализация работы префикс-функции."""
    
    test_strings = [
        "ABAB",
        "AAAA",
        "ABCABDABC",
        "AABAAAB",
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, s in enumerate(test_strings):
        pi = compute_prefix_function(s)
        
        ax = axes[idx]
        
        # График со строкой и значениями pi
        x = range(len(s))
        ax.bar(x, pi, color='steelblue', alpha=0.7, edgecolor='black')
        
        # Добавить буквы под графиком
        for i, char in enumerate(s):
            ax.text(i, -0.5, char, ha='center', fontsize=12, fontweight='bold')
        
        # Добавить значения на столбцы
        for i, val in enumerate(pi):
            ax.text(i, val + 0.1, str(val), ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel("Position", fontsize=11)
        ax.set_ylabel("Prefix Function Value", fontsize=11)
        ax.set_title(f"Prefix Function for '{s}'", fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_ylim(-1, max(pi) + 1 if pi else 1)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig("05_prefix_function_visualization.png", dpi=150)
    print("Сохранён график: 05_prefix_function_visualization.png")
    plt.close()


def visualize_z_function():
    """Визуализация работы Z-функции."""
    
    test_strings = [
        "ABAB",
        "AAAA",
        "ABCDA",
        "AABAAAB",
    ]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()
    
    for idx, s in enumerate(test_strings):
        z = compute_z_function(s)
        
        ax = axes[idx]
        
        # График со строкой и значениями Z
        x = range(len(s))
        colors = ['green' if z[i] > 0 else 'lightcoral' for i in range(len(z))]
        ax.bar(x, z, color=colors, alpha=0.7, edgecolor='black')
        
        # Добавить буквы под графиком
        for i, char in enumerate(s):
            ax.text(i, -0.5, char, ha='center', fontsize=12, fontweight='bold')
        
        # Добавить значения на столбцы
        for i, val in enumerate(z):
            if val > 0:
                ax.text(i, val + 0.1, str(val), ha='center', va='bottom', fontsize=10)
        
        ax.set_xlabel("Position", fontsize=11)
        ax.set_ylabel("Z-Function Value", fontsize=11)
        ax.set_title(f"Z-Function for '{s}'", fontsize=12, fontweight='bold')
        ax.set_xticks(x)
        ax.set_ylim(-1, max(z) + 1 if z else 1)
        ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig("06_z_function_visualization.png", dpi=150)
    print("Сохранён график: 06_z_function_visualization.png")
    plt.close()


def create_summary_visualization():
    """Создание сводной визуализации с ключевыми результатами."""
    
    fig = plt.figure(figsize=(16, 10))
    
    # Заголовок
    fig.suptitle('String Matching Algorithms - Performance Summary', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # Подзаголовок с информацией о системе
    try:
        with open("benchmark_results.json", "r", encoding="utf-8") as f:
            results = json.load(f)
            system_info = results.get("system_info", {})
            
            info_text = (f"System: {system_info.get('os', 'Unknown')} | "
                        f"CPU: {system_info.get('cpu_count', '?')} cores | "
                        f"RAM: {system_info.get('ram_gb', 0):.1f} GB | "
                        f"Timestamp: {results.get('timestamp', 'Unknown')[:10]}")
            fig.text(0.5, 0.955, info_text, ha='center', fontsize=10, style='italic')
    except:
        pass
    
    # Создание подграфиков
    gs = fig.add_gridspec(3, 2, left=0.08, right=0.95, top=0.93, bottom=0.05, hspace=0.3, wspace=0.3)
    
    # Пустой размещение для информационного текста
    ax_info = fig.add_subplot(gs[0, :])
    ax_info.axis('off')
    
    info_text = """
    KEY FINDINGS:
    • KMP (Knuth-Morris-Pratt): Best for general cases and periodic strings
    • Boyer-Moore: Excellent for large alphabets and non-matching cases
    • Z-Function: Efficient for pattern analysis and periodicity checking
    • Rabin-Karp: Useful for multiple pattern matching
    """
    ax_info.text(0.1, 0.5, info_text, fontsize=11, verticalalignment='center',
                family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Остальные графики
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1])
    ax3 = fig.add_subplot(gs[2, 0])
    ax4 = fig.add_subplot(gs[2, 1])
    
    # Примеры визуализации функций
    # Префикс-функция
    s1 = "ABCABDABC"
    pi = compute_prefix_function(s1)
    ax1.bar(range(len(s1)), pi, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_title(f"Prefix Function: '{s1}'", fontweight='bold')
    ax1.set_ylabel("Value")
    ax1.set_xticks(range(len(s1)))
    ax1.set_xticklabels(list(s1))
    
    # Z-функция
    s2 = "AABAAAB"
    z = compute_z_function(s2)
    colors = ['green' if z[i] > 0 else 'lightcoral' for i in range(len(z))]
    ax2.bar(range(len(s2)), z, color=colors, alpha=0.7, edgecolor='black')
    ax2.set_title(f"Z-Function: '{s2}'", fontweight='bold')
    ax2.set_ylabel("Value")
    ax2.set_xticks(range(len(s2)))
    ax2.set_xticklabels(list(s2))
    
    # Временная сложность таблица
    ax3.axis('off')
    complexity_data = [
        ['Algorithm', 'Time', 'Space', 'Best Case'],
        ['KMP', 'O(n+m)', 'O(m)', 'Small alphabets'],
        ['Z-Function', 'O(n+m)', 'O(n)', 'Pattern analysis'],
        ['Boyer-Moore', 'O(n/m)', 'O(|Σ|)', 'Large alphabets'],
        ['Rabin-Karp', 'O(n+m)', 'O(1)', 'Multiple patterns'],
    ]
    
    table = ax3.table(cellText=complexity_data, cellLoc='center', loc='center',
                     colWidths=[0.25, 0.25, 0.25, 0.25])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Стиль заголовка
    for i in range(len(complexity_data[0])):
        table[(0, i)].set_facecolor('#40466e')
        table[(0, i)].set_text_props(weight='bold', color='white')
    
    ax3.set_title("Algorithm Complexity & Characteristics", fontweight='bold', pad=20)
    
    # Рекомендации
    ax4.axis('off')
    recommendations = """
    RECOMMENDATIONS:
    
    • Small patterns or periodic texts
      → Use KMP or Z-Function
    
    • Large alphabet (DNA, text)
      → Use Boyer-Moore
    
    • Multiple patterns simultaneously
      → Use Rabin-Karp
    
    • Real-time requirements
      → Use Boyer-Moore (best avg case)
    
    • Memory constraints
      → Use Rabin-Karp (O(1) space)
    """
    ax4.text(0.05, 0.95, recommendations, fontsize=10, verticalalignment='top',
            family='monospace', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    plt.savefig("00_summary_visualization.png", dpi=150, bbox_inches='tight')
    print("Сохранён график: 00_summary_visualization.png")
    plt.close()


# Главная функция
if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("СОЗДАНИЕ ГРАФИКОВ И ВИЗУАЛИЗАЦИЙ")
    print("=" * 80)
    
    print("\nСоздание сводной визуализации...")
    create_summary_visualization()
    
    print("\nСоздание графика сравнения алгоритмов...")
    plot_algorithm_comparison()
    
    print("\nСоздание графика масштабируемости...")
    plot_scalability()
    
    print("\nСоздание графика влияния размера паттерна...")
    plot_pattern_size_influence()
    
    print("\nСоздание графика анализа худшего случая...")
    plot_worst_case_analysis()
    
    print("\nСоздание визуализации префикс-функции...")
    visualize_prefix_function()
    
    print("\nСоздание визуализации Z-функции...")
    visualize_z_function()
    
    print("\n" + "=" * 80)
    print("ВСЕ ГРАФИКИ СОЗДАНЫ УСПЕШНО")
    print("=" * 80)
    
    # Список созданных файлов
    print("\nСозданные файлы:")
    png_files = list(Path(".").glob("*.png"))
    for i, file in enumerate(sorted(png_files), 1):
        print(f"  {i}. {file.name}")
