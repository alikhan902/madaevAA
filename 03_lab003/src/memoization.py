# memoization.py
import time
import matplotlib.pyplot as plt
from recursion import fibonacci as fibonacci_naive

# Мемоизированная версия числа Фибоначчи
memo = {}

def fibonacci_memo(n):
    if n in memo:
        return memo[n]
    if n == 0:
        memo[n] = 0
    elif n == 1:
        memo[n] = 1
    else:
        memo[n] = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    return memo[n]

print("Сравнение наивной и мемоизированной версий для n = 35")

start = time.time()
fibonacci_naive(35)
end = time.time()
naive_time = end - start

start = time.time()
fibonacci_memo(35)
end = time.time()
memoized_time = end - start

print(f"Наивная версия: {naive_time:.5f} секунд")
print(f"С мемоизацией: {memoized_time:.5f} секунд")

n_values = [10, 20, 30, 35]
naive_times = []
memoized_times = []

for n in n_values:
    # Время наивной версии
    start = time.time()
    fibonacci_naive(n)
    end = time.time()
    naive_times.append(end - start)

    # Время мемоизированной версии
    start = time.time()
    fibonacci_memo(n)
    end = time.time()
    memoized_times.append(end - start)

# Построение графика
plt.plot(n_values, naive_times, label='Наивная рекурсия')
plt.plot(n_values, memoized_times, label='Мемоизация')
plt.xlabel('n')
plt.ylabel('Время (секунды)')
plt.title('Сравнение времени вычисления Фибоначчи')
plt.legend()
plt.grid(True)
plt.show()
