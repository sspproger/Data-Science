import sys

def caesar_cipher(text, shift, mode='encode'):
    """
    Шифрует или дешифрует текст с помощью шифра Цезаря.
    mode: 'encode' или 'decode'
    """
    result = []
    for char in text:
        if char.isalpha():
            # Проверяем, латинский ли символ
            if not ('a' <= char <= 'z' or 'A' <= char <= 'Z'):
                raise ValueError("The script does not support your language yet.")
            
            # Определяем базовый код символа (для 'a' или 'A')
            base = ord('a') if char.islower() else ord('A')
            # Сдвигаем символ
            if mode == 'encode':
                shifted = (ord(char) - base + shift) % 26
            else:  # decode
                shifted = (ord(char) - base - shift) % 26
            new_char = chr(base + shifted)
            result.append(new_char)
        else:
            # Если символ не буква, оставляем как есть
            result.append(char)
    return ''.join(result)

def main():
    # Проверка количества аргументов
    if len(sys.argv) != 4:
        raise Exception("Usage: python3 caesar.py <encode|decode> <text> <shift>")
    
    mode = sys.argv[1].lower()
    text = sys.argv[2]
    try:
        shift = int(sys.argv[3])
    except ValueError:
        raise Exception("Shift must be an integer.")
    
    if mode not in ['encode', 'decode']:
        raise Exception("Mode must be 'encode' or 'decode'.")
    
    try:
        result = caesar_cipher(text, shift, mode)
        print(result)
    except ValueError as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
