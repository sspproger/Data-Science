def dict_sorter():
    # Исходный список кортежей (такой же как в ex04)
    list_of_tuples = [
        ('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')
    ]

    # 1. Создаём словарь: ключ - страна, значение - число (как int)
    country_dict = {}
    for country, number in list_of_tuples:
        country_dict[country] = int(number)

    # 2. Сортируем словарь по двум критериям:
    #    - По значению (числу) в порядке убывания (-x[1])
    #    - По ключу (названию страны) в алфавитном порядке (x[0])
    sorted_items = sorted(country_dict.items(), key=lambda x: (-x[1], x[0]))

    # 3. Выводим только названия стран (без чисел)
    for country, _ in sorted_items:
        print(country)


if __name__ == '__main__':
    dict_sorter()
