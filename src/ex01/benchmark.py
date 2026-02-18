#!/usr/bin/env python
import timeit

def get_gmail_with_loop(emails):
    """
    Функция, которая находит все Gmail адреса с помощью обычного цикла
    """
    result = []
    for email in emails:
        if email.endswith('@gmail.com'):
            result.append(email)
    return result

def get_gmail_with_comprehension(emails):
    """
    Функция, которая находит все Gmail адреса с помощью list comprehension
    """
    return [email for email in emails if email.endswith('@gmail.com')]

def get_gmail_with_map(emails):
    """
    Функция которая находит все Gmail адреса с помощью map
    Возвращает email для gmail адресов и None для остальных
    """
    return list(map(lambda email: email if email.endswith('@gmail.com') else None, emails))

def measure_time(func, emails, number_of_runs):
    """
    Замеряет время выполения функции
    """
    return timeit.timeit(lambda: func(emails), number=number_of_runs)

if __name__ == '__main__':
    
    emails = [
        'john@gmail.com',
        'james@gmail.com',
        'alice@yahoo.com',
        'anna@live.com',
        'philipp@gmail.com'
    ] * 5
    
    # Замеряем время выполнения
    loop_time = measure_time(get_gmail_with_loop, emails, 100_000)
    comprehension_time = measure_time(get_gmail_with_comprehension, emails, 100_000)
    map_time = measure_time(get_gmail_with_map, emails, 100_000)

    # Собираем все времена в список для сортировки и сортируем от меньшего к большему
    times = [(loop_time, "loop"), (comprehension_time, "comprehension"), (map_time, "map")]
    times.sort()

    # Определяем самый быстрый метод
    if times[0][1] == "map":
        print("it is better to use a map")
    elif times[0][1] == "comprehension":
        print("it is better to use a list comprehension")
    else:
        print("it is better to use a loop")

    # Выводим все три времени в порядке возрастания
    print(f"{times[0][0]} vs {times[1][0]} vs {times[2][0]}")    

