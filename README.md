# Проект курсовой работы.
# Название Проекта

## Содержание

- [Описание](#описание)
- [Требования](#требования)
- [Установка](#установка)
- [Серуктура проекта](#title1)
- [Тестирование](#title2)
- [Лицензия](#title3)

## Описание
  
### Задачи по категориям:  
#### Веб-страницы: 
[Веб-страницы:]().  
Основные функции для генерации JSON-ответов реализуйте в отдельном модуле views.py.  
Данные для анализа и вывода на веб-страницах — это данные с начала месяца, на который выпадает входящая дата,  
по входящую дату.
Если дата — 20.05.2020 , то данные для анализа будут в диапазоне 01.05.2020-20.05.2020.
Валюты и акции для отображения на веб-страницах задаются в отдельном файле пользовательских настроек user_settings.json

Пример:

{  
> "user_currencies": ["USD", "EUR"],  
> "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]  
> 
}  

<span style="color: pink; font-size: 16px;">Как JSON-ответ используется веб-страницей:</span>  
-Веб-страница обычно связана с бэкендом через API. Фронтенд обращается к API бэкенда с запросом на получение данных, на что бэкенд отвечает JSON-ответом. Затем фронтенд подставляет значения из JSON-ответа на веб-страницу, чтобы пользователь мог увидеть их на экране.

-В данном случае бэкенд предоставляет JSON-ответ с данными о расходах за месяц, среднем размере транзакции, сумме кешбэка, топе-3 категорий расходов и топе-3 транзакций. Фронтенд использует этот ответ, чтобы отобразить соответствующие значения на веб-странице.

-Также в данном случае бэкенд может использовать сторонние API для получения текущих цен на валюты и акции S&P500. Фронтенд может использовать эти данные, чтобы отобразить соответствующие значения на веб-странице. 
- Главная  
- События


#### Сервисы:  
- Выгодные категории повышенного кешбэка  
- Инвесткопилка  
- Простой поиск  
- Поиск по телефонным номерам  
- Поиск переводов физическим лицам  
#### Отчеты:  
- Траты по категории  
- Траты по дням недели  
- Траты в рабочий/выходной день  




## Требования

Перед тем, как установить проект, убедитесь, что у вас установлен python = 3.13 или выше.
Также могут понадобиться следующие зависимости, список которых есть в файле *****<span style="color: magenta;">requirements.txt</span>*****:

- poetry-core = ">=2.0.0,<3.0.0"
- requests = "^2.32.3"
- isort = "^6.0.1"

## Установка

### Следуйте этим шагам, чтобы установить проект:

1. Клонируйте репозиторий:
   ```bash
   git clone git@github.com:https://github.com/Donskoff/ScyPro_project
### Создайте и активируйте виртуальное окружение:

python -m venv venv
source venv/bin/activate  # для Unix или MacOS
venv\Scripts\activate  # для Windows
### Установите зависимости:

pip install -r requirements.txt  
<span style="color: grey; font-size: 13px;">(pip freeze > requirements.txt для создания)</span> 
### Для запуска приложения выполните команду:

python src/main.py


## <a id="title1">Серуктура проекта</a>
 



### <p style="margin-left: 1px;"><a style="color: yellow;" id="title1">...\ProjectCours/ </a> 
#### <p style="margin-left: 1px;">├── <a style="color: turquoise;" id="title1">src/</a>
<p style="margin-left: 30px;">├── utils.py</p> 
<p style="margin-left: 30px;">├── main.py</p> 
<p style="margin-left: 30px;">├── views.py.py</p> 
<p style="margin-left: 30px;">├── reports.py</p> 
<p style="margin-left: 30px;">├── services.py</p> 

<p style="margin-left: 1px;">├── <b style="color: turquoise;" id="title1">tests</b>
<p style="margin-left: 30px;">├── test_utils.py</p>  
<p style="margin-left: 30px;">├── test_views.py</p>  
<p style="margin-left: 30px;">├── test_reports.py</p>  
<p style="margin-left: 30px;">├── test_services.py</p>  

<p style="margin-left: 1px;">├── <b style="color: turquoise;" id="title1">user_settings.json</b>
<p style="margin-left: 1px;">├── <b style="color: turquoise;" id="title1">.venv/</b>
<p style="margin-left: 1px;">├── <b style="color: turquoise;" id="title1">.env</b>
<p style="margin-left: 1px;">├── <b style="color: turquoise;" id="title1">.env_template</b>
<p style="margin-left: 1px;">├── <b style="color: turquoise;" id="title1">.git/</b>
<p style="margin-left: 1px;">├── <b style="color: turquoise;" id="title1">.idea/</b>
<p style="margin-left: 1px;">├── <b style="color: turquoise;" id="title1">.flake8</b>
<p style="margin-left: 1px;">├── <b style="color: turquoise;" id="title1">.gitignore</b>
<p style="margin-left: 1px;">├── <b style="color: turquoise;" id="title1">pyproject.toml</b>
<p style="margin-left: 1px;">├── <b style="color: turquoise;" id="title1">poetry.lock</b>
<p style="margin-left: 1px;">└── <b style="color: turquoise;" id="title1">README.md</b>

## <a id="title2">Тестирование</a>

Для тестирования функций проекта используется библиотеки:*****<span style="color: green;">pytest</span>*****.  
Весь тестовый код находится в папке *****<span style="color: green;">tests</span>*****.  
<p style="margin-left: 1px;">├── <b style="color: turquoise;" id="title1">tests</b>
<p style="margin-left: 30px;">├── test_utils.py</p>  
<p style="margin-left: 30px;">├── test_views.py</p>  
<p style="margin-left: 30px;">├── test_reports.py</p>  
<p style="margin-left: 30px;">├── test_services.py</p>   

### Запуск тестов:

Вы можете запускать тесты из командной строки, выполнив следующую команду в корневой директории проекта:  

<p style="margin-left: 1px;"><b style="color: turquoise;" id="title1">./my_prj/ProjectCours</b>

```
pytest 
```  
pytest --cov=src --cov-report=html  
1. git add htmlcov — чтобы добавить папку в отслеживание.
2. git commit -m "Добавлен отчёт покрытия тестами" — чтобы зафиксировать изменения.
3. git push — чтобы отправить изменения в удалённый репозиторий.  
Убедись, что папка htmlcov не указана в файле .gitignore, 
так как это может помешать её добавлению в репозиторий. 
Также проверь, что команда git add htmlcov действительно 
была выполнена в той же директории, где находится папка htmlcov.

## <a id="title3">Лицензия</a>  
Этот проект лицензируется под MIT License. 
> [!NOTE]
> Useful information that users should know, even when skimming content.

> [!TIP]
> Helpful advice for doing things better or more easily.

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

| Command | Description |
| --- | --- |
| git status | List all new or modified files |
| git diff | Show file differences that haven't been staged |

### API  
https://www.cbr-xml-daily.ru/daily_json.js
https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=TI1R7Q1A8M4NO3K
Параметры API  
❚ Обязательно: function
Функция API по вашему выбору.
❚ Обязательно: symbol
Символ выбранного вами глобального тикера. Например: symbol=IBM.
❚ Необязательно: datatype
По умолчанию datatype=json. Строки json и csv принимаются со следующими параметрами: json возвращает  
данные о котировках в формате JSON; csv возвращает данные о котировках в формате CSV (значения, разделенные запятыми).
❚ Обязательно: apikey

  "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]