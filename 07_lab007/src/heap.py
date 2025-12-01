# heap.py
# Реализация минимальной/максимальной кучи с поясняющими комментариями

class Heap:
    def __init__(self, is_min=True):  # O(1) создание объекта кучи
        self.is_min = is_min  # O(1) True для Min-Heap, False для Max-Heap
        self.heap = []  # O(1) внутреннее представление кучи в виде списка

    def _sift_up(self, index):  # O(log n) всплытие элемента вверх по дереву
        """Всплытие элемента (восстановление свойства кучи)."""  # O(1)
        parent = (index - 1) // 2  # O(1) вычисление индекса родителя
        while index > 0 and self._compare(self.heap[index], self.heap[parent]):  # O(log n) цикл по высоте кучи
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]  # O(1) обмен элементов
            index = parent  # O(1) переход вверх
            parent = (index - 1) // 2  # O(1) вычисление нового родителя

    def _sift_down(self, index):  # O(log n) погружение элемента вниз по дереву
        """Погружение элемента (восстановление свойства кучи)."""  # O(1)
        size = len(self.heap)  # O(1) получение размера кучи
        left = 2 * index + 1  # O(1) индекс левого потомка
        right = 2 * index + 2  # O(1) индекс правого потомка
        largest_or_smallest = index  # O(1) текущий кандидат

        if left < size and self._compare(self.heap[left], self.heap[largest_or_smallest]):  # O(1)
            largest_or_smallest = left  # O(1) обновление кандидата
        if right < size and self._compare(self.heap[right], self.heap[largest_or_smallest]):  # O(1)
            largest_or_smallest = right  # O(1) обновление кандидата

        if largest_or_smallest != index:  # O(1) проверка необходимости обмена
            self.heap[index], self.heap[largest_or_smallest] = self.heap[largest_or_smallest], self.heap[index]  # O(1) обмен
            self._sift_down(largest_or_smallest)  # O(log n) рекурсивный вызов

    def _compare(self, child, parent):  # O(1) сравнение двух элементов по правилу кучи
        """Сравниваем элементы в зависимости от типа кучи."""  # O(1)
        if self.is_min:  # O(1) для Min-Heap сравнение меньше
            return child < parent  # O(1)
        else:  # O(1) для Max-Heap сравнение больше
            return child > parent  # O(1)

    def insert(self, value):  # O(log n) вставка значения в кучу
        """Вставка нового элемента в кучу."""  # O(1)
        self.heap.append(value)  # O(1) добавление в конец списка
        self._sift_up(len(self.heap) - 1)  # O(log n) восстановление свойства кучи

    def extract(self):  # O(log n) извлечение корневого элемента
        """Извлечение корня кучи."""  # O(1)
        if len(self.heap) == 0:  # O(1) проверка на пустоту
            raise IndexError("Extract from an empty heap.")  # O(1) возбуждение исключения
        root = self.heap[0]  # O(1) сохранение корня
        last_element = self.heap.pop()  # O(1) удаление последнего элемента
        if len(self.heap) > 0:  # O(1) если остались элементы
            self.heap[0] = last_element  # O(1) перемещение последнего в корень
            self._sift_down(0)  # O(log n) восстановление свойства кучи
        return root  # O(1) возвращаем корень

    def peek(self):  # O(1) просмотр корня без удаления
        """Просмотр корня кучи."""  # O(1)
        if len(self.heap) == 0:  # O(1) проверка на пустоту
            raise IndexError("Peek from an empty heap.")  # O(1) возбуждение исключения
        return self.heap[0]  # O(1) возвращаем корень

    def build_heap(self, array):  # O(n) построение кучи из массива
        """Построение кучи из произвольного массива."""  # O(1)
        self.heap = array  # O(1) присваивание ссылки на массив (внимание: изменяет переданный список)
        for i in range(len(array) // 2 - 1, -1, -1):  # O(n) обход внутренних узлов
            self._sift_down(i)  # O(log n) для каждого узла, суммарно O(n)
            
    def get_heap(self):  # O(1) вернуть текущее внутреннее представление
        """Получить текущую кучу."""  # O(1)
        return self.heap  # O(1)
