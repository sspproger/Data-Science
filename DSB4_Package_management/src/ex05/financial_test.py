#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys
import time
import re
import pytest
import io
from contextlib import redirect_stdout
from unittest.mock import Mock, patch

def parse_html(response, field):
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('div', {'class': re.compile('row lv-0')})
    if not rows:
        raise Exception('Financial data table not found for the given ticker')

    for row in rows:
        financial_field = row.find('div', {'class': re.compile('rowTitle')})
        if financial_field and financial_field.text.strip() == field:
                values = row.find_all('div', {'class': re.compile('column yf-')})
                txt = [value.text.strip() for value in values]
                return tuple(txt)

    raise Exception(f'Financial field "{field}" not found in the statement') 

def main():
    try:
        ticker = sys.argv[1]
        field = sys.argv[2]
        url = f'https://finance.yahoo.com/quote/{ticker}/financials'
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 YaBrowser/25.12.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f'Failed to fetch data (HTTP status code: {response.status_code})')
        values = parse_html(response, field)
        time.sleep(5)
        print((field, *values))
    except Exception as e:
        print(e)

def test_parse_html_returns_correct_values():
    """Тест 1: Проверка корректного поля - возвращает правильные значения"""
    
    # Создаём мок-объект response с HTML-данными
    mock_response = Mock()
    mock_response.text = '''
    <html>
        <body>
            <div class="row lv-0">
                <div class="rowTitle">Total Revenue</div>
                <div class="column yf-1">134,249,000</div>
                <div class="column yf-2">125,843,000</div>
                <div class="column yf-3">110,360,000</div>
            </div>
            <div class="row lv-0">
                <div class="rowTitle">Cost of Revenue</div>
                <div class="column yf-1">42,910,000</div>
                <div class="column yf-2">40,261,000</div>
            </div>
        </body>
    </html>
    '''
    
    # Вызываем функцию с тестовыми данными
    result = parse_html(mock_response, "Total Revenue")
    
    # Проверяем, что возвращаются правильные значения
    expected = ("134,249,000", "125,843,000", "110,360,000")
    assert result == expected, f"Ожидалось {expected}, получено {result}"

def test_parse_html_field_not_found():
    """Тест 2: Проверка исключения для несуществующего поля"""
    
    mock_response = Mock()
    mock_response.text = '''
    <div class="row lv-0">
        <div class="rowTitle">Total Revenue</div>
        <div class="column yf-1">100,000</div>
    </div>
    '''
    
    # Проверяем, что при запросе несуществующего поля возникает исключение
    with pytest.raises(Exception) as exc_info:
        parse_html(mock_response, "Non Existent Field")
    
    # Проверяем текст исключения
    assert 'Financial field "Non Existent Field" not found' in str(exc_info.value)

def test_parse_html_multiple_matches():
    """Тест 3: Проверка обработки нескольких совпадений"""
    
    mock_response = Mock()
    mock_response.text = '''
    <div class="row lv-0">
        <div class="rowTitle">Revenue</div>
        <div class="column yf-1">50,000</div>
    </div>
    <div class="row lv-0">
        <div class="rowTitle">Total Revenue</div>
        <div class="column yf-1">100,000</div>
        <div class="column yf-2">200,000</div>
    </div>
    <div class="row lv-0">
        <div class="rowTitle">Other Revenue</div>
        <div class="column yf-1">30,000</div>
    </div>
    '''
    
    # Должен найти именно "Total Revenue", а не просто "Revenue"
    result = parse_html(mock_response, "Total Revenue")
    expected = ("100,000", "200,000")
    assert result == expected   

def test_parse_html_return_type():
    """Тест 4: Проверка типа возвращаемого значения"""
    
    mock_response = Mock()
    mock_response.text = '''
    <div class="row lv-0">
        <div class="rowTitle">Total Revenue</div>
        <div class="column yf-1">100,000</div>
        <div class="column yf-2">200,000</div>
    </div>
    '''
    
    result = parse_html(mock_response, "Total Revenue")
    # Проверяем, что возвращается tuple 
    assert isinstance(result, tuple), f"Ожидался tuple, получен {type(result)}"
    # Дополнительные проверки
    assert len(result) == 2
    assert result[0] == "100,000"
    assert result[1] == "200,000"  


def test_main_invalid_ticker():
    """Тест 1: Проверка main с неверным тикером (404 ошибка)"""
    
    mock_response = Mock()
    mock_response.status_code = 404     # Страница не найдена
    
    with patch('sys.argv', ['financial_test.py', 'INVALID_TICKER', 'Total Revenue']), \
         patch('requests.get', return_value=mock_response):
        
        f = io.StringIO()               # Создаем буфер в памяти для записи вывода
        with redirect_stdout(f):        # Перенаправляем stdout в буфер f
            main()                      # Запускаем main(), её вывод пойдет в f, а не в консоль
        
        output = f.getvalue().strip()   # Получаем всё, что было "напечатано"
        
        # Проверяем, что выведена ошибка
        assert "Failed to fetch data" in output
        assert "404" in output
        
def test_main_table_not_found():
    """Тест 2: Проверка main, когда таблица не найдена на странице"""
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '''
    <html>
        <body>
            <h1>MSFT Stock</h1>
            <p>No financial table here</p>
        </body>
    </html>
    '''
    
    with patch('sys.argv', ['financial_test.py', 'MSFT', 'Total Revenue']), \
         patch('requests.get', return_value=mock_response):
        
        f = io.StringIO()
        with redirect_stdout(f):
            main()
        
        output = f.getvalue().strip()
        
        # Проверяем, что выведена ошибка о таблице
        assert "Financial data table not found" in output

def test_main_missing_arguments():
    """Тест 3: Проверка main с недостающими аргументами"""
    
    #Нет аргументов вообще
    original_argv = sys.argv.copy()
    try:
        sys.argv = ['financial_test.py']
        
        f = io.StringIO()
        with redirect_stdout(f):
            main()
        
        output = f.getvalue().strip()
        assert output != ""  # Должна быть какая-то ошибка
        assert "list index out of range" in output or "Exception" in output
    finally:
        sys.argv = original_argv   

def test_main_field_not_found():
    """Тест 4: Проверка main, когда поле не найдено"""
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '''
    <div class="row lv-0">
        <div class="rowTitle">Net Income</div>
        <div class="column yf-1">50,000</div>
    </div>
    '''
    
    with patch('sys.argv', ['financial_test.py', 'AAPL', 'Total Revenue']), \
         patch('requests.get', return_value=mock_response):
        
        f = io.StringIO()
        with redirect_stdout(f):
            main()
        
        output = f.getvalue().strip()
        # Проверяем, что выведена ошибка о поле
        assert 'Financial field "Total Revenue" not found' in output  

def test_main_valid_input():
    """Тест 5: Проверка main с корректными аргументами"""
    
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = '''
    <div class="row lv-0">
        <div class="rowTitle">Total Revenue</div>
        <div class="column yf-1">134,249,000</div>
        <div class="column yf-2">125,843,000</div>
    </div>
    '''
    
    with patch('sys.argv', ['financial_test.py', 'MSFT', 'Total Revenue']), \
         patch('requests.get', return_value=mock_response), \
         patch('time.sleep'):  # Мокаем sleep, чтобы тест не ждал 5 секунд
        
        f = io.StringIO()
        with redirect_stdout(f):
            main()
        
        output = f.getvalue().strip()
        
        # Проверяем вывод 
        assert "Total Revenue" in output
        assert "134,249,000" in output
        assert "125,843,000" in output
        # Проверяем, что вывод в формате tuple
        assert output.startswith("(") and output.endswith(")")                                    

if __name__ == '__main__':
    main()