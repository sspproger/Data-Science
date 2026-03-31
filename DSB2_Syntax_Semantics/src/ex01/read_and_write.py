def convert_csv_to_tsv():
    try:
        with open('ds.csv', 'r', encoding='utf-8') as csv_file:
            lines = csv_file.readlines()
        
        tsv_lines = []
        
        for line in lines:
            # Пропускаем только полностью пустые строки (после удаления пробелов и переносов)
            if not line.strip():
                continue
            
            fields = []
            current_field = ''
            in_quotes = False
            
            i = 0
            while i < len(line):
                char = line[i]
                
                if char == '"':
                    # Проверяем, является ли это escaped кавычкой (две кавычки подряд внутри quoted поля)
                    if i + 1 < len(line) and line[i + 1] == '"' and in_quotes:
                        current_field += '"'
                        i += 1  # Пропускаем следующую кавычку
                    else:
                        # Это начало или конец quoted поля
                        in_quotes = not in_quotes
                
                elif char == ',' and not in_quotes:
                    # Нашли разделитель вне quoted поля
                    fields.append(current_field)
                    current_field = ''
                
                else:
                    current_field += char
                
                i += 1
            
            # Добавляем последнее поле (последняя запятая уже обработана в цикле)
            fields.append(current_field)
            
            # Убираем возможные переносы строк в конце последнего поля
            if fields[-1].endswith('\n'):
                fields[-1] = fields[-1].rstrip('\n')
            
            # Если есть поля, добавляем строку в результат
            if fields:
                tsv_lines.append('\t'.join(fields))
        
        # Записываем результат
        with open('ds.tsv', 'w', encoding='utf-8') as tsv_file:
            tsv_file.write('\n'.join(tsv_lines))
    
    except FileNotFoundError:
        return


if __name__ == '__main__':
    convert_csv_to_tsv()
