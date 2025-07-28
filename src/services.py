import json
import logging
from typing import Dict, List

import pandas as pd

# from config import PATH_TO_OPERATIONS

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def search_transactions(file_path: str) -> str:
    """
    Ищет транзакции, относящиеся к переводам физическим лицам.

    :param file_path: Путь к файлу Excel с данными о транзакциях.
    :return: JSON-строка со всеми транзакциями, относящимися к переводам физическим лицам.
    """
    try:
        # Чтение данных из файла Excel
        df = pd.read_excel(file_path)

        # Фильтрация транзакций по категории "Переводы"
        transfers = df[df["Категория"] == "Переводы"]

        # Определение шаблона для поиска имени и первой буквы фамилии
        pattern = r"^[А-ЯЁ][а-яё]+\s+[А-ЯЁ]\."

        # Фильтрация по описанию, используя регулярное выражение
        filtered_transfers = transfers[transfers["Описание"].str.contains(pattern, regex=True)]

        # Преобразование отфильтрованных данных в словарь
        transactions_list: List[Dict] = filtered_transfers.to_dict(orient="records")

        # Логирование количества найденных транзакций
        logging.info(f"Найдено {len(transactions_list)} транзакций.")

        # Преобразование списка транзакций в JSON
        return json.dumps(transactions_list, ensure_ascii=False)

    except Exception as e:
        logging.error(f"Ошибка при поиске транзакций: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# Пример использования
# file_path = PATH_TO_OPERATIONS
# print(search_transactions(file_path))
# print(type(search_transactions(file_path)))
