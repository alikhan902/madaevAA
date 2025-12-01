"""
Модуль: binary_search_tree.py
Описание: Реализация бинарного дерева поиска (BST) с основными операциями
          вставки, поиска, удаления и проверки валидности дерева.
"""

class TreeNode:
    """
    Класс узла дерева.
    Атрибуты:
        value: значение узла
        left: левый потомок
        right: правый потомок
    """
    def __init__(self, value):  # O(1)
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    """
    Класс бинарного дерева поиска (BST).
    Основные операции: вставка, поиск, удаление элементов.
    """
    def __init__(self):  # O(1)
        self.root = None

    def insert(self, value):  # O(log n) в среднем, O(n) в худшем случае
        """
        Вставляет элемент в дерево.
        Параметры: value - значение для вставки
        """
        if not self.root:
            self.root = TreeNode(value)  # O(1)
            return
        
        current = self.root
        while True:  # O(h), где h - высота дерева
            if value < current.value:
                if current.left:
                    current = current.left  # O(1)
                else:
                    current.left = TreeNode(value)  # O(1)
                    break
            elif value > current.value:
                if current.right:
                    current = current.right  # O(1)
                else:
                    current.right = TreeNode(value)  # O(1)
                    break
            else:
                break
    
    def search(self, value):  # O(log n) в среднем, O(n) в худшем случае
        """
        Ищет элемент в дереве (итеративный подход).
        Параметры: value - значение для поиска
        Возвращает: узел с найденным значением или None
        """
        current = self.root
        while current:  # O(h), где h - высота дерева
            if current.value == value:
                return current  # O(1)
            elif value < current.value:
                current = current.left  # O(1)
            else:
                current = current.right  # O(1)
        return None  # O(1)

    def _search_recursive(self, node, value):  # O(log n) в среднем, O(n) в худшем случае
        """
        Ищет элемент в дереве (рекурсивный подход).
        Параметры: node - текущий узел, value - значение для поиска
        Возвращает: узел с найденным значением или None
        """
        if node is None or node.value == value:
            return node  # O(1)
        if value < node.value:
            return self._search_recursive(node.left, value)  # O(h)
        return self._search_recursive(node.right, value)  # O(h)

    def delete(self, value):  # O(log n) в среднем, O(n) в худшем случае
        """
        Удаляет элемент из дерева.
        Параметры: value - значение для удаления
        """
        self.root = self._delete_recursive(self.root, value)  # O(h)

    def _delete_recursive(self, node, value):  # O(log n) в среднем, O(n) в худшем случае
        """
        Рекурсивная функция удаления элемента.
        Обрабатывает три случая: узел без потомков, с одним или двумя потомками.
        """
        if node is None:
            return node  # O(1)
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)  # O(h)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)  # O(h)
        else:
            # Узел с одним или без потомков
            if node.left is None:
                return node.right  # O(1)
            elif node.right is None:
                return node.left  # O(1)
            # Узел с двумя потомками: найти минимум в правом поддереве
            min_larger_node = self._find_min(node.right)  # O(h)
            node.value = min_larger_node.value  # O(1)
            node.right = self._delete_recursive(node.right, min_larger_node.value)  # O(h)
        return node  # O(1)

    def _find_min(self, node):  # O(h), где h - высота поддерева
        """
        Находит узел с минимальным значением в поддереве.
        Минимум всегда находится в самом левом узле.
        """
        current = node
        while current.left is not None:  # O(h)
            current = current.left  # O(1)
        return current  # O(1)

    def _find_max(self, node):  # O(h), где h - высота поддерева
        """
        Находит узел с максимальным значением в поддереве.
        Максимум всегда находится в самом правом узле.
        """
        current = node
        while current.right is not None:  # O(h)
            current = current.right  # O(1)
        return current  # O(1)

    def is_valid_bst(self):  # O(n)
        """
        Проверяет, является ли дерево корректным BST.
        Возвращает: True если дерево корректное, иначе False
        """
        return self._is_valid_bst(self.root, float('-inf'), float('inf'))  # O(n)

    def _is_valid_bst(self, node, min_value, max_value):  # O(n)
        """
        Рекурсивная проверка корректности BST.
        Посещает каждый узел один раз и проверяет условия BST.
        """
        if node is None:
            return True  # O(1)
        if node.value <= min_value or node.value >= max_value:
            return False  # O(1)
        return self._is_valid_bst(node.left, min_value, node.value) and \
               self._is_valid_bst(node.right, node.value, max_value)  # O(n)

    def height(self, node):  # O(n)
        """
        Вычисляет высоту дерева.
        Параметры: node - корень поддерева
        Возвращает: высота дерева (количество уровней)
        """
        if node is None:
            return 0  # O(1)
        left_height = self.height(node.left)  # O(n)
        right_height = self.height(node.right)  # O(n)
        return max(left_height, right_height) + 1  # O(1)
