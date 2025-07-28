"""Главная функция."""

import json
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from config import PATH_TO_OPERATIONS
from src.utils import fetch_exchange_rates, fetch_stock_rates, greeting


def load_user_settings():
    settings_path = Path(__file__).parent.parent / "user_settings.json"
    with open(settings_path, "r", encoding="utf-8") as file:
        return json.load(file)


def filter_transactions(excel_data, date_cutoff):
    start_of_month = date_cutoff.replace(day=1)
    filtered_data = excel_data[
        (excel_data["Дата операции"] >= start_of_month) & (excel_data["Дата операции"] <= date_cutoff)
    ]
    return filtered_data


def summarize_card_data(filtered_data):
    card_summary = (
        filtered_data.groupby("Номер карты")
        .agg(
            total_spent=("Сумма платежа", "sum"),
            cashback=("Сумма платежа", lambda x: x.sum() * 0.01),
        )
        .reset_index()
    )
    card_summary["last_digits"] = card_summary["Номер карты"].astype(str).str[-4:]
    return card_summary[["last_digits", "total_spent", "cashback"]].to_dict(orient="records")


def get_top_transactions(filtered_data):
    top_transactions = filtered_data.nlargest(5, "Сумма платежа")[
        ["Дата операции", "Сумма платежа", "Категория", "Описание"]
    ]
    top_transactions["Дата операции"] = top_transactions["Дата операции"].dt.strftime("%d.%m.%Y")
    return top_transactions.rename(
        columns={
            "Дата операции": "date",
            "Сумма платежа": "amount",
            "Категория": "category",
            "Описание": "description",
        }
    ).to_dict(orient="records")


def main(date):
    excel_data = pd.read_excel(PATH_TO_OPERATIONS)
    date_cutoff = pd.to_datetime(date)

    excel_data["Дата операции"] = pd.to_datetime(
        excel_data["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce", dayfirst=True
    )

    filtered_data = filter_transactions(excel_data, date_cutoff)
    cards = summarize_card_data(filtered_data)
    top_transactions = get_top_transactions(filtered_data)

    day = greeting()
    exchange_rates = fetch_exchange_rates("https://www.cbr-xml-daily.ru/daily_json.js")

    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    user_set = load_user_settings()
    user_stocks = user_set.get("user_stocks", [])
    stock = fetch_stock_rates("https://www.alphavantage.co/query", "GLOBAL_QUOTE", user_stocks, API_KEY)

    response = {
        "greeting": day,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": exchange_rates,
        "stock_prices": stock,
    }

    return json.dumps(response, ensure_ascii=False, indent=2)
