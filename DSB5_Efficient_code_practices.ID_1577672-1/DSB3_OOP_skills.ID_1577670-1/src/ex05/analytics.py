import os
from random import randint

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def file_reader(self, has_header=True):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError("File not found")
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        
        if has_header and len(lines) > 0:
            lines = lines[1:]
        
        data = []
        for line in lines:
            values = line.strip().split(',')
            if len(values) == 2:
                data.append([int(values[0]), int(values[1])])
        
        return data

class Calculations:
    def __init__(self, data):
        self.data = data
    
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
        
        head_str = f"{head_frac:.5f}"[:6]
        tail_str = f"{tail_frac:.5f}"[:6]
        
        return float(head_str), float(tail_str)

class Analytics(Calculations):
    def predict_random(self, num_predictions):
        predictions = []
        for _ in range(num_predictions):
            heads = randint(0, 1)
            tails = 1 - heads
            predictions.append([heads, tails])
        return predictions
    
    def predict_last(self):
        if self.data:
            return self.data[-1]
        return None
    
    def save_file(self, data, filename, extension='txt'):
        full_filename = f"{filename}.{extension}"
        with open(full_filename, 'w') as file:
            file.write(data)
        return full_filename
