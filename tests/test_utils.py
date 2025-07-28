import unittest
from datetime import datetime
from unittest.mock import mock_open, patch

from src.utils import fetch_exchange_rates, fetch_stock_rates, greeting


class TestGreeting(unittest.TestCase):

    @patch("src.utils.datetime")
    def test_evening_greeting(self, mock_datetime):
        mock_now = datetime(2023, 1, 1, 22, 0, 0)
        mock_datetime.now.return_value = mock_now

        mock_datetime.strptime.side_effect = lambda *args, **kwargs: datetime.strptime(*args, **kwargs)

        result = greeting()
        self.assertEqual(result, "Добрый вечер!")

    @patch("src.utils.datetime")
    def test_afternoon_greeting(self, mock_datetime):
        mock_now = datetime(2023, 1, 1, 13, 0, 0)
        mock_datetime.now.return_value = mock_now

        mock_datetime.strptime.side_effect = lambda *args, **kwargs: datetime.strptime(*args, **kwargs)

        result = greeting()
        self.assertEqual(result, "Добрый день!")

    @patch("src.utils.datetime")
    def test_morning_greeting(self, mock_datetime):
        mock_now = datetime(2023, 1, 1, 8, 0, 0)
        mock_datetime.now.return_value = mock_now

        mock_datetime.strptime.side_effect = lambda *args, **kwargs: datetime.strptime(*args, **kwargs)

        result = greeting()
        self.assertEqual(result, "Доброе утро!")

    @patch("src.utils.datetime")
    def test_night_greeting(self, mock_datetime):
        mock_now = datetime(2023, 1, 1, 23, 30, 0)
        mock_datetime.now.return_value = mock_now

        mock_datetime.strptime.side_effect = lambda *args, **kwargs: datetime.strptime(*args, **kwargs)

        result = greeting()
        self.assertEqual(result, "Доброй ночи!")


class TestFetchExchangeRates(unittest.TestCase):

    @patch("src.utils.requests.get")
    @patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
    def test_fetch_exchange_rates_success(self, mock_file, mock_requests_get):
        # Настройка мока для успешного ответа от API
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {
            "Valute": {
                "USD": {"CharCode": "USD", "Name": "Доллар США", "Value": 75.0},
                "EUR": {"CharCode": "EUR", "Name": "Евро", "Value": 90.0},
                "RUB": {"CharCode": "RUB", "Name": "Российский рубль", "Value": 1.0},
            }
        }

        # Вызов функции
        result = fetch_exchange_rates("http://example.com/api")

        # Проверка результата
        expected_result = (
            {" currency ": "USD", "rate": 75.0},
            {" currency ": "EUR", "rate": 90.0},
        )
        self.assertEqual(result, expected_result)

    @patch("src.utils.requests.get")
    @patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
    def test_fetch_exchange_rates_no_data(self, mock_file, mock_requests_get):
        # Настройка мока для ответа без данных о валютах
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {}

        # Вызов функции
        result = fetch_exchange_rates("http://example.com/api")

        # Проверка результата
        self.assertIsNone(result)

    @patch("src.utils.requests.get")
    @patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
    def test_fetch_exchange_rates_invalid_response(self, mock_file, mock_requests_get):
        # Настройка мока для ошибки при запросе
        mock_requests_get.return_value.status_code = 404

        # Проверка на выброс исключения
        with self.assertRaises(ValueError) as context:
            fetch_exchange_rates("http://example.com/api")
        self.assertEqual(str(context.exception), "Ошибка: 404")


class TestFetchStockRates(unittest.TestCase):

    @patch("src.utils.requests.get")
    @patch(
        "builtins.open", new_callable=mock_open, read_data='{"user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}'
    )
    def test_fetch_stock_rates_success(self, mock_file, mock_requests_get):
        # Настройка мока для успешного ответа от API
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {
            "Global Quote": {"01. symbol": "AAPL", "05. price": "150.00"}
        }

        # Вызов функции
        result = fetch_stock_rates("http://example.com/api", "GLOBAL_QUOTE", ["AAPL"], "dummy_api_key")

        # Проверка результата
        expected_result = ({"stock": "AAPL", "price": 150.00},)
        self.assertEqual(result, expected_result)

    @patch("src.utils.requests.get")
    @patch("builtins.open", new_callable=mock_open, read_data='{"user_stocks": ["AAPL", "AMZN"]}')
    def test_fetch_stock_rates_multiple_symbols(self, mock_file, mock_requests_get):
        # Настройка мока для успешного ответа от API для нескольких акций
        mock_requests_get.side_effect = [
            unittest.mock.Mock(
                status_code=200, json=lambda: {"Global Quote": {"01. symbol": "AAPL", "05. price": "150.00"}}
            ),
            unittest.mock.Mock(
                status_code=200, json=lambda: {"Global Quote": {"01. symbol": "AMZN", "05. price": "3000.00"}}
            ),
        ]

        # Вызов функции
        result = fetch_stock_rates("http://example.com/api", "GLOBAL_QUOTE", ["AAPL", "AMZN"], "dummy_api_key")

        # Проверка результата
        expected_result = (
            {"stock": "AAPL", "price": 150.00},
            {"stock": "AMZN", "price": 3000.00},
        )
        self.assertEqual(result, expected_result)

    @patch("src.utils.requests.get")
    @patch("builtins.open", new_callable=mock_open, read_data='{"user_stocks": ["AAPL"]}')
    def test_fetch_stock_rates_invalid_response(self, mock_file, mock_requests_get):
        # Настройка мока для ответа с ошибкой
        mock_requests_get.return_value.status_code = 404

        # Вызов функции
        result = fetch_stock_rates("http://example.com/api", "GLOBAL_QUOTE", ["AAPL"], "dummy_api_key")

        # Проверка результата
        self.assertEqual(result, ())


if __name__ == "__main__":
    unittest.main()
