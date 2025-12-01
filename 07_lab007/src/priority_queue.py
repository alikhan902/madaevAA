# priority_queue.py
# Простая реализация приоритетной очереди поверх кучи (Min-Heap)

from heap import Heap  # O(1) импорт класса Heap


class PriorityQueue:
    def __init__(self):  # O(1) инициализация приоритетной очереди
        self.heap = Heap(is_min=True)  # O(1) Min-Heap для хранения (priority, item)

    def enqueue(self, item, priority):  # O(log n) добавление элемента в очередь
        """Добавление элемента в очередь с заданным приоритетом."""  # O(1)
        self.heap.insert((priority, item))  # O(log n) вставка в кучу по приоритету

    def dequeue(self):  # O(log n) извлечение элемента с наименьшим приоритетом
        """Удаление элемента с наименьшим приоритетом (корень кучи)."""  # O(1)
        if len(self.heap.get_heap()) == 0:  # O(1) проверка на пустоту
            raise IndexError("Dequeue from an empty queue.")  # O(1) возбуждение исключения
        return self.heap.extract()[1]  # O(log n) извлечение кортежа (priority, item) и возврат item
