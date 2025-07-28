from pathlib import Path
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Определение путей
PATH = Path(__file__).parent
PATH_TO_OPERATIONS = PATH / "data" / "operations.xlsx"
PATH_TO_USER_SETTINGS = PATH / "user_settings.json"
PATH_TO_LOGGER = PATH / "logs"
PATH_TO_GREETING = PATH / "src" / "utils.py"

# Получение API ключа из переменных окружения
API_KEY = os.getenv("API_KEY")

# from pathlib import Path
#
#
# PATH = Path(__file__).parent
# PATH_TO_OPERATIONS = PATH / "data" / "operations.xlsx"
# PATH_TO_USER_SETTINGS = PATH / "user_settings.json"
# PATH_TO_LOGGER = PATH / "logs"
# PATH_TO_GREETING = PATH / "src" / "utils.py"