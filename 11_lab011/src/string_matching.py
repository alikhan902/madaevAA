"""
Дополнительные алгоритмы поиска подстроки:
1. Алгоритм Бойера-Мура (Boyer-Moore)
2. Алгоритм Рабина-Карпа (Rabin-Karp)

Бойера-Мура:
- Лучше всего работает с большими алфавитами и длинными паттернами
- Идет по тексту справа налево в паттерне
- Использует два правила сдвига: "плохой символ" и "хороший суффикс"
- Временная сложность: O(n/m) в среднем, O(nm) в худшем
- Пространственная сложность: O(|Σ|), где Σ - размер алфавита

Рабина-Карпа:
- Использует хеширование для быстрого сравнения
- Хорош для поиска множественных паттернов одновременно
- Временная сложность: O(n + m) в среднем, O(nm) в худшем
- Пространственная сложность: O(1)
"""


def boyer_moore_search(text: str, pattern: str) -> list[int]:
    """
    Алгоритм Бойера-Мура для поиска подстроки.
    
    Основные идеи:
    1. Сравниваем паттерн справа налево (в обратном порядке)
    2. При несовпадении используем правило "плохого символа"
    3. Паттерн сдвигается на несколько позиций сразу
    
    Правило "плохого символа":
    Если символ не входит в паттерн, сдвигаем на всю длину паттерна.
    Если входит, сдвигаем на расстояние до его последнего вхождения.
    
    Args:
        text: текст для поиска
        pattern: паттерн для поиска
        
    Returns:
        Список индексов начальных позиций найденных вхождений
        
    Time Complexity: O(n/m) в среднем, O(nm) в худшем
    Space Complexity: O(|Σ|)
    """
    if not pattern or not text:
        return []
    
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    # Таблица "плохого символа"
    # Для каждого символа храним расстояние до его последнего вхождения в паттерн
    bad_char_table = {}
    for i in range(m - 1):
        bad_char_table[pattern[i]] = m - 1 - i
    
    # Символ, не входящий в паттерн, имеет значение m
    default_shift = m
    
    results = []
    i = 0  # Позиция в тексте
    
    while i <= n - m:
        # Сравниваем паттерн справа налево
        j = m - 1  # Позиция в паттерне (с конца)
        
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        
        if j < 0:
            # Найдено совпадение
            results.append(i)
            # Используем правило "плохого символа" для продолжения поиска
            i += default_shift if i + m >= n else bad_char_table.get(text[i + m], default_shift)
        else:
            # Несовпадение на позиции j
            bad_char = text[i + j]
            shift = bad_char_table.get(bad_char, default_shift)
            # Сдвигаем так, чтобы этот символ выровнялся с его последним вхождением в паттерн
            shift = max(1, shift - (m - 1 - j))
            i += shift
    
    return results


def boyer_moore_search_optimized(text: str, pattern: str) -> list[int]:
    """
    Оптимизированная версия Бойера-Мура с обоими правилами сдвига.
    
    Args:
        text: текст для поиска
        pattern: паттерн для поиска
        
    Returns:
        Список индексов начальных позиций найденных вхождений
        
    Time Complexity: O(n/m) в среднем, O(nm) в худшем
    Space Complexity: O(m + |Σ|)
    """
    if not pattern or not text:
        return []
    
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    # Таблица "плохого символа"
    bad_char = [-1] * 256  # Для ASCII
    for i in range(m):
        bad_char[ord(pattern[i])] = i
    
    results = []
    s = 0  # Сдвиг
    
    while s <= n - m:
        j = m - 1
        
        # Сравниваем паттерн справа налево
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        
        if j < 0:
            # Найдено совпадение
            results.append(s)
            s += 1 if s + m >= n else m - bad_char[ord(text[s + m])]
        else:
            # Сдвигаем согласно правилу "плохого символа"
            s += max(1, j - bad_char[ord(text[s + j])])
    
    return results


def rabin_karp_search(text: str, pattern: str, prime: int = 101) -> list[int]:
    """
    Алгоритм Рабина-Карпа для поиска подстроки.
    
    Основная идея:
    1. Вычисляем хеш паттерна
    2. Вычисляем хеши всех подстрок текста длины m
    3. Сравниваем хеши и проверяем символы при совпадении
    
    Args:
        text: текст для поиска
        pattern: паттерн для поиска
        prime: простое число для хеширования (для модуля)
        
    Returns:
        Список индексов начальных позиций найденных вхождений
        
    Time Complexity: O(n + m) в среднем, O(nm) в худшем (при коллизиях)
    Space Complexity: O(1)
    """
    if not pattern or not text:
        return []
    
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    BASE = 256  # Размер алфавита
    MOD = 101 * 10**9 + 7  # Большое простое число для модуля
    
    pattern_hash = 0
    text_hash = 0
    pow_base = 1  # BASE^(m-1) % MOD
    
    # Предварительное вычисление BASE^(m-1) % MOD
    for i in range(m - 1):
        pow_base = (pow_base * BASE) % MOD
    
    # Вычисляем хеш паттерна и первого окна текста
    for i in range(m):
        pattern_hash = (BASE * pattern_hash + ord(pattern[i])) % MOD
        text_hash = (BASE * text_hash + ord(text[i])) % MOD
    
    results = []
    
    # Скользящее окно по тексту
    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            # Если хеши совпадают, проверяем строки символ за символом
            if text[i:i + m] == pattern:
                results.append(i)
        
        # Вычисляем хеш для следующего окна
        if i < n - m:
            text_hash = (BASE * (text_hash - ord(text[i]) * pow_base) + ord(text[i + m])) % MOD
            if text_hash < 0:
                text_hash += MOD
    
    return results


def rabin_karp_multiple_search(text: str, patterns: list[str]) -> dict[str, list[int]]:
    """
    Поиск нескольких паттернов одновременно с помощью Рабина-Карпа.
    
    Это одно из основных преимуществ алгоритма - можно искать
    множество паттернов за один проход по тексту.
    
    Args:
        text: текст для поиска
        patterns: список паттернов для поиска
        
    Returns:
        Словарь {паттерн: список позиций}
        
    Time Complexity: O(n*k + m) где k - количество паттернов
    Space Complexity: O(k)
    """
    if not patterns or not text:
        return {}
    
    n = len(text)
    results = {pattern: [] for pattern in patterns}
    
    BASE = 256
    MOD = 101 * 10**9 + 7
    
    # Вычисляем хеши для всех паттернов
    pattern_hashes = {}
    for pattern in patterns:
        h = 0
        for char in pattern:
            h = (BASE * h + ord(char)) % MOD
        pattern_hashes[pattern] = h
    
    # Обрабатываем каждый паттерн отдельно
    for pattern in patterns:
        m = len(pattern)
        if m > n:
            continue
        
        pattern_hash = pattern_hashes[pattern]
        pow_base = 1
        
        for i in range(m - 1):
            pow_base = (pow_base * BASE) % MOD
        
        text_hash = 0
        for i in range(m):
            text_hash = (BASE * text_hash + ord(text[i])) % MOD
        
        for i in range(n - m + 1):
            if pattern_hash == text_hash:
                if text[i:i + m] == pattern:
                    results[pattern].append(i)
            
            if i < n - m:
                text_hash = (BASE * (text_hash - ord(text[i]) * pow_base) + ord(text[i + m])) % MOD
                if text_hash < 0:
                    text_hash += MOD
    
    return results


# Примеры использования
if __name__ == "__main__":
    test_cases = [
        ("ABABDABACDABABCABAB", "ABABCABAB"),
        ("AABAACAADAABAABA", "AABA"),
        ("abcabcabcabc", "bcab"),
        ("mississippi", "issi"),
    ]
    
    print("=" * 60)
    print("АЛГОРИТМ БОЙЕРА-МУРА:")
    print("=" * 60)
    
    for text, pattern in test_cases:
        results = boyer_moore_search(text, pattern)
        print(f"Текст: '{text}'")
        print(f"Паттерн: '{pattern}'")
        print(f"Найдено в позициях: {results}\n")
    
    print("\n" + "=" * 60)
    print("АЛГОРИТМ РАБИНА-КАРПА:")
    print("=" * 60)
    
    for text, pattern in test_cases:
        results = rabin_karp_search(text, pattern)
        print(f"Текст: '{text}'")
        print(f"Паттерн: '{pattern}'")
        print(f"Найдено в позициях: {results}\n")
    
    print("\n" + "=" * 60)
    print("ПОИСК МНОЖЕСТВЕННЫХ ПАТТЕРНОВ (РАБИНА-КАРПА):")
    print("=" * 60)
    
    text = "AABAACAADAABAABA"
    patterns = ["AABA", "AAB", "ABA"]
    results = rabin_karp_multiple_search(text, patterns)
    
    print(f"Текст: '{text}'")
    for pattern, positions in results.items():
        print(f"  Паттерн '{pattern}': {positions}")
