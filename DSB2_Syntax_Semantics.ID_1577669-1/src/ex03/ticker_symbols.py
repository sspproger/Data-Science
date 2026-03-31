import sys

def main():
    # Словарь компаний и их тикеров
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }
    
    # Словарь тикеров и цен акций
    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }
    
    # Проверяем количество аргументов
    if len(sys.argv) != 2:
        return  # Ничего не делаем при неправильном количестве аргументов
    
    # Получаем введенный тикер
    user_ticker = sys.argv[1]
    
    # Ищем компанию по тикеру
    found_company = None
    correct_ticker = None
    
    for company, ticker in COMPANIES.items():
        # Сравниваем без учета регистра
        if ticker.lower() == user_ticker.lower():
            found_company = company
            correct_ticker = ticker  # Сохраняем тикер в правильном регистре
            break
    
    # Если нашли компанию - выводим результат
    if found_company and correct_ticker:
        stock_price = STOCKS[correct_ticker]
        print(f"{found_company} {stock_price}")
    else:
        print("Unknown ticker")

if __name__ == '__main__':
    main()
