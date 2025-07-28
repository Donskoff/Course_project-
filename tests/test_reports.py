import json
from unittest.mock import mock_open, patch

import pandas as pd

from src.reports import spending_by_category


def test_report_decorator_writes_to_file():
    """
    Тестирование декоратора report_decorator на корректную запись в файл.

    Проверяет, что декоратор записывает правильные данные в файл JSON.
    """
    # Создаем тестовые данные
    sample_data = pd.DataFrame(
        {"Дата операции": ["07.07.2025 06:13:28"], "Категория": ["Супермаркеты"], "Сумма операции": [-160.89]}
    )
    # Используем mock_open для подмены функции open
    with patch("builtins.open", mock_open()) as mocked_file:
        # Вызываем функцию, обернутую декоратором
        spending_by_category(sample_data, "Супермаркеты")
        # result = spending_by_category(sample_data, "Супермаркеты")
        # Проверяем, что write был вызван
        assert mocked_file().write.call_count > 0  # Убедитесь, что write был вызван хотя бы один раз

        # Получаем все вызовы write
        written_calls = mocked_file().write.call_args_list

        # Получаем строку, которая была записана
        written_content = "".join(call[0][0] for call in written_calls)

        # Проверяем, что содержимое, записанное в файл, соответствует ожидаемому
        expected_content = json.dumps(
            [{"Дата операции": "07.07.2025 06:13:28", "Категория": "Супермаркеты", "Сумма операции": -160.89}],
            ensure_ascii=False,
            indent=4,
        )

        assert written_content.strip() == expected_content.strip()
