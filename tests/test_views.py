"""Тесты модуля views.py."""

import json
import unittest
from unittest.mock import patch

import pandas as pd

from src.views import main


class TestMainFunction(unittest.TestCase):

    @patch("src.views.pd.read_excel")
    @patch("src.views.filter_transactions")
    @patch("src.views.summarize_card_data")
    @patch("src.views.get_top_transactions")
    @patch("src.views.greeting")
    @patch("src.views.fetch_exchange_rates")
    @patch("src.views.load_dotenv")
    @patch("src.views.os.getenv")
    @patch("src.views.load_user_settings")
    @patch("src.views.fetch_stock_rates")
    def test_main(
        self,
        mock_fetch_stock_rates,
        mock_load_user_settings,
        mock_getenv,
        mock_load_dotenv,
        mock_fetch_exchange_rates,
        mock_greeting,
        mock_get_top_transactions,
        mock_summarize_card_data,
        mock_filter_transactions,
        mock_read_excel,
    ):
        # Настройка мока для чтения Excel файла
        mock_read_excel.return_value = pd.DataFrame(
            {
                "Дата операции": pd.to_datetime(["2023-10-01", "2023-10-02", "2023-10-03"]),
                "Сумма платежа": [100, 200, 300],
                "Номер карты": ["1234567812345678", "8765432187654321", "1234567812345678"],
                "Категория": ["Еда", "Транспорт", "Развлечения"],
                "Описание": ["Покупка 1", "Покупка 2", "Покупка 3"],
            }
        )

        # Настройка мока для фильтрации транзакций
        mock_filter_transactions.return_value = mock_read_excel.return_value

        # Настройка мока для суммирования данных по картам
        mock_summarize_card_data.return_value = [{"last_digits": "5678", "total_spent": 400, "cashback": 4.0}]

        # Настройка мока для получения топ транзакций
        mock_get_top_transactions.return_value = [
            {"date": "01.10.2023", "amount": 300, "category": "Развлечения", "description": "Покупка 3"},
            {"date": "02.10.2023", "amount": 200, "category": "Транспорт", "description": "Покупка 2"},
            {"date": "03.10.2023", "amount": 100, "category": "Еда", "description": "Покупка 1"},
        ]

        # Настройка мока для приветствия
        mock_greeting.return_value = "Добро пожаловать!"

        # Настройка мока для курсов валют
        mock_fetch_exchange_rates.return_value = {"USD": 73.5, "EUR": 85.0}

        # Настройка мока для получения API_KEY
        mock_getenv.return_value = "dummy_api_key"

        # Настройка мока для загрузки пользовательских настроек
        mock_load_user_settings.return_value = {"user_stocks": ["AAPL", "GOOGL"]}

        # Настройка мока для получения курсов акций
        mock_fetch_stock_rates.return_value = {"AAPL": {"price": 150.0}, "GOOGL": {"price": 2800.0}}

        # Вызов тестируемой функции
        result = main("2023-10-03")

        # Проверка результата
        expected_response = {
            "greeting": "Добро пожаловать!",
            "cards": [{"last_digits": "5678", "total_spent": 400, "cashback": 4.0}],
            "top_transactions": [
                {"date": "01.10.2023", "amount": 300, "category": "Развлечения", "description": "Покупка 3"},
                {"date": "02.10.2023", "amount": 200, "category": "Транспорт", "description": "Покупка 2"},
                {"date": "03.10.2023", "amount": 100, "category": "Еда", "description": "Покупка 1"},
            ],
            "currency_rates": {"USD": 73.5, "EUR": 85.0},
            "stock_prices": {"AAPL": {"price": 150.0}, "GOOGL": {"price": 2800.0}},
        }

        self.assertEqual(json.loads(result), expected_response)


if __name__ == "__main__":
    unittest.main()
