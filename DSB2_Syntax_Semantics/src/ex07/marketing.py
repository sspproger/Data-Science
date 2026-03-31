import sys

def convert_to_sets(clients, participants, recipients):
    """
    Преобразуем списки в множества для работы с операциями над множествами
    Множества автоматически удаляют дубликаты
    """
    clients_set = set(clients)
    participants_set = set(participants)
    recipients_set = set(recipients)
    return clients_set, participants_set, recipients_set

def call_center_task(clients_set, recipients_set):
    """Клиенты, которые не видели промо-письмо (для call-центра)"""
    # Разность множеств: те, кто в clients, но не в recipients
    return list(clients_set - recipients_set)

def potential_clients_task(participants_set, clients_set):
    """Участники, которые не являются клиентами (потенциальные клиенты)"""
    # Разность множеств: те, кто в participants, но не в clients
    return list(participants_set - clients_set)

def loyalty_program_task(clients_set, participants_set):
    """Клиенты, которые не участвовали в мероприятии (программа лояльности)"""
    # Разность множеств: те, кто в clients, но не в participants
    return list(clients_set - participants_set)

def main():
    """
    Основная функция, которая обрабатывает аргументы командной строки
    и выполняет нужную задачу
    """
    # Проверяем количество аргументов
    if len(sys.argv) != 2:
        print("Ошибка: требуется один аргумент")
        print("Использование: python3 marketing.py <задача>")
        print("Доступные задачи: call_center, potential_clients, loyalty_program")
        return
    
    # Получаем название задачи из аргументов
    task_name = sys.argv[1]
    
    # Исходные данные (как в задании)
    clients = [
        'andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
        'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
        'elon@paypal.com', 'jessica@gmail.com'
    ]
    
    participants = [
        'walter@heisenberg.com', 'vasily@mail.ru',
        'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
        'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com'
    ]
    
    recipients = [
        'andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is'
    ]
    
    # Преобразуем в множества
    clients_set, participants_set, recipients_set = convert_to_sets(
        clients, participants, recipients
    )
    
    # Выполняем нужную задачу в зависимости от аргумента
    if task_name == 'call_center':
        result = call_center_task(clients_set, recipients_set)
    elif task_name == 'potential_clients':
        result = potential_clients_task(participants_set, clients_set)
    elif task_name == 'loyalty_program':
        result = loyalty_program_task(clients_set, participants_set)
    else:
        # Если аргумент неверный - вызываем исключение, как требует задание
        raise ValueError(f"Неизвестная задача: {task_name}")
    
    # Выводим результат
    # Поскольку в примерах вывода показаны списки в квадратных скобках,
    # выводим именно так
    print(result)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        # Обрабатываем исключения, включая ValueError для неверных аргументов
        print(f"Ошибка: {e}")
        sys.exit(1)
