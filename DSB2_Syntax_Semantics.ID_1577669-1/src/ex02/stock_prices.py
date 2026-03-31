import sys

def get_stock_price():
    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK',
	'Samsung': 'SAM'
    }
    
    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37,
	'SAM': 11.55
    }
    
    # Проверка количества аргументов
    if len(sys.argv) != 2:
        return
    
    # Получение названия компании из аргументов
    company_name = sys.argv[1]
    
    # Поиск компании (регистронезависимый)
    company_key = None
    for key in COMPANIES:
        if key.lower() == company_name.lower():
            company_key = key
            break
    
    # Если компания найдена, выводим цену акции
    if company_key:
        ticker = COMPANIES[company_key]
        price = STOCKS[ticker]
        print(price)
    else:
        print("Unknown company")

if __name__ == '__main__':
    get_stock_price()
