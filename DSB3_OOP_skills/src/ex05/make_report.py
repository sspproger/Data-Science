import sys
from analytics import Research, Analytics
import config

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 make_report.py data.csv")
        sys.exit(1)
    
    try:
        # 1. Читаем данные
        researcher = Research(sys.argv[1])
        data = researcher.file_reader()
        
        # 2. Создаем аналитику
        analytics = Analytics(data)
        
        # 3. Получаем статистику
        heads, tails = analytics.counts()
        total = heads + tails
        
        # 4. Получаем вероятности
        head_frac, tail_frac = analytics.fractions(heads, tails)
        
        # 5. Генерируем предсказания
        predictions = analytics.predict_random(config.num_of_steps)
        
        # 6. Считаем предсказания
        heads_predicted = sum(p[0] for p in predictions)
        tails_predicted = sum(p[1] for p in predictions)
        
        # 7. Формируем отчет
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
        filename = analytics.save_file(report, "report", "txt")
        print(f"Report saved to {filename}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
