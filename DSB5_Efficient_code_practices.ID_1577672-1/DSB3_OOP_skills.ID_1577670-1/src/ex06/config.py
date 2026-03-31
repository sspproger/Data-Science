# Конфигурационные параметры
num_of_steps = 3  # количество предсказаний

# Шаблон отчета
REPORT_TEMPLATE = """Report:

We made {total} observations by tossing a coin: {tails} were tails and {heads} were heads.
The probabilities are {tail_percent:.2f}% and {head_percent:.2f}%, respectively.
Our forecast is that the next {num_predictions} observations will be: {tails_predicted} tail(s) and {heads_predicted} head(s).
"""

# Telegram webhook (пример - нужно заменить на реальный URL)
TELEGRAM_WEBHOOK_URL = "https://api.telegram.org/botYOUR_TOKEN/sendMessage"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"
