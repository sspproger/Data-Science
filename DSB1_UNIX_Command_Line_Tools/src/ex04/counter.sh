#!/bin/sh

INPUT_FILE="../ex03/hh_positions.csv"
OUTPUT_FILE="hh_uniq_positions.csv"

# Проверяем наличие входного файла
if [ ! -f "$INPUT_FILE" ]; then
    echo "Ошибка: входной файл $INPUT_FILE не найден."
    exit 1
fi

# Извлекаем уникальные значения колонки "name", считаем их, сортируем по убыванию
tail -n +2 "$INPUT_FILE" | \
    awk -F ',' '{ print $3 }' | \
    tr -d '"' | \
    sort | \
    uniq -c | \
    sort -rn | \
    awk '{ print "\"" $2 "\"," $1 }' > temp.csv

# Добавляем заголовок
echo '"name","count"' > "$OUTPUT_FILE"
cat temp.csv >> "$OUTPUT_FILE"

# Удаляем временный файл
rm -f temp.csv

echo "Файл $OUTPUT_FILE успешно создан."
