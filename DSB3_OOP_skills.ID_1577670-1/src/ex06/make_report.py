import sys
import logging
from analytics import Research, Analytics
import config

# Настройка логирования для make_report
logging.basicConfig(
    filename='analytics.log',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main():
    logging.debug("Starting make_report program")
    
    if len(sys.argv) != 2:
        error_msg = "Usage: python3 make_report.py data.csv"
        logging.error(error_msg)
        print(error_msg)
        sys.exit(1)
    
    researcher = Research(sys.argv[1])
    
    try:
        # 1. Читаем данные
        logging.debug("Reading data from file")
        data = researcher.file_reader()
        
        # 2. Создаем аналитику
        logging.debug("Creating Analytics instance")
        analytics = Analytics(data)
        
        # 3. Получаем статистику
        logging.debug("Getting counts")
        heads, tails = analytics.counts()
        total = heads + tails
        
        # 4. Получаем вероятности
        logging.debug("Calculating fractions")
        head_frac, tail_frac = analytics.fractions(heads, tails)
        
        # 5. Генерируем предсказания
        logging.debug(f"Generating {config.num_of_steps} predictions")
        predictions = analytics.predict_random(config.num_of_steps)
        
        # 6. Считаем предсказания
        heads_predicted = sum(p[0] for p in predictions)
        tails_predicted = sum(p[1] for p in predictions)
        
        # 7. Формируем отчет
        logging.debug("Formatting report")
        report = config.REPORT_TEMPLATE.format(
            total=total,
            tails=tails,
            heads=heads,
            tail_percent=tail_frac * 100,
            head_percent=head_frac * 100,
            num_predictions=config.num_of_steps,
            tails_predicted=tails_predicted,
            heads_predicted=heads_predicted
        )
        
        # 8. Сохраняем отчет
        logging.debug("Saving report to file")
        filename = analytics.save_file(report, "report", "txt")
        print(f"Report saved to {filename}")
        
        # 9. Отправляем сообщение в Telegram
        logging.debug("Sending success message to Telegram")
        success = researcher.send_to_telegram("The report has been successfully created")
        if success:
            print("Telegram notification sent: Success")
        else:
            print("Telegram notification failed")
        
        logging.info("Program completed successfully")
        
    except Exception as e:
        error_msg = f"Error: {e}"
        logging.error(error_msg)
        print(error_msg)
        
        # Отправляем сообщение об ошибке в Telegram
        try:
            researcher.send_to_telegram("The report hasn't been created due to an error")
            print("Telegram notification sent: Error")
        except:
            print("Failed to send Telegram error notification")
        
        sys.exit(1)

if __name__ == '__main__':
    main()
