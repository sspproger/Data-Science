import sys
import os
from random import randint

# Основной класс
class Research:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def file_reader(self, has_header=True):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError("File not found")
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        
        # Проверка заголовка
        if has_header and len(lines) > 0:
            lines = lines[1:]  # пропускаем заголовок
        
        # Читаем данные
        data = []
        for line in lines:
            values = line.strip().split(',')
            if len(values) == 2:
                data.append([int(values[0]), int(values[1])])
        
        return data


class Calculations:
    def __init__(self, data):
        self.data = data  # теперь data хранится в конструкторе
    
    def counts(self):
        heads = sum(row[0] for row in self.data)
        tails = sum(row[1] for row in self.data)
        return heads, tails
    
    def fractions(self, heads, tails):
        total = heads + tails
        if total == 0:
            return 0.0, 0.0
        
        head_frac = heads / total
        tail_frac = tails / total
        
        # Округление до 4 знаков как в ex03
        head_str = f"{head_frac:.5f}"[:6]  # "0.45454" -> "0.4545"
        tail_str = f"{tail_frac:.5f}"[:6]  # "0.54545" -> "0.5454"
        
        return float(head_str), float(tail_str)

# Наследующий класс
class Analytics(Calculations):  # наследуем от Calculations
    def predict_random(self, num_predictions):
        predictions = []
        for _ in range(num_predictions):
            heads = randint(0, 1)  # случайное значение 0 или 1
            tails = 1 - heads      # противоположное значение
            predictions.append([heads, tails])
        return predictions
    
    def predict_last(self):
        if self.data:
            return self.data[-1]  # последний элемент
        return None

# Основная программа
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 first_child.py data.csv")
        sys.exit(1)
    
    try:
        # 1. Читаем данные
        researcher = Research(sys.argv[1])
        data = researcher.file_reader()
        print(data)
        
        # 2. Создаем аналитику с данными
        analytics = Analytics(data)
        
        # 3. Считаем и выводим counts
        heads, tails = analytics.counts()
        print(f"{heads} {tails}")
        
        # 4. Считаем и выводим fractions
        head_frac, tail_frac = analytics.fractions(heads, tails)
        print(f"{head_frac:.4f} {tail_frac:.4f}")
        
        # 5. Генерируем 3 предсказания
        predictions = analytics.predict_random(3)
        print(predictions)
        
        # 6. Получаем последний элемент
        last = analytics.predict_last()
        print(last)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
