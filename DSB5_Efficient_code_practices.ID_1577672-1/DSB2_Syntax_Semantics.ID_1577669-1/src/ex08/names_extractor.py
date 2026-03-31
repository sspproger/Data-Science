import sys

def main():
    # Проверяем количество аргументов
    if len(sys.argv) != 2:
        print("Usage: python names_extractor.py <input_file>")
        return
    
    input_file = sys.argv[1]
    
    try:
        # Открываем входной файл
        with open(input_file, 'r', encoding='utf-8') as f:
            # Открываем выходной файл для записи
            with open("employees.tsv", 'w', encoding='utf-8') as out_f:
                # Пишем заголовок в TSV файл
                out_f.write("Name\tSurname\tEmail\n")
                
                # Читаем каждый email из входного файла
                for line in f:
                    email = line.strip()
                    
                    # Пропускаем пустые строки
                    if not email:
                        continue
                    
                    # Разделяем email на части
                    if '@' in email:
                        # Получаем часть до @ (имя.фамилия)
                        name_part = email.split('@')[0]
                        
                        if '.' in name_part:
                            # Разделяем имя и фамилию
                            name, surname = name_part.split('.')
                            
                            # Делаем первую букву заглавной
                            name = name.capitalize()
                            surname = surname.capitalize()
                            
                            # Записываем в TSV файл
                            out_f.write(f"{name}\t{surname}\t{email}\n")
                        else:
                            print(f"Warning: No dot in name part: {email}", file=sys.stderr)
                    else:
                        print(f"Warning: Invalid email format (no @): {email}", file=sys.stderr)
        
        print(f"File employees.tsv created successfully from {input_file}")
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
