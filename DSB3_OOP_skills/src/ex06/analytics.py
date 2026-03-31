import os
import logging
from random import randint
import requests
import config

# Настройка логирования
logging.basicConfig(
    filename='analytics.log',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Research:
    def __init__(self, file_path):
        self.file_path = file_path
        logging.debug(f"Research class initialized with file: {file_path}")
    
    def file_reader(self, has_header=True):
        logging.debug("Reading file with file_reader method")
        if not os.path.exists(self.file_path):
            error_msg = f"File not found: {self.file_path}"
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        
        if has_header and len(lines) > 0:
            lines = lines[1:]
        
        data = []
        for line in lines:
            values = line.strip().split(',')
            if len(values) == 2:
                data.append([int(values[0]), int(values[1])])
        
        logging.debug(f"Successfully read {len(data)} observations")
        return data
    
    def send_to_telegram(self, message):
        """Отправляет сообщение в Telegram"""
        logging.debug(f"Sending message to Telegram: {message}")
        try:
            # Создаем данные для отправки
            data = {
                'chat_id': config.TELEGRAM_CHAT_ID,
                'text': message
            }
            
            # Отправляем запрос (в реальном проекте нужен реальный URL)
            # response = requests.post(config.TELEGRAM_WEBHOOK_URL, json=data)
            # response.raise_for_status()
            
            logging.info(f"Telegram message sent: {message}")
            return True
        except Exception as e:
            logging.error(f"Failed to send Telegram message: {e}")
            return False

class Calculations:
    def __init__(self, data):
        self.data = data
        logging.debug("Calculations class initialized with data")
    
    def counts(self):
        logging.debug("Calculating counts of heads and tails")
        heads = sum(row[0] for row in self.data)
        tails = sum(row[1] for row in self.data)
        logging.info(f"Counts calculated: heads={heads}, tails={tails}")
        return heads, tails
    
    def fractions(self, heads, tails):
        logging.debug("Calculating fractions")
        total = heads + tails
        if total == 0:
            logging.warning("Total is zero, returning default fractions")
            return 0.0, 0.0
        
        head_frac = heads / total
        tail_frac = tails / total
        
        head_str = f"{head_frac:.5f}"[:6]
        tail_str = f"{tail_frac:.5f}"[:6]
        
        logging.info(f"Fractions calculated: heads={head_str}, tails={tail_str}")
        return float(head_str), float(tail_str)

class Analytics(Calculations):
    def predict_random(self, num_predictions):
        logging.debug(f"Generating {num_predictions} random predictions")
        predictions = []
        for i in range(num_predictions):
            heads = randint(0, 1)
            tails = 1 - heads
            predictions.append([heads, tails])
            logging.debug(f"Prediction {i+1}: heads={heads}, tails={tails}")
        
        logging.info(f"Generated {len(predictions)} predictions")
        return predictions
    
    def predict_last(self):
        logging.debug("Getting last observation")
        if self.data:
            last = self.data[-1]
            logging.info(f"Last observation: {last}")
            return last
        logging.warning("No data available for last observation")
        return None
    
    def save_file(self, data, filename, extension='txt'):
        logging.debug(f"Saving file: {filename}.{extension}")
        full_filename = f"{filename}.{extension}"
        try:
            with open(full_filename, 'w') as file:
                file.write(data)
            logging.info(f"File saved successfully: {full_filename}")
            return full_filename
        except Exception as e:
            logging.error(f"Failed to save file {full_filename}: {e}")
            raise
