#!/usr/bin/env python
import timeit
import sys
from functools import reduce

def sum_squares_loop(n):
    """Вычисляет сумму квадратов от 1 до n с помощью цикла"""
    total = 0
    for i in range(1, n + 1):
        total += i * i
    return total

def sum_squares_reduce(n):
    """Вычисляет сумму квадратов от 1 до n с помощью reduce"""
    return reduce(lambda acc, x: acc + x * x, range(1, n + 1), 0)

if __name__ == '__main__':
    # Проверяем количество аргументов
    if len(sys.argv) != 4:
        sys.exit(1)
    
    # Получаем аргументы командной строки
    function_name = sys.argv[1]
    number_of_calls = int(sys.argv[2])
    n = int(sys.argv[3])
    
    # Выбираем нужную функцию
    if function_name == 'loop':
        func = sum_squares_loop
    elif function_name == 'reduce':
        func = sum_squares_reduce
    else:
        sys.exit(1)
    
    # Замеряем время выполнения
    result_time = timeit.timeit(lambda: func(n), number=number_of_calls)
    
    # Выводим результат
    print(result_time)