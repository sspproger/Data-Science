import sys

def all_stocks():
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
    }
    
    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
    }
    
    # Проверяем количество аргументов
    if len(sys.argv) != 2:
        return
    
    # Получаем строку с аргументами
    input_str = sys.argv[1]
    
    # Разделяем по запятым
    elements = input_str.split(',')
    
    # Очищаем элементы от пробелов и проверяем на пустоту
    cleaned_elements = []
    for elem in elements:
        elem = elem.strip()
        if elem == '':
            # Если есть пустой элемент (две запятые подряд), выходим
            return
        cleaned_elements.append(elem)
    
    # Создаем нормализованные версии словарей для поиска без учета регистра
    companies_lower = {k.lower(): v for k, v in COMPANIES.items()}
    stocks_lower = {k.lower(): v for k, v in STOCKS.items()}
    
    # Для каждого элемента определяем тип
    results = []
    for elem in cleaned_elements:
        elem_lower = elem.lower()
        
        # Проверяем, является ли тикером
        if elem_lower in stocks_lower:
            # Находим оригинальное название компании по тикеру
            company_name = None
            for comp_name, ticker in COMPANIES.items():
                if ticker.lower() == elem_lower:
                    company_name = comp_name
                    break
            
            if company_name:
                # Форматируем тикер как в примере (верхний регистр)
                ticker_formatted = elem.upper() if elem.isupper() else COMPANIES[company_name]
                results.append(f"{ticker_formatted} is a ticker symbol for {company_name}")
        
        # Проверяем, является ли названием компании
        elif elem_lower in companies_lower:
            company_name = None
            # Находим оригинальное название с правильным регистром
            for comp_name in COMPANIES:
                if comp_name.lower() == elem_lower:
                    company_name = comp_name
                    break
            
            if company_name:
                ticker = COMPANIES[company_name]
                price = STOCKS[ticker]
                # Сохраняем оригинальный регистр из ввода для названия компании
                company_formatted = elem if elem[0].isupper() else company_name
                results.append(f"{company_formatted} stock price is {price}")
        
        # Неизвестная компания/тикер
        else:
            results.append(f"{elem} is an unknown company or an unknown ticker symbol")
    
    # Выводим результаты
    for result in results:
        print(result)

if __name__ == '__main__':
    all_stocks()
