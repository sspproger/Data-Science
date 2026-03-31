import sys
import os

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def file_reader(self, has_header=True):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} not found")
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        
        # Проверка формата (как в ex02)
        if len(lines) < 2:
            raise ValueError("File must contain at least 2 lines")
        
        header = lines[0].strip().split(',')
        if len(header) != 2:
            raise ValueError("Header must contain exactly 2 columns")
        
        for i, line in enumerate(lines[1:], 1):
            values = line.strip().split(',')
            if len(values) != 2:
                raise ValueError(f"Line {i}: must contain exactly 2 values")
            if values[0] not in ['0', '1'] or values[1] not in ['0', '1']:
                raise ValueError(f"Line {i}: values must be 0 or 1")
            if values[0] == values[1]:
                raise ValueError(f"Line {i}: values cannot be the same")
        
        # Пропускаем заголовок если есть
        start_line = 1 if has_header and len(lines) > 0 else 0
        
        # Возвращаем список списков
        result = []
        for line in lines[start_line:]:
            values = line.strip().split(',')
            result.append([int(values[0]), int(values[1])])
        
        return result
    
    class Calculations:
        def counts(self, data):
            heads = sum(row[0] for row in data)
            tails = sum(row[1] for row in data)
            return heads, tails
        
        def fractions(self, heads, tails):
            total = heads + tails
            if total == 0:
                return 0.0, 0.0
            
            head_frac = heads / total
            tail_frac = tails / total
            
            # Математическое округление до 4 знаков (как в задании)
            # Форматируем до 5 знаков и берем первые 5 символов
            head_str = f"{head_frac:.5f}"[:6]  # "0.45454" -> "0.4545"
            tail_str = f"{tail_frac:.5f}"[:6]  # "0.54545" -> "0.5454"
            
            return float(head_str), float(tail_str)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 first_nest.py <file_path>")
        sys.exit(1)
    
    try:
        research = Research(sys.argv[1])
        data = research.file_reader()
        
        # Выводим данные из file_reader()
        print(data)
        
        # Создаем экземпляр вложенного класса
        calc = research.Calculations()
        
        # Получаем и выводим counts
        heads, tails = calc.counts(data)
        print(f"{heads} {tails}")
        
        # Получаем и выводим fractions
        head_frac, tail_frac = calc.fractions(heads, tails)
        print(f"{head_frac:.4f} {tail_frac:.4f}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
