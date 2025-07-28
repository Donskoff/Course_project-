"""Главная функция."""

import json
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from config import PATH_TO_OPERATIONS
from src.utils import fetch_exchange_rates, fetch_stock_rates, greeting


def filter_excel(date):
    # Считываем данные из файла Excel
    excel_data = pd.read_excel(PATH_TO_OPERATIONS)
    # Преобразуем строку date в объект datetime
    date_cutoff = pd.to_datetime(date)
    # Определяем начало месяца
    start_of_month = date_cutoff.replace(day=1, hour=0, minute=0, second=0)
    # Преобразуем колонку "Дата операции" в datetime
    excel_data["Дата операции"] = pd.to_datetime(
        excel_data["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
    )
    # Фильтруем данные по дате
    filtered_data = excel_data[
        (excel_data["Дата операции"] >= start_of_month) & (excel_data["Дата операции"] <= date_cutoff)
    ]
    # Получаем последние 4 цифры номера карты и считаем сумму платежей и кэшбэк
    card_summary = (
        filtered_data.groupby("Номер карты")
        .agg(
            total_spent=("Сумма платежа", "sum"),
            cashback=("Сумма платежа", lambda x: x.sum() * 0.01),
        )
        .reset_index()
    )
    # Добавляем последние 4 цифры карты
    card_summary["last_digits"] = card_summary["Номер карты"].astype(str).str[-4:]

    cards = card_summary[["last_digits", "total_spent", "cashback"]].to_dict(orient="records")

    # Получаем топ-5 транзакций по сумме платежа
    top_transactions = filtered_data.nlargest(5, "Сумма платежа")[
        ["Дата операции", "Сумма платежа", "Категория", "Описание"]
    ]
    top_transactions["Дата операции"] = top_transactions["Дата операции"].dt.strftime("%d.%m.%Y")  # Форматируем дату
    top_transactions = top_transactions.rename(
        columns={
            "Дата операции": "date",
            "Сумма платежа": "amount",
            "Категория": "category",
            "Описание": "description",
        }
    ).to_dict(orient="records")

    day = greeting()

    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    exchange_rates = fetch_exchange_rates(url)

    # Загрузка переменных из .env-файла
    load_dotenv()
    # Получение значения переменной API_KEY из .env-файла
    API_KEY = os.getenv("API_KEY")
    # Путь к файлу настроек пользователя
    settings_path = Path(__file__).parent.parent / "user_settings.json"
    # Загрузка настроек пользователя
    with open(settings_path, "r", encoding="utf-8") as file:
        user_set = json.load(file)
    user_stocks = user_set.get("user_stocks", [])
    # Определение URL и функции
    url = "https://www.alphavantage.co/query"
    function = "GLOBAL_QUOTE"

    # Вызов функции для получения курсов акций
    stock = fetch_stock_rates(url, function, user_stocks, API_KEY)

    # Формируем ответ в формате JSON
    response = {
        "greeting": day,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": exchange_rates,
        "stock_prices": (stock),
    }

    # Возвращаем ответ в формате JSON
    return json.dumps(response, ensure_ascii=False, indent=2)
