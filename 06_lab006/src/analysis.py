"""
Модуль: analysis.py
Описание: Анализ производительности операций в бинарном дереве поиска.
          Включает визуализацию дерева и сравнение времени поиска
          для сбалансированного и вырожденного дерева.
"""
import time  # O(1)
import random  # O(1)
import matplotlib.pyplot as plt  # O(1)
from binary_search_tree import BinarySearchTree  # O(1)

def visualize_tree(node, level=0, prefix="Root: "):  # O(n)
    """
    Текстовая визуализация дерева в консоли с иерархическим представлением.
    Параметры: node - узел для вывода, level - уровень углубления, prefix - префикс вывода
    Сложность: O(n), где n - количество узлов (посещаются все узлы)
    """
    if node is None:  # O(1)
        return
    
    print(" " * (level * 4) + prefix + str(node.value))  # O(1)
    
    if node.left is not None or node.right is not None:  # O(1)
        if node.left:  # O(1)
            visualize_tree(node.left, level + 1, "L--- ")  # O(n) для левого поддерева
        else:
            print(" " * ((level + 1) * 4) + "L--- None")  # O(1)
        
        if node.right:  # O(1)
            visualize_tree(node.right, level + 1, "R--- ")  # O(n) для правого поддерева
        else:
            print(" " * ((level + 1) * 4) + "R--- None")  # O(1)

def print_tree_ascii(node, prefix="", is_left=None):  # O(n)
    """
    ASCII визуализация дерева с красивыми линиями соединения.
    Параметры: node - узел для вывода, prefix - префикс строк, is_left - флаг позиции
    Сложность: O(n), где n - количество узлов (посещаются все узлы)
    """
    if node is None:  # O(1)
        return
    
    if is_left is None:  # O(1)
        print(node.value)  # O(1)
    else:
        print(prefix + ("├── " if is_left else "└── ") + str(node.value))  # O(1)
    
    children = [node.left, node.right]  # O(1)
    for i, child in enumerate(children):  # O(2) = O(1)
        is_last = (i == len(children) - 1)  # O(1)
        if child or i < len(children) - 1:  # O(1)
            extension = "    " if is_last else "│   "  # O(1)
            if child:  # O(1)
                print_tree_ascii(child, prefix + extension, is_last)  # O(n) для поддерева

def measure_search_time(bst, size, tree_type):  # O(n log n) в среднем, O(n²) в худшем случае
    """
    Измеряет время поиска всех элементов в дереве.
    Параметры: bst - дерево, size - размер дерева, tree_type - тип дерева
    Возвращает: время поиска в секундах
    Сложность: O(n log n) в среднем, O(n²) в худшем случае
    """
    # Заполнение дерева
    if tree_type == 'balanced':  # O(1)
        elements = random.sample(range(1, size + 1), size)  # O(n)
    else:  # для вырожденного дерева
        elements = list(range(1, size + 1))  # O(n)

    for value in elements:  # O(n)
        bst.insert(value)  # O(log n) в среднем, O(n) в худшем случае

    # Замер времени поиска
    start_time = time.time()  # O(1)
    for value in elements:  # O(n)
        bst.search(value)  # O(log n) в среднем, O(n) в худшем случае
    end_time = time.time()  # O(1)

    return end_time - start_time  # O(1)

def test_performance():  # O(k * n log n), где k - количество размеров, n - размер дерева
    """
    Тестирует производительность поиска в дереве для различных размеров.
    Строит и выводит графики сравнения времени поиска.
    Сложность: O(k * n log n) в среднем, где k - количество размеров
    """
    sizes = [100, 500, 1000, 5000, 10000]  # O(1)
    balanced_times = []  # O(1)
    degenerate_times = []  # O(1)

    for size in sizes:  # O(k), где k = 5
        bst_balanced = BinarySearchTree()  # O(1)
        bst_degenerate = BinarySearchTree()  # O(1)

        balanced_time = measure_search_time(bst_balanced, size, 'balanced')  # O(n log n)
        degenerate_time = measure_search_time(bst_degenerate, size, 'degenerate')  # O(n²)

        balanced_times.append(balanced_time)  # O(1)
        degenerate_times.append(degenerate_time)  # O(1)

    # Построение графиков
    plt.plot(sizes, balanced_times, label='Сбалансированное дерево')  # O(k)
    plt.plot(sizes, degenerate_times, label='Вырожденное дерево')  # O(k)
    plt.xlabel('Размер дерева')  # O(1)
    plt.ylabel('Время поиска (сек.)')  # O(1)
    plt.legend()  # O(1)
    plt.title('Сравнение времени поиска для сбалансированного и вырожденного дерева')  # O(1)
    plt.show()  # O(1)

if __name__ == "__main__":  # O(n)
    # Демонстрация визуализации дерева
    print("=" * 50)  # O(1)
    print("ТЕКСТОВАЯ ВИЗУАЛИЗАЦИЯ ДЕРЕВА")  # O(1)
    print("=" * 50)  # O(1)
    
    # Создание сбалансированного дерева
    print("\n1. Сбалансированное дерево:")  # O(1)
    print("-" * 30)  # O(1)
    bst_balanced = BinarySearchTree()  # O(1)
    balanced_values = [50, 30, 70, 20, 40, 60, 80]  # O(1)
    for value in balanced_values:  # O(7) = O(1)
        bst_balanced.insert(value)  # O(log n)
    
    print("\nИерархическая визуализация:")  # O(1)
    visualize_tree(bst_balanced.root)  # O(n)
    
    print("\n\nASCII визуализация:")  # O(1)
    print_tree_ascii(bst_balanced.root)  # O(n)
    
    # Создание вырожденного дерева
    print("\n\n2. Вырожденное дерево (в виде линии):")  # O(1)
    print("-" * 30)  # O(1)
    bst_degenerate = BinarySearchTree()  # O(1)
    degenerate_values = [1, 2, 3, 4, 5, 6]  # O(1)
    for value in degenerate_values:  # O(6) = O(1)
        bst_degenerate.insert(value)  # O(n) в худшем случае
    
    print("\nIерархическая визуализация:")  # O(1)
    visualize_tree(bst_degenerate.root)  # O(n)
    
    print("\n\nASCII визуализация:")  # O(1)
    print_tree_ascii(bst_degenerate.root)  # O(n)
    
    # Тест производительности
    print("\n\n" + "=" * 50)  # O(1)
    print("АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ")  # O(1)
    print("=" * 50)  # O(1)
    test_performance()  # O(k * n log n)
