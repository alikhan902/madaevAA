# recursion_tasks.py
import os

# Бинарный поиск
def binary_search(arr, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search(arr, target, low, mid - 1)
    else:
        return binary_search(arr, target, mid + 1, high)

# Рекурсивный обход файловой системы
def recursive_file_traversal(path):
    for root, dirs, files in os.walk(path):
        print(f"Каталог: {root}")
        for file in files:
            print(f"    Файл: {file}")
        for dir in dirs:
            recursive_file_traversal(os.path.join(root, dir))

# Ханойские башни
def hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f"Переместить диск 1 с {source} на {target}")
        return
    hanoi(n - 1, source, auxiliary, target)
    print(f"Переместить диск {n} с {source} на {target}")
    hanoi(n - 1, auxiliary, target, source)

if __name__ == "__main__":
    print("=== Бинарный поиск ===")
    arr = [1, 3, 5, 7, 9, 11]
    target = 7
    result = binary_search(arr, target, 0, len(arr) - 1)
    print(f"Ищем {target} в {arr} -> индекс: {result}")

    print("\n=== Рекурсивный обход файлов ===")
    recursive_file_traversal(".")  # текущая папка

    print("\n=== Ханойские башни ===")
    hanoi(3, "A", "C", "B")
