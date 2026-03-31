#!/usr/bin/sh

INPUT_FILE="../ex02/hh_sorted.csv"
OUTPUT_FILE="hh_positions.csv"

# Проверяем, установлен ли Miller
if command -v mlr >/dev/null 2>&1; then
    # Используем Miller для обработки с кавычками
    mlr --csv --quote-all put '
        $name = tolower($name);
        
        # Формируем результат без промежуточных переменных
        if ($name =~ "junior" && $name =~ "middle" && $name =~ "senior") {
            $name = "Junior/Middle/Senior";
        } elif ($name =~ "junior" && $name =~ "middle") {
            $name = "Junior/Middle";
        } elif ($name =~ "junior" && $name =~ "senior") {
            $name = "Junior/Senior";
        } elif ($name =~ "middle" && $name =~ "senior") {
            $name = "Middle/Senior";
        } elif ($name =~ "junior") {
            $name = "Junior";
        } elif ($name =~ "middle") {
            $name = "Middle";
        } elif ($name =~ "senior") {
            $name = "Senior";
        } else {
            $name = "-";
        }
    ' "$INPUT_FILE" > "$OUTPUT_FILE"
else
    # Запасной вариант на Python (уже включает кавычки)
    python3 -c "
import csv
import sys

input_file = '$INPUT_FILE'
output_file = '$OUTPUT_FILE'

with open(input_file, 'r', encoding='utf-8') as f_in, \
     open(output_file, 'w', encoding='utf-8', newline='') as f_out:
    
    reader = csv.DictReader(f_in)
    writer = csv.DictWriter(f_out, fieldnames=reader.fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    
    for row in reader:
        name = row['name']
        name_lower = name.lower()
        result = []
        
        if 'junior' in name_lower:
            result.append('Junior')
        if 'middle' in name_lower:
            result.append('Middle')
        if 'senior' in name_lower:
            result.append('Senior')
        
        if result:
            row['name'] = '/'.join(result)
        else:
            row['name'] = '-'
        
        writer.writerow(row)
" || echo "Ошибка: установите Python3 или Miller для обработки CSV"
fi
