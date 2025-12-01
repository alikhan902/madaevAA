# test_heap.py
# Набор юнит-тестов для кучи, heapsort и приоритетной очереди

import unittest  # O(1) импорт модуля unittest
from heap import Heap  # O(1) импорт класса Heap
from priority_queue import PriorityQueue  # O(1) импорт PriorityQueue
from heapsort import heapsort  # O(1) импорт функции heapsort


class TestHeap(unittest.TestCase):

    def test_insert_and_extract_min(self):  # O(1) тестовая функция
        min_heap = Heap(is_min=True)  # O(1) создание Min-Heap
        min_heap.insert(10)  # O(log n) вставка
        min_heap.insert(5)  # O(log n) вставка
        min_heap.insert(3)  # O(log n) вставка

        self.assertEqual(min_heap.extract(), 3)  # O(log n) извлечение — ожидаем 3
        self.assertEqual(min_heap.extract(), 5)  # O(log n) извлечение — ожидаем 5
        self.assertEqual(min_heap.extract(), 10)  # O(log n) извлечение — ожидаем 10

    def test_insert_and_extract_max(self):  # O(1)
        max_heap = Heap(is_min=False)  # O(1) создание Max-Heap
        max_heap.insert(10)  # O(log n)
        max_heap.insert(5)  # O(log n)
        max_heap.insert(3)  # O(log n)

        self.assertEqual(max_heap.extract(), 10)  # O(log n) извлечение — ожидаем 10
        self.assertEqual(max_heap.extract(), 5)  # O(log n) извлечение — ожидаем 5
        self.assertEqual(max_heap.extract(), 3)  # O(log n) извлечение — ожидаем 3

    def test_build_heap(self):  # O(1)
        min_heap = Heap(is_min=True)  # O(1)
        min_heap.build_heap([10, 5, 3, 7, 1, 8])  # O(n) построение кучи
        self.assertEqual(min_heap.extract(), 1)  # O(log n) извлечение — ожидаем 1
        self.assertEqual(min_heap.extract(), 3)  # O(log n) извлечение — ожидаем 3

    def test_peek(self):  # O(1)
        min_heap = Heap(is_min=True)  # O(1)
        min_heap.insert(10)  # O(log n)
        min_heap.insert(5)  # O(log n)
        min_heap.insert(3)  # O(log n)
        self.assertEqual(min_heap.peek(), 3)  # O(1) просмотр — ожидаем 3

    def test_empty_extract(self):  # O(1)
        min_heap = Heap(is_min=True)  # O(1)
        with self.assertRaises(IndexError):  # O(1)
            min_heap.extract()  # O(1) / O(log n) — извлечение из пустой кучи вызывает ошибку

    def test_empty_peek(self):  # O(1)
        min_heap = Heap(is_min=True)  # O(1)
        with self.assertRaises(IndexError):  # O(1)
            min_heap.peek()  # O(1) просмотр пустой кучи вызывает ошибку


class TestHeapsort(unittest.TestCase):

    def test_heapsort(self):  # O(1)
        array = [3, 1, 5, 7, 2, 4, 6]  # O(1) создание тестового массива
        sorted_array = heapsort(array)  # O(n log n) сортировка
        self.assertEqual(sorted_array, [1, 2, 3, 4, 5, 6, 7])  # O(1) проверка результата

    def test_empty_array(self):  # O(1)
        array = []  # O(1)
        sorted_array = heapsort(array)  # O(1) при пустом массиве
        self.assertEqual(sorted_array, [])  # O(1)

    def test_single_element(self):  # O(1)
        array = [5]  # O(1)
        sorted_array = heapsort(array)  # O(1)
        self.assertEqual(sorted_array, [5])  # O(1)


class TestPriorityQueue(unittest.TestCase):

    def test_enqueue_and_dequeue(self):  # O(1)
        pq = PriorityQueue()  # O(1)
        pq.enqueue("task1", 2)  # O(log n)
        pq.enqueue("task2", 1)  # O(log n)
        pq.enqueue("task3", 3)  # O(log n)

        self.assertEqual(pq.dequeue(), "task2")  # O(log n) dequeue — приоритет 1
        self.assertEqual(pq.dequeue(), "task1")  # O(log n) dequeue — приоритет 2
        self.assertEqual(pq.dequeue(), "task3")  # O(log n) dequeue — приоритет 3

    def test_empty_dequeue(self):  # O(1)
        pq = PriorityQueue()  # O(1)
        with self.assertRaises(IndexError):  # O(1)
            pq.dequeue()  # O(1) / O(log n) — извлечение из пустой очереди вызывает ошибку


if __name__ == '__main__':
    unittest.main()  # запуск тестов — строка вывода, сложность не проставлена
