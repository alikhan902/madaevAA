"""
Визуализация жадных алгоритмов.

Этот модуль содержит функции для визуализации:
1. Дерева Хаффмана
2. Графиков производительности
3. Процесса построения MST
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import List, Tuple
import networkx as nx
from greedy_algorithms import HuffmanNode, huffman_coding


def draw_huffman_tree(root: HuffmanNode,
                      output_file: str = 'huffman_tree.png') -> None:
    """
    Рисует дерево Хаффмана с помощью matplotlib.

    Args:
        root: Корень дерева Хаффмана.
        output_file: Путь для сохранения изображения.
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(-1, 15)
    ax.set_ylim(-1, 10)
    ax.axis('off')

    # Вычисляем позиции узлов
    positions = {}
    node_id = [0]

    def get_node_id():
        node_id[0] += 1
        return node_id[0]

    def assign_positions(node, x, y, offset_x):
        """Рекурсивно назначает позиции для узлов дерева."""
        if node is None:
            return

        node_key = id(node)
        positions[node_key] = (x, y)

        if node.left is not None and node.right is not None:
            # Расстояние между левым и правым потомком
            new_offset = offset_x / 2

            # Левый потомок
            assign_positions(node.left, x - new_offset, y - 1.5, new_offset)
            # Правый потомок
            assign_positions(node.right, x + new_offset, y - 1.5, new_offset)

            # Рисуем линии к потомкам
            left_x, left_y = positions[id(node.left)]
            right_x, right_y = positions[id(node.right)]

            ax.plot([x, left_x], [y, left_y], 'k-', linewidth=2)
            ax.plot([x, right_x], [y, right_y], 'k-', linewidth=2)

    def draw_nodes(node):
        """Рекурсивно рисует узлы."""
        if node is None:
            return

        x, y = positions[id(node)]

        # Цвет узла
        if node.char is not None:
            # Листовой узел (символ)
            color = '#90EE90'  # Светло-зеленый
            ax.add_patch(mpatches.Circle((x, y), 0.4, color=color,
                                        edgecolor='black', linewidth=2))
            ax.text(x, y, f"'{node.char}'\n{node.freq}",
                   ha='center', va='center', fontsize=10, fontweight='bold')
        else:
            # Внутренний узел (частота)
            color = '#87CEEB'  # Небесно-голубой
            ax.add_patch(mpatches.Circle((x, y), 0.4, color=color,
                                        edgecolor='black', linewidth=2))
            ax.text(x, y, f"{node.freq}",
                   ha='center', va='center', fontsize=9, fontweight='bold')

        # Рекурсивно рисуем потомков
        draw_nodes(node.left)
        draw_nodes(node.right)

    # Начинаем с корня в верхней середине
    assign_positions(root, 7, 8, 3)
    draw_nodes(root)

    plt.title('Дерево кодирования Хаффмана', fontsize=16, fontweight='bold',
              pad=20)
    plt.text(7, -0.8, 'Зеленые узлы - символы (листья), голубые - суммы частот',
            ha='center', fontsize=11, style='italic')

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✓ Дерево Хаффмана сохранено как '{output_file}'")
    plt.close()


def visualize_huffman_process(text: str,
                              output_file: str = 'huffman_process.png') -> None:
    """
    Визуализирует процесс построения дерева Хаффмана пошагово.

    Args:
        text: Исходный текст для кодирования.
        output_file: Путь для сохранения изображения.
    """
    from collections import defaultdict
    import heapq

    # Подсчитываем частоты
    freq_dict = defaultdict(int)
    for char in text:
        freq_dict[char] += 1

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Процесс построения дерева Хаффмана', fontsize=16,
                 fontweight='bold')

    # Шаг 1: Исходные частоты
    ax = axes[0, 0]
    chars = sorted(freq_dict.keys())
    freqs = [freq_dict[c] for c in chars]
    bars = ax.bar(chars, freqs, color='#87CEEB', edgecolor='black', linewidth=1.5)
    ax.set_ylabel('Частота', fontsize=11)
    ax.set_title('Шаг 1: Исходные частоты символов', fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    # Добавляем значения на столбцы
    for bar, freq in zip(bars, freqs):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               f'{int(height)}', ha='center', va='bottom', fontsize=10)

    # Шаг 2: Очередь и объединение (в виде таблицы)
    ax = axes[0, 1]
    ax.axis('off')
    ax.text(0.5, 0.95, 'Шаг 2: Объединение узлов с минимальными частотами',
           ha='center', va='top', fontsize=12, fontweight='bold',
           transform=ax.transAxes)

    # Создаем таблицу с процессом объединения
    sorted_chars = sorted(freq_dict.items(), key=lambda x: x[1])
    text_lines = []
    text_lines.append("Исходная очередь (по частоте):")
    for char, freq in sorted_chars:
        text_lines.append(f"  '{char}': {freq}")

    text_lines.append("\nПроцесс объединения:")
    step = 1
    remaining = list(sorted_chars)
    while len(remaining) > 1:
        remaining.sort(key=lambda x: x[1])
        a, b = remaining[0], remaining[1]
        remaining = remaining[2:]
        combined = (f"({a[0]}+{b[0]})", a[1] + b[1])
        remaining.append(combined)
        if step <= 3:  # Показываем первые 3 шага
            text_lines.append(f"  Шаг {step}: объединяем {a[0]}({a[1]}) + "
                            f"{b[0]}({b[1]}) = {a[1] + b[1]}")
            step += 1

    if len(remaining) > 1:
        text_lines.append("  ...")

    full_text = '\n'.join(text_lines)
    ax.text(0.05, 0.85, full_text, ha='left', va='top', fontsize=9,
           family='monospace', transform=ax.transAxes)

    # Шаг 3: Коды Хаффмана
    ax = axes[1, 0]
    ax.axis('off')
    ax.text(0.5, 0.95, 'Шаг 3: Сгенерированные коды',
           ha='center', va='top', fontsize=12, fontweight='bold',
           transform=ax.transAxes)

    codes, root = huffman_coding(text)
    code_lines = []
    for char in sorted(codes.keys()):
        code = codes[char]
        code_lines.append(f"  '{char}': {code:>10s} (длина {len(code)})")

    codes_text = '\n'.join(code_lines)
    ax.text(0.05, 0.85, codes_text, ha='left', va='top', fontsize=10,
           family='monospace', transform=ax.transAxes)

    # Шаг 4: Статистика сжатия
    ax = axes[1, 1]
    ax.axis('off')
    ax.text(0.5, 0.95, 'Шаг 4: Эффективность сжатия',
           ha='center', va='top', fontsize=12, fontweight='bold',
           transform=ax.transAxes)

    # Вычисляем размер до и после
    original_bits = len(text) * 8
    encoded_bits = sum(len(code) * freq_dict[char] for char, code in codes.items())
    compression_ratio = (1 - encoded_bits / original_bits) * 100

    stats_text = f"""Текст: "{text}"
Длина: {len(text)} символов
Уникальные символы: {len(codes)}

Размер:
  Оригинал: {original_bits} бит ({original_bits // 8} байт)
  Хаффман: {encoded_bits} бит ({encoded_bits // 8} байт)

Эффективность:
  Сжатие: {compression_ratio:.1f}%
  Средняя длина кода: {encoded_bits / len(text):.2f} бит/символ
"""
    ax.text(0.05, 0.85, stats_text, ha='left', va='top', fontsize=10,
           family='monospace', transform=ax.transAxes)

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✓ Процесс Хаффмана сохранен как '{output_file}'")
    plt.close()


def visualize_interval_scheduling(intervals: List[Tuple[int, int]],
                                  output_file: str = 'interval_scheduling.png') -> None:
    """
    Визуализирует процесс выбора интервалов.

    Args:
        intervals: Список интервалов (start, end).
        output_file: Путь для сохранения изображения.
    """
    from greedy_algorithms import interval_scheduling

    selected = interval_scheduling(intervals)

    fig, ax = plt.subplots(figsize=(12, 8))

    # Сортируем интервалы по времени начала для визуализации
    all_intervals = sorted(enumerate(intervals), key=lambda x: x[1][0])

    # Рисуем интервалы
    y_pos = 0
    colors_used = set()

    for idx, (orig_idx, (start, end)) in enumerate(all_intervals):
        is_selected = (start, end) in selected

        if is_selected:
            color = '#90EE90'  # Зеленый для выбранных
            colors_used.add(orig_idx)
            linewidth = 3
            label = "Выбран" if orig_idx not in colors_used or idx == 0 else ""
        else:
            color = '#FFB6C6'  # Розовый для отклоненных
            linewidth = 1

        # Рисуем прямоугольник для интервала
        rect = mpatches.Rectangle((start, y_pos - 0.3), end - start, 0.6,
                                 facecolor=color, edgecolor='black',
                                 linewidth=linewidth)
        ax.add_patch(rect)

        # Добавляем метку
        ax.text((start + end) / 2, y_pos, f"({start},{end})",
               ha='center', va='center', fontsize=9, fontweight='bold')

        y_pos += 1

    ax.set_xlim(min(min(s, e) for s, e in intervals) - 1,
               max(max(s, e) for s, e in intervals) + 1)
    ax.set_ylim(-1, len(intervals))
    ax.set_xlabel('Время', fontsize=12)
    ax.set_ylabel('Интервалы', fontsize=12)
    ax.set_title('Задача о выборе заявок (Interval Scheduling)', fontsize=14,
                fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')

    # Легенда
    selected_patch = mpatches.Patch(facecolor='#90EE90', edgecolor='black',
                                    label=f'Выбрано ({len(selected)} интервалов)')
    rejected_patch = mpatches.Patch(facecolor='#FFB6C6', edgecolor='black',
                                   label=f'Отклонено ({len(intervals) - len(selected)} интервалов)')
    ax.legend(handles=[selected_patch, rejected_patch], loc='upper right',
             fontsize=11)

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✓ Interval Scheduling визуализирован как '{output_file}'")
    plt.close()


def visualize_mst(vertices: List[str],
                  edges: List[Tuple[str, str, int]],
                  mst_edges: List[Tuple[str, str, int]],
                  title: str = "Минимальное остовное дерево",
                  output_file: str = 'mst.png') -> None:
    """
    Визуализирует граф и его MST.

    Args:
        vertices: Список вершин.
        edges: Список всех ребер графа.
        mst_edges: Список ребер MST.
        title: Заголовок визуализации.
        output_file: Путь для сохранения изображения.
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Создаем NetworkX графы
    G_full = nx.Graph()
    G_full.add_nodes_from(vertices)
    for u, v, w in edges:
        G_full.add_edge(u, v, weight=w)

    G_mst = nx.Graph()
    G_mst.add_nodes_from(vertices)
    for u, v, w in mst_edges:
        G_mst.add_edge(u, v, weight=w)

    # Используем одинаковую раскладку для обоих графов
    pos = nx.spring_layout(G_full, seed=42, k=2, iterations=50)

    # График 1: Полный граф
    nx.draw_networkx_nodes(G_full, pos, node_color='lightblue',
                          node_size=800, ax=ax1)
    nx.draw_networkx_labels(G_full, pos, font_size=12, font_weight='bold',
                           ax=ax1)
    nx.draw_networkx_edges(G_full, pos, width=2, ax=ax1, alpha=0.5)

    # Добавляем метки весов ребер
    edge_labels = {(u, v): w for u, v, w in edges}
    nx.draw_networkx_edge_labels(G_full, pos, edge_labels, font_size=9,
                                ax=ax1)
    ax1.set_title('Полный граф', fontsize=12, fontweight='bold')
    ax1.axis('off')

    # График 2: MST
    nx.draw_networkx_nodes(G_mst, pos, node_color='lightgreen',
                          node_size=800, ax=ax2)
    nx.draw_networkx_labels(G_mst, pos, font_size=12, font_weight='bold',
                           ax=ax2)
    nx.draw_networkx_edges(G_mst, pos, width=3, ax=ax2, edge_color='red',
                          alpha=0.8)

    # Добавляем метки весов для MST
    mst_labels = {(u, v): w for u, v, w in mst_edges}
    nx.draw_networkx_edge_labels(G_mst, pos, mst_labels, font_size=9,
                                ax=ax2)
    ax2.set_title('Минимальное остовное дерево', fontsize=12,
                 fontweight='bold')
    ax2.axis('off')

    # Общий заголовок и информация
    total_weight = sum(w for _, _, w in mst_edges)
    fig.suptitle(f'{title} (общий вес: {total_weight})',
                fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"✓ MST визуализирован как '{output_file}'")
    plt.close()


def create_comparison_plot() -> None:
    """
    Создает сравнительный график сложностей алгоритмов.
    """
    algorithms = ['Interval\nScheduling', 'Fractional\nKnapsack',
                 'Huffman', 'Prim MST', 'Kruskal MST']
    complexities = [np.log(100), np.log(100),  # O(n log n)
                   np.log(100), 100 * np.log(100),  # O(E log V)
                   100 * np.log(100)]  # O(E log E)

    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ['#90EE90', '#87CEEB', '#FFD700', '#FFA07A', '#DDA0DD']
    bars = ax.bar(algorithms, complexities, color=colors, edgecolor='black',
                 linewidth=1.5)

    ax.set_ylabel('Относительная временная сложность', fontsize=12)
    ax.set_title('Сравнение временной сложности жадных алгоритмов', fontsize=14,
                fontweight='bold')
    ax.grid(axis='y', alpha=0.3)

    # Добавляем метки
    complexity_labels = ['O(n log n)', 'O(n log n)', 'O(n log n)',
                        'O(E log V)', 'O(E log E)']
    for bar, label in zip(bars, complexity_labels):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
               label, ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig('algorithms_complexity.png', dpi=150, bbox_inches='tight')
    print("✓ График сложности сохранен как 'algorithms_complexity.png'")
    plt.close()


def main() -> None:
    """Главная функция для создания всех визуализаций."""
    print("\n" + "=" * 80)
    print("СОЗДАНИЕ ВИЗУАЛИЗАЦИЙ ЖАДНЫХ АЛГОРИТМОВ")
    print("=" * 80 + "\n")

    # 1. Дерево Хаффмана
    print("1. Визуализация дерева Хаффмана...")
    text = "aaaabbcccd"
    codes, root = huffman_coding(text)
    draw_huffman_tree(root, 'huffman_tree.png')

    # 2. Процесс построения Хаффмана
    print("2. Визуализация процесса Хаффмана...")
    visualize_huffman_process(text, 'huffman_process.png')

    # 3. Interval Scheduling
    print("3. Визуализация Interval Scheduling...")
    intervals = [(0, 5), (1, 3), (2, 4), (4, 7), (6, 9), (8, 11)]
    visualize_interval_scheduling(intervals, 'interval_scheduling.png')

    # 4. MST
    print("4. Визуализация MST...")
    vertices = ['A', 'B', 'C', 'D']
    all_edges = [('A', 'B', 4), ('A', 'C', 2), ('B', 'C', 1),
                 ('B', 'D', 5), ('C', 'D', 8)]
    mst_edges = [('A', 'C', 2), ('B', 'C', 1), ('B', 'D', 5)]
    visualize_mst(vertices, all_edges, mst_edges, output_file='mst.png')

    # 5. График сложностей
    print("5. Создание графика сложностей...")
    create_comparison_plot()

    print("\n" + "=" * 80)
    print("ВСЕ ВИЗУАЛИЗАЦИИ СОЗДАНЫ")
    print("=" * 80 + "\n")
    print("Созданные файлы:")
    print("  - huffman_tree.png: Дерево кодирования Хаффмана")
    print("  - huffman_process.png: Процесс построения дерева")
    print("  - interval_scheduling.png: Выбор интервалов")
    print("  - mst.png: Минимальное остовное дерево")
    print("  - algorithms_complexity.png: Сравнение сложностей")
    print()


if __name__ == '__main__':
    main()
