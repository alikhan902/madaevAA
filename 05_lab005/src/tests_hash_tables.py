# tests_hash_tables.py
# Модульные тесты для хеш-таблиц

import unittest  # O(1) импорт
import random  # O(1) импорт
import string  # O(1) импорт

from hash_functions import simple_hash, poly_hash, djb2_hash  # O(1) импорт
from hash_table_chaining import HashTableChaining  # O(1) импорт
from hash_table_open_addressing import HashTableOpenAddressing  # O(1) импорт

def rand_str(n=8):  # O(n) где n — длина строки
    """Генерирует случайную строку длины n"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(n))  # O(n)

class TestHashTables(unittest.TestCase):  # O(1) определение класса
    def setUp(self):  # O(m*n) где m=200, n=6 (длина генерируемой строки)
        """Подготовка к тесту: создание 200 случайных ключей"""
        self.keys = [rand_str(6) for _ in range(200)]  # O(m*n)
        self.values = list(range(len(self.keys)))  # O(m)

    def test_chaining_basic(self):  # O(m*(1+α)) в среднем где m=200
        """Тест базовых операций для chaining"""
        ht = HashTableChaining(hash_func=poly_hash)  # O(capacity)
        for k, v in zip(self.keys, self.values):  # O(m) цикл
            ht.put(k, v)  # O(n) за хеш-функцию, O(1) за вставку, итого O(n)
        for k, v in zip(self.keys, self.values):  # O(m) цикл
            self.assertEqual(ht.get(k), v)  # O(n) за хеш + O(1+α) поиск
        # delete half
        for k in self.keys[:50]:  # O(50) цикл
            ht.delete(k)  # O(n) за хеш + O(1+α) удаление
            self.assertFalse(ht.contains(k))  # O(n) за хеш + O(1+α)
        self.assertTrue(len(ht) == 150)  # O(1)

    def test_open_linear_basic(self):  # O(m*(1+α)) в среднем
        """Тест базовых операций для open addressing linear"""
        ht = HashTableOpenAddressing(hash_func=djb2_hash, mode="linear")  # O(capacity)
        for k, v in zip(self.keys, self.values):  # O(m) цикл
            ht.put(k, v)  # O(1+α)
        for k, v in zip(self.keys, self.values):  # O(m) цикл
            self.assertEqual(ht.get(k), v)  # O(1+α)
        for k in self.keys[:50]:  # O(50) цикл
            ht.delete(k)  # O(1+α)
            self.assertFalse(ht.contains(k))  # O(1+α)

    def test_open_double_basic(self):  # O(m*(1+α)) в среднем
        """Тест базовых операций для open addressing double hashing"""
        ht = HashTableOpenAddressing(hash_func=poly_hash, second_hash_func=simple_hash, mode="double")  # O(capacity)
        for k, v in zip(self.keys, self.values):  # O(m) цикл
            ht.put(k, v)  # O(1+α)
        for k, v in zip(self.keys, self.values):  # O(m) цикл
            self.assertEqual(ht.get(k), v)  # O(1+α)

    def test_collision_behavior(self):  # O(collision_count)
        """Тест поведения при коллизиях"""
        # force collisions by using very small capacity and simple hash
        ht = HashTableChaining(capacity=4, hash_func=lambda s: sum(ord(c) for c in s))  # O(1)
        keys = ['aa', 'bb', 'cc', 'dd', 'ee']  # O(1)
        for i, k in enumerate(keys):  # O(5) цикл
            ht.put(k, i)  # O(1) за хеш + O(1) вставка
        stats = ht.stats()  # O(capacity)
        self.assertTrue(stats['collisions'] >= 1)  # O(1)

if __name__ == "__main__":  # O(1)
    unittest.main()  # O(test_count*(1+α))
