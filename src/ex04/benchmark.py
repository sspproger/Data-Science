#!/usr/bin/env python
import timeit
import random
from collections import Counter

def count_with_manual(numbers):
    """Считает, сколько раз каждое число от 0 до 100 встречается в списке numbers"""
    counts = {i:0 for i in range(101)}
    for num in numbers:
        counts[num] += 1
    return counts

def top_ten_manual(numbers):
    """Возвращает список из 10 кортежей самых часто встречающихся чисел из списка numbers"""
    counts = count_with_manual(numbers)
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return sorted_counts[:10]

def count_with_counter(numbers):
    counter = Counter(numbers)
    full_counts = {i: counter.get(i, 0) for i in range(101)}
    return full_counts

def top_ten_with_counter(numbers):
    counter = Counter(numbers)
    return counter.most_common(10)

if __name__ == '__main__':
    random_list = [random.randint(0, 100) for _ in range(1_000_000)]

    manual_count_time = timeit.timeit(lambda: count_with_manual(random_list), number=1)
    print(f"my function: {manual_count_time:.7f}")

    counter_count_time = timeit.timeit(lambda: count_with_counter(random_list), number=1)
    print(f"Counter: {counter_count_time:.7f}")

    manual_top_time = timeit.timeit(lambda: top_ten_manual(random_list), number=1)
    print(f"my top: {manual_top_time:.7f}")

    counter_top_time = timeit.timeit(lambda: top_ten_with_counter(random_list), number=1)
    print(f"Counter is top: {counter_top_time:.7f}")