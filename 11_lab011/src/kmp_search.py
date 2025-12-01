"""
Алгоритм Кнута-Морриса-Пратта (KMP) для поиска подстроки.

Использует префикс-функцию для пропуска повторных сравнений.
В отличие от наивного алгоритма, не "откатывается" в тексте.

Временная сложность: O(n + m), где n - длина текста, m - длина паттерна
Пространственная сложность: O(m)

Лучше всего работает при частых повторениях в паттерне.
"""

from prefix_function import compute_prefix_function


def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Поиск всех вхождений паттерна в тексте с использованием KMP.
    
    Алгоритм:
    1. Вычисляем префикс-функцию для паттерна
    2. Проходим по тексту, сравнивая символы с паттерном
    3. При несовпадении используем префикс-функцию для пропуска
    4. При совпадении всего паттерна добавляем позицию в результаты
    
    Args:
        text: текст для поиска
        pattern: паттерн для поиска
        
    Returns:
        Список индексов начальных позиций найденных вхождений
        
    Time Complexity: O(n + m)
    Space Complexity: O(m)
    """
    if not pattern or not text:
        return []
    
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    # Вычисляем префикс-функцию для паттерна
    pi = compute_prefix_function(pattern)
    results = []
    j = 0  # индекс для паттерна
    
    # Проходим по тексту
    for i in range(n):
        # При несовпадении используем префикс-функцию
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        
        # Если символы совпадают
        if text[i] == pattern[j]:
            j += 1
        
        # Если весь паттерн найден
        if j == m:
            results.append(i - m + 1)
            j = pi[m - 1]  # Продолжаем поиск дальше
    
    return results


def kmp_search_first(text: str, pattern: str) -> int:
    """
    Поиск первого вхождения паттерна в тексте.
    
    Args:
        text: текст для поиска
        pattern: паттерн для поиска
        
    Returns:
        Индекс первого вхождения или -1, если не найдено
        
    Time Complexity: O(n + m)
    Space Complexity: O(m)
    """
    if not pattern or not text:
        return -1
    
    n, m = len(text), len(pattern)
    if m > n:
        return -1
    
    pi = compute_prefix_function(pattern)
    j = 0
    
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        
        if text[i] == pattern[j]:
            j += 1
        
        if j == m:
            return i - m + 1
    
    return -1


def kmp_search_with_steps(text: str, pattern: str) -> tuple[list[int], list[str]]:
    """
    Поиск с пошаговым объяснением процесса.
    
    Returns:
        Кортеж (результаты, шаги выполнения)
        
    Time Complexity: O(n + m)
    Space Complexity: O(n + m)
    """
    if not pattern or not text:
        return [], []
    
    n, m = len(text), len(pattern)
    if m > n:
        return [], ["Паттерн длиннее текста"]
    
    pi = compute_prefix_function(pattern)
    results = []
    steps = []
    j = 0
    
    steps.append(f"Текст:     {text}")
    steps.append(f"Паттерн:   {pattern}")
    steps.append(f"π-функция: {pi}")
    steps.append("")
    
    for i in range(n):
        step = f"i={i}: '{text[i]}' (в паттерне j={j})"
        
        while j > 0 and text[i] != pattern[j]:
            step += f"\n  Несовпадение: '{text[i]}' != '{pattern[j]}'"
            j = pi[j - 1]
            step += f" -> j = π[{j}] = {j}"
        
        if text[i] == pattern[j]:
            step += f"\n  Совпадение: '{text[i]}' == '{pattern[j]}' -> j = {j + 1}"
            j += 1
        
        if j == m:
            step += f"\n  !!! НАЙДЕНО вхождение в позиции {i - m + 1}"
            results.append(i - m + 1)
            j = pi[m - 1]
        
        steps.append(step)
    
    steps.append(f"\nИтого найдено вхождений: {len(results)}")
    if results:
        steps.append(f"Позиции: {results}")
    
    return results, steps


# Примеры использования
if __name__ == "__main__":
    test_cases = [
        ("ABABDABACDABABCABAB", "ABABCABAB"),
        ("AABAACAADAABAABA", "AABA"),
        ("abcabcabcabc", "bcab"),
        ("mississippi", "issi"),
    ]
    
    for text, pattern in test_cases:
        results = kmp_search(text, pattern)
        print(f"Текст: '{text}'")
        print(f"Паттерн: '{pattern}'")
        print(f"Найдено в позициях: {results}\n")
