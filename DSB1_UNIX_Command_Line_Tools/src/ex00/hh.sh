#!/bin/sh

if [ $# -eq 0 ]; then
    echo "Ошибка: не указано название вакансии"
    echo "Usage: $0 <vacancy_name>"
    exit 1
fi

# Кодируем пробелы в названии вакансии для URL
VACANCY_NAME=$(echo "$1" | sed 's/ /+/g')
URL="https://api.hh.ru/vacancies?text=$VACANCY_NAME&per_page=20"

# Загружаем данные, извлекаем массив items и форматируем с отступами
curl -s "$URL" | jq '.items' > hh.json

if [ -s hh.json ]; then
    echo "Data saved to hh.json"
    echo "Number of vacancies: $(jq 'length' hh.json)"
else
    echo "Error: Failed to download or process data"
    exit 1
fi
