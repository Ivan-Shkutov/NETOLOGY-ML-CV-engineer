"""
Класс OrderAnalyzer — вся логика чтения, фильтрации и расчёта метрик.
"""
import logging
from pathlib import Path

import pandas as pd


class OrderAnalyzer:
    """Анализирует CSV-файлы с заказами и собирает метрики по доставленным заказам."""

    def __init__(
        self,
        data_dir: Path,
        reports_dir: Path,
        logs_dir: Path,
        report_filename: str,
        log_filename: str,
        status_column: str,
        amount_column: str,
        delivered_status: str,
        required_columns: list,
    ):
        self.data_dir = Path(data_dir)
        self.reports_dir = Path(reports_dir)
        self.logs_dir = Path(logs_dir)
        self.report_path = self.reports_dir / report_filename
        self.log_path = self.logs_dir / log_filename

        self.status_column = status_column
        self.amount_column = amount_column
        self.delivered_status = delivered_status
        self.required_columns = required_columns

        self.processed_count = 0
        self.error_count = 0

        for directory in (self.data_dir, self.reports_dir, self.logs_dir):
            directory.mkdir(parents=True, exist_ok=True)

        self._setup_logger()

    def _setup_logger(self):
        """Настраивает запись ошибок в файл logs/errors.log."""
        self.logger = logging.getLogger("OrderAnalyzer")
        self.logger.setLevel(logging.ERROR)
        self.logger.propagate = False

        if self.logger.handlers:
            self.logger.handlers.clear()

        handler = logging.FileHandler(self.log_path, mode="a", encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _log_error(self, filename: str, message: str):
        """Пишет ошибку в лог и увеличивает счётчик ошибок."""
        self.logger.error(f"Файл '{filename}': {message}")
        self.error_count += 1

    def load_file(self, file_path: Path) -> pd.DataFrame:
        """Загружает CSV и проверяет структуру."""
        if not file_path.exists():
            raise FileNotFoundError("файл не найден")
        if not file_path.is_file():
            raise ValueError("указанный путь ведёт не к файлу")

        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError("файл пуст")

        missing = [col for col in self.required_columns if col not in df.columns]
        if missing:
            raise ValueError(f"отсутствуют обязательные колонки: {missing}")

        if not pd.api.types.is_numeric_dtype(df[self.amount_column]):
            converted = pd.to_numeric(df[self.amount_column], errors="coerce")
            if converted.isna().all():
                raise ValueError(
                    f"колонка '{self.amount_column}' не содержит числовых значений"
                )
            df[self.amount_column] = converted

        return df

    def filter_delivered(self, df: pd.DataFrame) -> pd.DataFrame:
        """Оставляет только заказы со статусом 'Delivered'."""
        return df[df[self.status_column] == self.delivered_status]

    def calculate_metrics(self, df: pd.DataFrame) -> dict:
        """Считает выручку, средний чек и количество заказов."""
        if df.empty:
            return {
                "total_revenue": 0.0,
                "average_check": 0.0,
                "orders_count": 0,
            }

        revenue = float(df[self.amount_column].sum())
        avg_check = float(df[self.amount_column].mean())
        count = int(df.shape[0])

        return {
            "total_revenue": round(revenue, 2),
            "average_check": round(avg_check, 2),
            "orders_count": count,
        }

    def process_file(self, file_path: Path) -> dict | None:
        """Обрабатывает один файл. При ошибке пишет в лог и возвращает None."""
        try:
            df = self.load_file(file_path)
            delivered = self.filter_delivered(df)
            metrics = self.calculate_metrics(delivered)
        except Exception as exc:
            self._log_error(file_path.name, str(exc))
            return None

        self.processed_count += 1
        return {
            "file_name": file_path.name,
            "total_revenue": metrics["total_revenue"],
            "average_check": metrics["average_check"],
            "orders_count": metrics["orders_count"],
        }

    def process_all_files(self) -> pd.DataFrame:
        """Обходит все CSV в data/, собирает метрики и сохраняет отчёт."""
        csv_files = sorted(self.data_dir.glob("*.csv"))

        if not csv_files:
            self.logger.error("В папке data/ не найдено ни одного CSV-файла.")
            empty = pd.DataFrame(
                columns=["file_name", "total_revenue", "average_check", "orders_count"]
            )
            empty.to_csv(self.report_path, index=False, encoding="utf-8")
            return empty

        results = []
        for file_path in csv_files:
            record = self.process_file(file_path)
            if record is not None:
                results.append(record)

        report_df = pd.DataFrame(
            results,
            columns=["file_name", "total_revenue", "average_check", "orders_count"],
        )
        report_df.to_csv(self.report_path, index=False, encoding="utf-8")
        return report_df

    def get_summary(self) -> dict:
        """Возвращает итоговую статистику: сколько обработано, сколько с ошибками."""
        return {
            "processed": self.processed_count,
            "errors": self.error_count,
        }