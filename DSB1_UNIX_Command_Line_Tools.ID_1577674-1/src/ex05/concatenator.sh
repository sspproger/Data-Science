#!/bin/sh

# concatenator.sh - объединяет разделенные CSV-файлы обратно в один

OUTPUT_FILE="merged_hh_positions.csv"

# Находим все CSV-файлы с именами в формате YYYY-MM-DD.csv
# Сортируем их по имени (что соответствует хронологическому порядку)
FILES=$(ls -1v [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].csv 2>/dev/null | sort)

# Проверяем, есть ли файлы для объединения
if [ -z "$FILES" ]; then
    echo "Ошибка: Не найдены файлы для объединения."
    echo "Сначала запустите partitioner.sh для создания файлов по датам."
    exit 1
fi

echo "Найдены файлы для объединения:"
echo "$FILES"
echo ""

# Берем заголовок из первого файла
FIRST_FILE=$(echo "$FILES" | head -n 1)
HEADER=$(head -n 1 "$FIRST_FILE")

# Записываем заголовок в выходной файл
echo "$HEADER" > "$OUTPUT_FILE"

# Объединяем данные из всех файлов (без заголовков)
for FILE in $FILES
do
    # Проверяем, что файл не пустой и содержит данные кроме заголовка
    if [ $(wc -l < "$FILE") -gt 1 ]; then
        tail -n +2 "$FILE" >> "$OUTPUT_FILE"
        echo "Добавлены данные из: $FILE"
    else
        echo "Пропущен пустой файл (только заголовок): $FILE"
    fi
done

# Проверяем количество строк в итоговом файле
TOTAL_LINES=$(wc -l < "$OUTPUT_FILE")
echo ""
echo "Объединение завершено!"
echo "Создан файл: $OUTPUT_FILE"
echo "Всего строк (включая заголовок): $TOTAL_LINES"
echo ""

# Проверяем, что файл не пустой
if [ "$TOTAL_LINES" -le 1 ]; then
    echo "Предупреждение: Выходной файл содержит только заголовок или пуст."
fi
