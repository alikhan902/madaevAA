# hash_table_open_addressing.py
# Хеш-таблица с открытой адресацией (linear/double hashing)

from typing import Any, Callable, Optional, List, Tuple  # O(1) импорт

_TOMBSTONE = object()  # O(1) создание sentinel объекта

class HashTableOpenAddressing:  # O(1) определение класса
    """
    Открытая адресация с поддержкой двух стратегий:
    - mode='linear' — линейное пробирование
    - mode='double' — двойное хеширование (double hashing)
    Реализация поддерживает динамическое увеличение при load_factor > max_load.
    Для удаления используется tombstone.
    Отслеживаем collisions (кол-во столкновений при вставке).
    
    Сложности:
      - average: O(1) при низком load factor
      - worst: O(n) при высокой загрузке или плохой хеш-функции
    """

    def __init__(self, capacity: int = 8, hash_func: Callable[[str], int] = None,  # O(capacity)
                 second_hash_func: Callable[[str], int] = None, mode: str = "linear"):  # O(1)
        self._capacity = max(8, capacity)  # O(1)
        self._keys: List[Optional[str]] = [None] * self._capacity  # O(capacity)
        self._vals: List[Any] = [None] * self._capacity  # O(capacity)
        self._size = 0  # O(1)
        self._hash = hash_func or (lambda s: sum(ord(c) for c in s))  # O(1)
        self._second_hash = second_hash_func or (lambda s: 1 + (sum(ord(c) for c in s) % (self._capacity - 1)))  # O(1)
        self._mode = mode  # O(1)
        self._collisions = 0  # O(1)
        self._max_load = 0.6  # O(1)

    def __len__(self):  # O(1)
        return self._size  # O(1)

    def load_factor(self) -> float:  # O(1)
        return self._size / self._capacity  # O(1)

    def _probe_sequence(self, key: str):  # O(capacity) в худшем
        """Генератор последовательности индексов зондирования
        Сложность: O(1) на одну итерацию, всего O(capacity)
        """
        h1 = self._hash(key) % self._capacity  # O(n) за хеш + O(1) модуль
        if self._mode == "linear":  # O(1)
            for i in range(self._capacity):  # O(capacity) цикл
                yield (h1 + i) % self._capacity  # O(1) на итерацию
        elif self._mode == "double":  # O(1)
            step = self._second_hash(key) % (self._capacity - 1)  # O(n) за хеш + O(1)
            if step == 0:  # O(1)
                step = 1  # O(1)
            idx = h1  # O(1)
            for i in range(self._capacity):  # O(capacity) цикл
                yield idx  # O(1)
                idx = (idx + step) % self._capacity  # O(1) на итерацию
        else:  # O(1)
            raise ValueError("Unknown probing mode")  # O(1)

    def put(self, key: str, value: Any) -> None:  # O(1+α) в среднем
        if self.load_factor() > self._max_load:  # O(1)
            self._resize(self._capacity * 2)  # O(n) редко

        first_tomb = None  # O(1)
        for idx in self._probe_sequence(key):  # O(capacity) в худшем
            k = self._keys[idx]  # O(1)
            if k is None:  # O(1)
                # empty slot
                if first_tomb is not None:  # O(1)
                    idx = first_tomb  # O(1)
                self._keys[idx] = key  # O(1)
                self._vals[idx] = value  # O(1)
                self._size += 1  # O(1)
                return  # O(1)
            if k is _TOMBSTONE:  # O(1)
                if first_tomb is None:  # O(1)
                    first_tomb = idx  # O(1)
                # continue probing, maybe key exists further
                continue  # O(1)
            if k == key:  # O(1)
                # replace value
                self._vals[idx] = value  # O(1)
                return  # O(1)
            # collision
            self._collisions += 1  # O(1)
        # table full (may happen if table contains only tombstones and used slots)
        # Попробуем увеличить таблицу и повторить вставку один раз.
        self._resize(self._capacity * 2)  # O(n)
        # После ресайза повторим вставку (должно завершиться успешно)
        self.put(key, value)  # O(1+α)
        return  # O(1)

    def get(self, key: str):  # O(1+α) в среднем
        for idx in self._probe_sequence(key):  # O(capacity) в худшем
            k = self._keys[idx]  # O(1)
            if k is None:  # O(1)
                break  # O(1)
            if k is _TOMBSTONE:  # O(1)
                continue  # O(1)
            if k == key:  # O(1)
                return self._vals[idx]  # O(1)
        raise KeyError(key)  # O(1)

    def delete(self, key: str):  # O(1+α) в среднем
        for idx in self._probe_sequence(key):  # O(capacity) в худшем
            k = self._keys[idx]  # O(1)
            if k is None:  # O(1)
                break  # O(1)
            if k is _TOMBSTONE:  # O(1)
                continue  # O(1)
            if k == key:  # O(1)
                self._keys[idx] = _TOMBSTONE  # O(1)
                self._vals[idx] = None  # O(1)
                self._size -= 1  # O(1)
                return  # O(1)
        raise KeyError(key)  # O(1)

    def contains(self, key: str) -> bool:  # O(1+α) в среднем
        try:  # O(1)
            self.get(key)  # O(1+α)
            return True  # O(1)
        except KeyError:  # O(1)
            return False  # O(1)

    def _resize(self, new_capacity: int):  # O(n) где n — число элементов
        old_items = [(k, v) for k, v in zip(self._keys, self._vals) if k is not None and k is not _TOMBSTONE]  # O(n)
        self._capacity = max(8, int(new_capacity))  # O(1)
        self._keys = [None] * self._capacity  # O(capacity)
        self._vals = [None] * self._capacity  # O(capacity)
        self._size = 0  # O(1)
        self._collisions = 0  # O(1)
        # update second_hash if it depended on capacity
        # keep same functions but ensure second_hash works: wrap to use mod (self._capacity - 1)
        for k, v in old_items:  # O(n) цикл
            self.put(k, v)  # O(1) в среднем на каждый элемент, итого O(n)

    def stats(self):  # O(capacity)
        """Возвращает статистику таблицы
        Сложность: O(capacity)
        """
        used = sum(1 for k in self._keys if k is not None and k is not _TOMBSTONE)  # O(capacity)
        tombs = sum(1 for k in self._keys if k is _TOMBSTONE)  # O(capacity)
        return {  # O(1)
            "size": self._size,  # O(1)
            "capacity": self._capacity,  # O(1)
            "load_factor": self.load_factor(),  # O(1)
            "collisions": self._collisions,  # O(1)
            "used_slots": used,  # O(1)
            "tombstones": tombs  # O(1)
        }

    def keys(self):  # O(n) где n — число элементов
        return [k for k in self._keys if k is not None and k is not _TOMBSTONE]  # O(n)
