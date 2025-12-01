"""
Модуль для вычисления префикс-функции строки.

Префикс-функция (π[i]): длина наибольшего собственного префикса строки S[0..i],
который является суффиксом подстроки S[0..i].

Временная сложность: O(n)
Пространственная сложность: O(n)
"""


def compute_prefix_function(pattern: str) -> list[int]:
    """
    Вычисляет префикс-функцию для строки.
    
    Алгоритм:
    - π[0] всегда 0 (пустой префикс не считается)
    - Для каждой позиции i используется ранее вычисленная информация
    - Если символы совпадают, увеличиваем длину совпадения
    - Если не совпадают, используем префиксные ссылки
    
    Args:
        pattern: входная строка
        
    Returns:
        Массив префикс-функции
        
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    n = len(pattern)
    pi = [0] * n
    
    # π[0] всегда равно 0
    for i in range(1, n):
        j = pi[i - 1]
        
        # Ищем наибольший префикс, который является суффиксом S[0..i]
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        
        if pattern[i] == pattern[j]:
            j += 1
        
        pi[i] = j
    
    return pi


def compute_prefix_function_verbose(pattern: str) -> tuple[list[int], list[str]]:
    """
    Вычисляет префикс-функцию с пошаговым объяснением.
    
    Returns:
        Кортеж (массив префикс-функции, список пошаговых описаний)
        
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    n = len(pattern)
    pi = [0] * n
    steps = []
    
    steps.append(f"Исходная строка: '{pattern}'")
    steps.append(f"π[0] = 0 (по определению)")
    
    for i in range(1, n):
        j = pi[i - 1]
        step_info = f"\nПозиция {i}: рассматриваем символ '{pattern[i]}'"
        
        while j > 0 and pattern[i] != pattern[j]:
            step_info += f"\n  '{pattern[i]}' != '{pattern[j]}' (j={j}), переходим к π[{j-1}]={pi[j-1]}"
            j = pi[j - 1]
        
        if pattern[i] == pattern[j]:
            step_info += f"\n  '{pattern[i]}' == '{pattern[j]}', увеличиваем j"
            j += 1
        
        pi[i] = j
        step_info += f"\n  π[{i}] = {j}"
        steps.append(step_info)
    
    steps.append(f"\nИтоговая функция: {pi}")
    return pi, steps


# Примеры использования
if __name__ == "__main__":
    test_strings = [
        "ABAB",
        "AAAA",
        "ABCDA",
        "AABAAAB",
        "ABCABDABC"
    ]
    
    for s in test_strings:
        pi = compute_prefix_function(s)
        print(f"Строка: {s:15} -> π = {pi}")
