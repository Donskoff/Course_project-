import json
import logging
from datetime import datetime, timedelta
from typing import Any, Callable, Optional

import pandas as pd

from config import PATH_TO_OPERATIONS

# Настройка логирования
logging.basicConfig(level=logging.INFO)

path = PATH_TO_OPERATIONS


def fload_excel(path):
    """Считываем данные из файла Excel."""
    operations = pd.read_excel(path)
    return operations


def report_decorator(file_name: Optional[str] = None):
    """
    Декоратор для функций-отчетов, который записывает результат выполнения функции в файл.

    :param file_name: Имя файла для записи отчета. Если не указано, используется my_report.json.
    """

    def decorator(func: Callable[[pd.DataFrame, str, Optional[str]], pd.DataFrame]) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            # Вызываем оригинальную функцию и получаем результат
            result = func(*args, **kwargs)
            # Определяем имя файла для записи
            output_file_name = file_name if file_name is not None else "my_report.json"
            # Преобразуем Timestamp в строку перед записью в JSON
            if "Дата операции" in result.columns:
                result["Дата операции"] = result["Дата операции"].dt.strftime("%d.%m.%Y %H:%M:%S")
            # Записываем результат в файл в формате JSON
            with open(output_file_name, "w", encoding="utf-8") as f:
                json.dump(result.to_dict(orient="records"), f, indent=4, ensure_ascii=False)
            logging.info(f"Report written to {output_file_name}")
            return result

        return wrapper

    return decorator


@report_decorator()  # Декоратор без параметров
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция для получения трат по заданной категории за последние три месяца от указанной даты.

    :param transactions: DataFrame с транзакциями, содержащий колонки 'Дата операции', 'Категория' и 'Сумма операции'.
    :param category: Название категории, по которой необходимо получить траты.
    :param date: Опциональная дата в формате 'DD.MM.YYYY HH:MM:SS'. Если не указана, используется текущая дата.
    :return: DataFrame с тратами по заданной категории за последние три месяца.
    """
    # Если дата не указана, берем текущую дату
    if date is None:
        date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    # Преобразуем строку даты в объект datetime
    date = datetime.strptime(date, "%d.%m.%Y %H:%M:%S")

    # Вычисляем дату три месяца назад
    three_months_ago = date - timedelta(days=90)

    # Преобразуем столбец 'Дата операции' в datetime с обработкой ошибок
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
    )

    # Удаляем строки с некорректными датами
    transactions = transactions[transactions["Дата операции"].notna()]

    # Фильтруем транзакции по категории и дате
    filtered_transactions = transactions[
        (transactions["Категория"] == category) & (transactions["Дата операции"] >= three_months_ago)
    ]

    # Возвращаем только нужные столбцы
    return filtered_transactions[["Дата операции", "Категория", "Сумма операции"]]


# Пример использования:
# transactions = fload_excel(path)
#
# date = "22.07.2025 23:59:59"
# category = "Супермаркеты"
# result = spending_by_category(transactions, category)
# print("***************")
# print(f"result = {result}")
