# recursion.py

# Факториал числа n
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Временная сложность: O(n)
# Глубина рекурсии: n

# Число Фибоначчи
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

# Временная сложность: O(2^n)
# Глубина рекурсии: n

# Быстрое возведение в степень
def power(a, n):
    if n == 0:
        return 1
    elif n % 2 == 0:
        half = power(a, n // 2)
        return half * half
    else:
        half = power(a, (n - 1) // 2)
        return half * half * a

# Временная сложность: O(log n)
# Глубина рекурсии: O(log n)
