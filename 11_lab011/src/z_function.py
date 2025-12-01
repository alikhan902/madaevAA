"""
Z-функция (Z-array) для строки.

Z[i] - длина наибольшего общего префикса строки S и суффикса S[i..n-1].
Иными словами, Z[i] показывает, насколько длинный префикс совпадает с подстрокой, начинающейся с позиции i.

Временная сложность: O(n)
Пространственная сложность: O(n)

Применение:
- Поиск подстроки
- Поиск периода строки
- Проверка циклического сдвига
"""


def compute_z_function(s: str) -> list[int]:
    """
    Вычисляет Z-функцию для строки.
    
    Алгоритм использует "окно совпадения" [l, r]:
    - Поддерживаем отрезок с наибольшим r, где s[l:r+1] = s[0:r-l+1]
    - Для каждой позиции i используем ранее вычисленную информацию
    
    Args:
        s: входная строка
        
    Returns:
        Массив Z-функции
        
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    n = len(s)
    z = [0] * n
    z[0] = n  # Z[0] по определению равен длине строки
    
    l, r = 0, 0  # Границы "окна совпадения"
    
    for i in range(1, n):
        # Если i выходит за правую границу окна, начинаем заново
        if i > r:
            l, r = i, i
            # Расширяем окно вправо пока совпадают символы
            while r < n and s[r - l] == s[r]:
                r += 1
            z[i] = r - l
            r -= 1
        else:
            # i находится внутри окна [l, r]
            k = i - l  # Позиция относительно l
            
            if z[k] < r - i + 1:
                # z[k] не доходит до конца окна
                z[i] = z[k]
            else:
                # Нужно проверить символы дальше r
                l = i
                while r < n and s[r - l] == s[r]:
                    r += 1
                z[i] = r - l
                r -= 1
    
    return z


def compute_z_function_verbose(s: str) -> tuple[list[int], list[str]]:
    """
    Вычисляет Z-функцию с пошаговым объяснением.
    
    Returns:
        Кортеж (массив Z-функции, список пошаговых описаний)
        
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    n = len(s)
    z = [0] * n
    z[0] = n
    steps = []
    
    steps.append(f"Исходная строка: '{s}'")
    steps.append(f"z[0] = {n} (по определению)")
    
    l, r = 0, 0
    
    for i in range(1, n):
        step = f"\nПозиция {i}: рассматриваем символ '{s[i]}'"
        
        if i > r:
            step += f"\n  i > r ({i} > {r}), начинаем новое окно"
            l, r = i, i
            
            while r < n and s[r - l] == s[r]:
                step += f"\n    s[{r - l}]='{s[r - l]}' == s[{r}]='{s[r]}'"
                r += 1
            
            z[i] = r - l
            r -= 1
            step += f"\n  Окно [{l}, {r}], z[{i}] = {z[i]}"
        else:
            k = i - l
            step += f"\n  i внутри окна [{l}, {r}]"
            step += f"\n  k = {i} - {l} = {k}"
            
            if z[k] < r - i + 1:
                z[i] = z[k]
                step += f"\n  z[{k}]={z[k]} < {r - i + 1}, значит z[{i}] = {z[k]}"
            else:
                step += f"\n  z[{k}]={z[k]} >= {r - i + 1}, проверяем дальше"
                l = i
                while r < n and s[r - l] == s[r]:
                    r += 1
                z[i] = r - l
                r -= 1
                step += f"\n  Окно [{l}, {r}], z[{i}] = {z[i]}"
        
        steps.append(step)
    
    steps.append(f"\nИтоговая Z-функция: {z}")
    return z, steps


def z_search(text: str, pattern: str) -> list[int]:
    """
    Поиск всех вхождений паттерна в тексте с помощью Z-функции.
    
    Метод:
    1. Объединяем паттерн и текст: "pattern#text"
    2. Вычисляем Z-функцию для объединённой строки
    3. Индексы i с z[i] = len(pattern) указывают на начало вхождений в тексте
    
    Args:
        text: текст для поиска
        pattern: паттерн для поиска
        
    Returns:
        Список индексов начальных позиций найденных вхождений
        
    Time Complexity: O(n + m)
    Space Complexity: O(n + m)
    """
    if not pattern or not text:
        return []
    
    m = len(pattern)
    n = len(text)
    
    if m > n:
        return []
    
    # Объединяем паттерн и текст с разделителем
    combined = pattern + "#" + text
    z = compute_z_function(combined)
    
    results = []
    # Ищем позиции, где z[i] = len(pattern)
    for i in range(m + 1, len(combined)):
        if z[i] == m:
            results.append(i - m - 1)
    
    return results


def find_period(s: str) -> int:
    """
    Находит наименьший период строки с помощью Z-функции.
    
    Строка имеет период p, если s[i] = s[i + p] для всех допустимых i.
    
    Args:
        s: входная строка
        
    Returns:
        Длина наименьшего периода или len(s), если периода нет
        
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    n = len(s)
    z = compute_z_function(s)
    
    # Проверяем периоды от 1 до n//2
    for period in range(1, n // 2 + 1):
        # Если период существует, то z[period] + period должно быть >= n
        if z[period] + period == n:
            # Дополнительная проверка
            if all(z[i] + i >= n or z[i] == 0 for i in range(1, period)):
                return period
    
    return n


def is_cyclic_shift(s1: str, s2: str) -> bool:
    """
    Проверяет, является ли s2 циклическим сдвигом s1.
    
    Использует Z-функцию: если s2 - циклический сдвиг s1,
    то s2 входит в s1 + s1.
    
    Args:
        s1: первая строка
        s2: вторая строка
        
    Returns:
        True, если s2 - циклический сдвиг s1
        
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if len(s1) != len(s2):
        return False
    
    if not s1:
        return True
    
    # Проверяем, входит ли s2 в s1 + s1
    combined = s2 + "#" + s1 + s1
    z = compute_z_function(combined)
    
    m = len(s2)
    for i in range(m + 1, len(combined)):
        if z[i] == m:
            return True
    
    return False


# Примеры использования
if __name__ == "__main__":
    # Тестирование Z-функции
    test_strings = [
        "ABAB",
        "AAAA",
        "ABCDA",
        "AABAAAB",
    ]
    
    print("=" * 50)
    print("Z-функция:")
    print("=" * 50)
    for s in test_strings:
        z = compute_z_function(s)
        print(f"Строка: {s:15} -> z = {z}")
    
    print("\n" + "=" * 50)
    print("Поиск подстроки с Z-функцией:")
    print("=" * 50)
    test_cases = [
        ("ABABDABACDABABCABAB", "ABABCABAB"),
        ("AABAACAADAABAABA", "AABA"),
    ]
    
    for text, pattern in test_cases:
        results = z_search(text, pattern)
        print(f"Текст: '{text}'")
        print(f"Паттерн: '{pattern}'")
        print(f"Найдено в позициях: {results}\n")
    
    print("=" * 50)
    print("Поиск периода:")
    print("=" * 50)
    periods = ["ABCABCABC", "AAAA", "ABCDEF", "XYXYXY"]
    for s in periods:
        p = find_period(s)
        print(f"Строка: {s:15} -> период = {p}")
    
    print("\n" + "=" * 50)
    print("Проверка циклического сдвига:")
    print("=" * 50)
    cyclic_tests = [
        ("ABCD", "CDAB"),
        ("ABCD", "DABC"),
        ("ABCD", "ABDC"),
        ("abcabc", "bcabca"),
    ]
    
    for s1, s2 in cyclic_tests:
        result = is_cyclic_shift(s1, s2)
        print(f"'{s1}' и '{s2}': {result}")
