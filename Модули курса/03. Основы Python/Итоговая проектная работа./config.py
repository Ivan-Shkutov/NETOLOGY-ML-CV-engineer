"""
Конфигурация проекта: все настройки в одном месте.
"""
from pathlib import Path

# Корневая директория проекта
BASE_DIR = Path(__file__).resolve().parent

# Пути к папкам
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

# Имена файлов результатов
REPORT_FILENAME = "summary_report.csv"
LOG_FILENAME = "errors.log"

# Настройки фильтрации
STATUS_COLUMN = "status"
AMOUNT_COLUMN = "total_amount"
DELIVERED_STATUS = "Delivered"

# Обязательные колонки во входном файле
REQUIRED_COLUMNS = [
    "order_id",
    "person_id",
    "order_date",
    "status",
    "total_amount",
    "currency",
    "payment_method",
    "shipping_method",
    "notes",
]