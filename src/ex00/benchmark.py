#!/usr/bin/env python
import timeit

def get_gmail_with_loop(emails_list):
    """
    Функция, которая находит все Gmail адреса с помощью обычного цикла
    """
    result = []
    for email in emails_list:
        if email.endswith('@gmail.com'):
            result.append(email)
    return result

def get_gmail_with_comprehension(emails_list):
    """
    Функция, которая находит все Gmail адреса с помощью list comprehension
    """
    return [email for email in emails_list if email.endswith('@gmail.com')]

def measure_time(func, emails_list, number_of_runs):
    """
    Замеряет время выполения функции
    """
    return timeit.timeit(lambda: func(emails_list), number=number_of_runs)

if __name__ == '__main__':
    
    base_emails = [
        'john@gmail.com',
        'james@gmail.com',
        'alice@yahoo.com',
        'anna@live.com',
        'philipp@gmail.com'
    ]
    
    # Дублируем каждый элемент 5 раз
    emails = base_emails * 5
    
    # Количество запусков согласно заданию
    number_of_runs = 90_000_000

    # Замеряем время выполнения
    loop_time = measure_time(get_gmail_with_loop, emails, number_of_runs)
    comprehension_time = measure_time(get_gmail_with_comprehension, emails, number_of_runs)

    # Сравниваем и выводим результат
    if comprehension_time <= loop_time:
        print("it is better to use a list comprehension")
        # Выводим от меньшего к большему
        print(f"{comprehension_time} vs {loop_time}")
    else:
        print("it is better to use a loop")
        # Выводим от меньшего к большему
        print(f"{loop_time} vs {comprehension_time}")