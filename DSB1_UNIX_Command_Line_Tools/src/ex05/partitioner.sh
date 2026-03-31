#!/bin/sh

# partitioner.sh - разделяет hh_positions.csv на файлы по датам

INPUT_FILE="../ex03/hh_positions.csv"

# Проверяем существование входного файла
if [ ! -f "$INPUT_FILE" ]; then
    echo "Ошибка: Файл $INPUT_FILE не найден в текущей директории."
    echo "Убедитесь, что вы находитесь в директории ex05 и файл существует."
    exit 1
fi

# Извлекаем заголовок
HEADER=$(head -n 1 "$INPUT_FILE")

# Читаем файл построчно, начиная со второй строки
tail -n +2 "$INPUT_FILE" | while IFS= read -r LINE
do
    # Извлекаем дату из поля created_at (формат: "2020-04-11T18:03:53+0300")
    # Убираем кавычки, берем первые 10 символов
    DATE=$(echo "$LINE" | awk -F',' '{print $2}' | tr -d '"' | cut -c1-10)
    
    # Проверяем, что дата корректна (содержит дефисы)
    if echo "$DATE" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'; then
        OUTPUT_FILE="${DATE}.csv"
        
        # Если файл еще не существует, записываем заголовок
        if [ ! -f "$OUTPUT_FILE" ]; then
            echo "$HEADER" > "$OUTPUT_FILE"
        fi
        
        # Добавляем строку в соответствующий файл
        echo "$LINE" >> "$OUTPUT_FILE"
    else
        echo "Предупреждение: Не удалось извлечь дату из строки: $LINE" >&2
    fi
done

echo "Разделение завершено. Созданы файлы по датам."
