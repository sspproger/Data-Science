#!/usr/bin/env python
import timeit
import sys


def get_gmail_with_loop(emails):
    """Находит Gmail адреса с помощью цикла"""
    result = []
    for email in emails:
        if email.endswith('@gmail.com'):
            result.append(email)
    return result


def get_gmail_with_comprehension(emails):
    """Находит Gmail адреса с помощью list comprehension"""
    return [email for email in emails if email.endswith('@gmail.com')]


def get_gmail_with_map(emails):
    """Находит Gmail адреса с помощью map"""
    return list(map(lambda email: email if email.endswith('@gmail.com') else None, emails))


def get_gmail_with_filter(emails):
    """Находит Gmail адреса с помощью filter"""
    return list(filter(lambda email: email.endswith('@gmail.com'), emails))


def measure_time(func, emails, number_of_calls):
    """Замеряет время выполнения функции"""
    return timeit.timeit(lambda: func(emails), number=number_of_calls)


if __name__ == '__main__':
    # Проверяем количество аргументов
    if len(sys.argv) != 3:
        sys.exit(1)
    
    # Получаем аргументы
    function_name = sys.argv[1]
    number_of_calls = int(sys.argv[2])
    
    # Словарь доступных функций
    functions = {
        'loop': get_gmail_with_loop,
        'list_comprehension': get_gmail_with_comprehension,
        'map': get_gmail_with_map,
        'filter': get_gmail_with_filter
    }
    
    # Проверяем, что функция существует
    if function_name not in functions:
        sys.exit(1)
    
    # Тестовые данные
    emails = [
        'john@gmail.com',
        'james@gmail.com',
        'alice@yahoo.com',
        'anna@live.com',
        'philipp@gmail.com'
    ] * 5
    
    # Выполняем замер
    result_time = measure_time(functions[function_name], emails, number_of_calls)
    
    # Выводим результат
    print(result_time)