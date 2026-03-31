import sys

def main():
    # Проверяем количество аргументов
    if len(sys.argv) != 2:
        print("Usage: python letter_starter.py <email>")
        return
    
    email_to_find = sys.argv[1]
    
    try:
        # Открываем файл employees.tsv для чтения
        with open("employees.tsv", 'r', encoding='utf-8') as file:
            # Пропускаем первую строку (заголовок)
            next(file)
            
            found = False
            # Читаем файл построчно
            for line in file:
                # Разделяем строку по табуляции
                parts = line.strip().split('\t')
                
                # Проверяем, что строка имеет правильный формат
                if len(parts) == 3:
                    name, surname, email = parts
                    
                    # Сравниваем email (игнорируем регистр)
                    if email.lower() == email_to_find.lower():
                        # Формируем приветствие с помощью f-string
                        greeting = f"Dear {name}, welcome to our team! We are sure that it will be a pleasure to work with you. That's a precondition for the professionals that our company hires."
                        print(greeting)
                        found = True
                        break
            
            if not found:
                print(f"Error: Email '{email_to_find}' not found in employees.tsv")
                
    except FileNotFoundError:
        print("Error: File employees.tsv not found")
        print("Please run names_extractor.py first to create employees.tsv")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
