# hash_table_chaining.py
# Хеш-таблица со методом цепочек (separate chaining)

from typing import Any, Callable, List, Tuple  # O(1) импорт
import math  # O(1) импорт

class HashTableChaining:  # O(1) определение класса
    """
    Хеш-таблица с методом цепочек (separate chaining).
    Динамическое масштабирование: увеличиваем при load_factor > max_load (0.75),
    уменьшаем при load_factor < min_load (0.2).
    Отслеживаем collisions (количество вставок, когда bucket уже не пуст).
    
    Сложность операций:
    put: O(1+α) в среднем, O(n) в худшем (все в одной цепочке)
    get: O(1+α) в среднем, O(n) в худшем
    delete: O(1+α) в среднем, O(n) в худшем
    Память: O(n + capacity)
    """

    def __init__(self, capacity: int = 8, hash_func: Callable[[str], int] = None):  # O(capacity)
        self._capacity = max(8, capacity)  # O(1)
        self._buckets: List[List[Tuple[str, Any]]] = [[] for _ in range(self._capacity)]  # O(capacity)
        self._size = 0  # O(1)
        self._hash = hash_func or (lambda s: sum(ord(c) for c in s))  # O(1)
        self._collisions = 0  # O(1)
        self._max_load = 0.75  # O(1)
        self._min_load = 0.2  # O(1)

    def __len__(self):  # O(1)
        return self._size  # O(1)

    def _bucket_index(self, key: str) -> int:  # O(n) где n — длина key
        return self._hash(key) % self._capacity  # O(n) за хеш-функцию + O(1) за модуль

    def put(self, key: str, value: Any) -> None:  # O(1+α) в среднем
        idx = self._bucket_index(key)  # O(n)
        bucket = self._buckets[idx]  # O(1)
        if bucket:  # O(1)
            # если ключ уже есть — заменим, не считаем коллизией
            for i, (k, _) in enumerate(bucket):  # O(len(bucket)) в среднем O(1+α)
                if k == key:  # O(1)
                    bucket[i] = (key, value)  # O(1)
                    return  # O(1)
            # новая запись в непустой бакете => коллизия
            self._collisions += 1  # O(1)
        bucket.append((key, value))  # O(1) для append
        self._size += 1  # O(1)
        if self.load_factor() > self._max_load:  # O(1)
            self._resize(self._capacity * 2)  # O(n) редко

    def get(self, key: str):  # O(1+α) в среднем
        idx = self._bucket_index(key)  # O(n)
        for k, v in self._buckets[idx]:  # O(len(bucket)) в среднем O(1+α)
            if k == key:  # O(1)
                return v  # O(1)
        raise KeyError(key)  # O(1)

    def delete(self, key: str):  # O(1+α) в среднем
        idx = self._bucket_index(key)  # O(n)
        bucket = self._buckets[idx]  # O(1)
        for i, (k, v) in enumerate(bucket):  # O(len(bucket)) в среднем O(1+α)
            if k == key:  # O(1)
                del bucket[i]  # O(len(bucket)) для удаления из списка
                self._size -= 1  # O(1)
                if 0 < self._capacity // 2 and self.load_factor() < self._min_load:  # O(1)
                    new_cap = max(8, self._capacity // 2)  # O(1)
                    self._resize(new_cap)  # O(n) редко
                return  # O(1)
        raise KeyError(key)  # O(1)

    def contains(self, key: str) -> bool:  # O(1+α) в среднем
        idx = self._bucket_index(key)  # O(n)
        return any(k == key for k, _ in self._buckets[idx])  # O(len(bucket)) в среднем O(1+α)

    def load_factor(self) -> float:  # O(1)
        return self._size / self._capacity  # O(1)

    def _resize(self, new_capacity: int):  # O(n) где n — текущее число элементов
        old_items = [(k, v) for bucket in self._buckets for (k, v) in bucket]  # O(n)
        self._capacity = int(new_capacity)  # O(1)
        self._buckets = [[] for _ in range(self._capacity)]  # O(new_capacity)
        self._size = 0  # O(1)
        self._collisions = 0  # O(1)
        for k, v in old_items:  # O(n) цикл
            self.put(k, v)  # O(1+α) на каждую вставку, итого O(n)

    def stats(self):  # O(n) где n — capacity
        """Возвращает словарь статистик: size, capacity, load_factor, collisions, bucket_lengths
        Сложность: O(n) где n — capacity
        """
        lens = [len(b) for b in self._buckets]  # O(capacity)
        return {  # O(1) на создание словаря
            "size": self._size,  # O(1)
            "capacity": self._capacity,  # O(1)
            "load_factor": self.load_factor(),  # O(1)
            "collisions": self._collisions,  # O(1)
            "max_bucket": max(lens) if lens else 0,  # O(capacity)
            "avg_bucket": sum(lens)/len(lens) if lens else 0,  # O(capacity)
            "bucket_lengths": lens  # O(capacity)
        }

    def keys(self):  # O(n) где n — число элементов
        return [k for bucket in self._buckets for (k, _) in bucket]  # O(n)
