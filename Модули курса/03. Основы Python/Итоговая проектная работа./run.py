"""
Точка входа. Запуск: python run.py
"""
import config
from src.analyzer import OrderAnalyzer


def main():
    analyzer = OrderAnalyzer(
        data_dir=config.DATA_DIR,
        reports_dir=config.REPORTS_DIR,
        logs_dir=config.LOGS_DIR,
        report_filename=config.REPORT_FILENAME,
        log_filename=config.LOG_FILENAME,
        status_column=config.STATUS_COLUMN,
        amount_column=config.AMOUNT_COLUMN,
        delivered_status=config.DELIVERED_STATUS,
        required_columns=config.REQUIRED_COLUMNS,
    )

    report_df = analyzer.process_all_files()
    summary = analyzer.get_summary()

    print("=" * 50)
    print("Итоговый отчёт:")
    print(report_df.to_string(index=False))
    print("=" * 50)
    print(f"Обработано файлов:        {summary['processed']}")
    print(f"Файлов с ошибками:        {summary['errors']}")
    print(f"Отчёт сохранён в:         {analyzer.report_path}")
    print(f"Лог ошибок:               {analyzer.log_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()