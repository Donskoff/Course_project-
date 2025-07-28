import json

from config import PATH_TO_OPERATIONS
from src.services import search_transactions


def test_search_transactions():
    # Укажите путь к тестовому файлу Excel
    result = search_transactions(PATH_TO_OPERATIONS)

    # Проверка, что результат является строкой
    assert isinstance(result, str)

    # Преобразование результата из JSON обратно в Python-объект
    transactions = json.loads(result)

    # Проверка, что это список
    assert isinstance(transactions, list)
