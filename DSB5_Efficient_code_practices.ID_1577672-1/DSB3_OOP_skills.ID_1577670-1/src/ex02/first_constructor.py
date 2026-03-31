import sys
import os

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def file_reader(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"File {self.file_path} not found")
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        
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
        
        return ''.join(lines)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 first_constructor.py <file_path>")
        sys.exit(1)
    
    try:
        research = Research(sys.argv[1])
        print(research.file_reader(), end='')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
