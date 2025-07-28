"""Вспомогательные функции."""

import json
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

from config import PATH_TO_USER_SETTINGS


def greeting() -> str:
    """Функция возвращает приветствие в зависимости от текущего времени/"""
    # Получаем текущее время
    current_time = datetime.now().time()
    # print(f"Текущее время равно: {current_time}")

    # Определяем время для приветствий
    morning_start = datetime.strptime("06:00", "%H:%M").time()
    afternoon_start = datetime.strptime("12:00", "%H:%M").time()
    evening_start = datetime.strptime("16:00", "%H:%M").time()
    night_start = datetime.strptime("23:00", "%H:%M").time()

    # Определяем приветствие на основе текущего времени
    if morning_start <= current_time < afternoon_start:
        day = "Доброе утро!"
        return day
    elif afternoon_start <= current_time < evening_start:
        day = "Добрый день!"
        return day
    elif evening_start <= current_time < night_start:
        day = "Добрый вечер!"
        return day
    else:
        day = "Доброй ночи!"
        return day


def fetch_exchange_rates(url: str):
    """Получает курсы валют из указанного URL."""

    # Загружаем настройки пользователя
    """Загружает настройки пользователя из JSON файла."""
    settings_path = str(PATH_TO_USER_SETTINGS)
    with open(settings_path, "r", encoding="utf-8") as file:
        user_settings = json.load(file)
    user_currencies = user_settings.get("user_currencies", [])

    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Ошибка: {response.status_code}")

    data = response.json()

    if "Valute" not in data:
        print("Нет данных о валютах.")
        return None

    # Словарь для хранения курсов валют
    exchange_rates = {}

    for currency, details in data["Valute"].items():
        # Сохраняем только нужные валюты по их символам
        if details["CharCode"] in user_currencies:
            exchange_rates[details["Name"]] = details["Value"]
            print(f"exchange_rates = {exchange_rates}")
            # Новый кортеж для хранения преобразованных данных
            valuta: tuple = tuple()
            print(f"valuta = {type(valuta)}")
            # Перебираем валютные данные в исходном словаре
            for currency, rate in exchange_rates.items():
                # Преобразуем название валюты в код
                if currency == "Доллар США":
                    currency_code = "USD"
                elif currency == "Евро":
                    currency_code = "EUR"
                else:
                    continue  # Если валюта не распознана, пропускаем

                # Добавляем информацию о валюте и курсе в новый кортеж
                valuta += ({" currency ": currency_code, "rate": rate},)

            # Выводим результат
    if not exchange_rates:
        print("Нет данных о запрашиваемых валютах.")

    # return exchange_rates  # Возвращаем только курсы валют
    return valuta  # Возвращаем только курсы валют


# Загрузка переменных из .env-файла
load_dotenv()
# Получение значения переменной API_KEY из .env-файла
apikey = os.getenv("API_KEY")
# Путь к файлу настроек пользователя
settings_path = Path(__file__).parent.parent / "user_settings.json"
# Загрузка настроек пользователя
with open(settings_path, "r", encoding="utf-8") as file:
    user_set = json.load(file)
symbols = user_set.get("user_stocks", [])
# Определение URL и функции
url = "https://www.alphavantage.co/query"
function = "GLOBAL_QUOTE"


def fetch_stock_rates(url: str, function: str, symbols: list, apikey: str):
    """Получает курсы акций из API для списка символов."""

    stock_data = {}

    for symbol in symbols:
        # Параметры запроса
        params = {"function": function, "symbol": symbol, "apikey": apikey}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            stock_data[symbol] = data  # Сохраняем данные для каждой акции

        stock = tuple()
        # Перебираем акционные данные в исходном словаре
        for symbol, data in stock_data.items():
            # Извлекаем цену акций и преобразуем в float
            price = float(data["Global Quote"]["05. price"])
            # Добавляем информацию о акции в новый кортеж
            stock += ({"stock": symbol, "price": price},)

        else:
            print(f"Ошибка при получении данных для {symbol}: {response.status_code}")

    return stock  # Возвращаем все данные о акциях
