from my_project.df_readers import get_transactions_csv

# Homework-Widget-Project

Учебный проект: обработка банковских транзакций для виджета.

## Что делает проект

Программа помогает подготовить банковские операции для показа пользователю:
* оставить только выполненные операции;
* расставить их по дате;
* спрятать номера карт и счетов;
* показать дату в привычном формате (ДД.ММ.ГГГГ);
* сортировать, фильтровать по ключам и показывать отчёты выполненных операций;
* вести лог-журнал операций в файле;
* читать транзакции из JSON-файла и считать итоговую сумму в рублях с конвертацией валют через API;
* читать транзакции из файлов XLSX, CSV и выводить в JSON формате
---

## Как подключить функции (самое важное для запуска)

Чтобы использовать функции в своём скрипте, нужно сначала их «подключить» через `import`. Вот, например, откуда брать каждую функцию:


```python
from src.my_project.processing import filter_by_state, sort_by_date
from src.my_project.masks import get_mask_card_number, get_mask_account
from src.my_project.widget import mask_account_card, get_date
from src.my_project.generators import filter_by_currency, transaction_descriptions, card_number_generator
from src.my_project.decorators import log
from src.my_project.utils import convert_json_to_python
from src.my_project.external_api import amound_by_transactions
from src.my_project.project_root_Path_finder import get_project_root
from src.my_project.df_readers import get_transactions_xlsx
from src.my_project.df_readers import get_transactions_csv
```
После этих строк можно спокойно вызывать filter_by_state, get_date и остальные — Python их увидит.

---

# `— filter_by_state —`

Фильтрует список операций по статусам 'EXECUTED' или 'CANCELED'.
По умолчанию, берёт список операций и возвращает те, у которых статус EXECUTED (по умолчанию).

При вызове функции можете поменять режим на 'CANCELED' -

```python
filter_by_state(records, state_mode="CANCELED")
```
Пример:

```python
operations = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2023-10-01T10:00:00'},
    {'id': 2, 'state': 'CANCELED', 'date': '2023-10-02T11:00:00'},
    {'id': 3, 'state': 'EXECUTED', 'date': '2023-10-03T12:00:00'}
]

result = filter_by_state(operations, state_mode="EXECUTED")
```
Что получится:

```python
[
    {'id': 1, 'state': 'EXECUTED', 'date': '2023-10-01T10:00:00'},
    {'id': 3, 'state': 'EXECUTED', 'date': '2023-10-03T12:00:00'}
]
```
---

#  `—sort_by_date—`

Функция сортирует операции по дате: (по умолчанию) новые будут в начале списка.

Пример:

```python
ops = [
    {'id': 1, 'date': '2023-10-03T12:00:00'},
    {'id': 2, 'date': '2023-10-01T10:00:00'},
    {'id': 3, 'date': '2023-10-02T11:00:00'}
]

sorted_ops = sort_by_date(ops, descending=True)
```
Что получится:

```python
[
    {'id': 1, 'date': '2023-10-03T12:00:00'},
    {'id': 3, 'date': '2023-10-02T11:00:00'},
    {'id': 2, 'date': '2023-10-01T10:00:00'}
]
```
**Если у какой-то операции нет даты или она записана странно, эта операция окажется в конце — программа не сломается.**

---
# `— get_mask_card_number —`
Функция маскирует номер карты (16 цифр), оставляя начало и конец видимыми, а середину прячет за звёздочками.

Пример:

```python
card = "7000792289606361"
masked = get_mask_card_number(card)
```
Что получится:

```python
"7000 79** **** 6361"
```
Если передать что-то не то (не 16 цифр, буквы и т.п.), функция сообщит об ошибке — *это защита от неправильных данных.*

---

# `— get_mask_account —`

Функция маскирует номер счёта (20 цифр) и оставляет только две звёздочки и последние 4 цифры.

Пример:

```python
account = "73654108430135874305"
masked = get_mask_account(account)
```
Что получится:

```python
"**4305"
```

# `— mask_account_card —`

Универсальный маскировщик, симбиоз функций - get_mask_account и get_mask_card_number

Функция сама понимает, карта это или счёт, и прячет номер правильно.

На вход задаётся строка с описанием банковского инструмента и номером.

Пример:

```python
data_1 = "Счет 73654108430135874305"
data_2 = "Visa Platinum 7000792289606361"

r1 = mask_account_card(data_1)
r2 = mask_account_card(data_2)
```
Что получится:

```python
"Счет **4305"                        # для счёта
"Visa Platinum 7000 79** **** 6361"  # для карты
```
---

# `— get_date —`

Приводит дату к формату ДД.ММ.ГГГГ
Функция превращает длинную дату из базы в простой формат, который удобно читать.

Пример:

```python
date_str = "2023-10-05T14:30:00.123456"
formatted = get_date(date_str)
```
Что получится:

```python
"05.10.2023"
```
---

# `— filter_by_currency —`

Возвращает итератор (генератор) по транзакциям, где код валюты совпадает с currency_code.

Пример:

```python
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    },
    {
        "id": 123456789,
        "state": "EXECUTED",
        "date": "2020-01-01T12:00:00.000000",
        "operationAmount": {
            "amount": "5000.00",
            "currency": {
                "name": "RUB",
                "code": "RUB"
            }
        },
        "description": "Перевод в рублях",
        "from": "Счет 11112222333344445555",
        "to": "Счет 66667777888899990000"
    }
]

usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))
```

Что получится:

```python
{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572', 'operationAmount': {'amount': '9824.07', 'currency': {'name': 'USD', 'code': 'USD'}}, 'description': 'Перевод организации', 'from': 'Счет 75106830613657916952', 'to': 'Счет 11776614605963066702'}
{'id': 142264268, 'state': 'EXECUTED', 'date': '2019-04-04T23:20:05.206878', 'operationAmount': {'amount': '79114.93', 'currency': {'name': 'USD', 'code': 'USD'}}, 'description': 'Перевод со счета на счет', 'from': 'Счет 19708645243227258542', 'to': 'Счет 75651667383060284188'}
```
---

# `— transaction_descriptions —`

Генератор, возвращающий описание каждой операции по очереди.

Пример:

```Python
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {
            "amount": "9824.07",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702"
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {
            "amount": "79114.93",
            "currency": {"name": "USD", "code": "USD"}
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188"
    },
    {
        "id": 123456789,
        "state": "EXECUTED",
        "date": "2020-01-01T12:00:00.000000",
        "operationAmount": {
            "amount": "5000.00",
            "currency": {"name": "RUB", "code": "RUB"}
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 11112222333344445555",
        "to": "Счет 66667777888899990000"
    },
    {
        "id": 987654321,
        "state": "EXECUTED",
        "date": "2020-02-01T12:00:00.000000",
        "operationAmount": {
            "amount": "3000.00",
            "currency": {"name": "RUB", "code": "RUB"}
        },
        "description": "Перевод с карты на карту",
        "from": "Карта 1111222233334444",
        "to": "Карта 5555666677778888"
    },
    {
        "id": 112233445,
        "state": "EXECUTED",
        "date": "2020-03-01T12:00:00.000000",
        "operationAmount": {
            "amount": "4000.00",
            "currency": {"name": "RUB", "code": "RUB"}
        },
        "description": "Перевод организации",
        "from": "Счет 22223333444455556666",
        "to": "Счет 77778888999900001111"
    }
]


descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))
```

Что получится:

```Python
Перевод организации
Перевод со счета на счет
Перевод со счета на счет
Перевод с карты на карту
Перевод организации
```
---

# `— card_number_generator —`

Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

Пример:

запускаем так >>>

```python
for card_number in card_number_generator(1, 5):
    print(card_number)
```
Что получится:

```text
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
0000 0000 0000 0004
0000 0000 0000 0005
```
---

# `— log —`

Функция-декоратор, выполняет ведение записей всех событий результатов работы декорируемой функции в файл или в консоль. И обрабатывает все выпадающие исключения.

Пример:

```python
    @log(filename="LOG.txt")  # @log() - режим вывода в консоль
    def add_iti_ons(a: int|float, b: int|float) -> int|float|str:
        return f"ОТВЕТ: {a / b}"

    result_fin = add_iti_ons(10, 5)
    print(result_fin)
```

Что получится:

в консоли >>>

```python
'add_iti_ons' started
'add_iti_ons' Ok
ОТВЕТ: 2.0
```

Запись в лог-файле LOG.txt >>>

```python
'add_iti_ons' started
'add_iti_ons' Ok
```

Пример с возникшим исключением:

```python
    @log(filename="LOG.txt")  # @log() - режим вывода в консоль
    def add_iti_ons(a: int|float, b: int|float) -> int|float|str:
        return f"ОТВЕТ: {a / b}"

    result_fin = add_iti_ons(10, 0)
    print(result_fin)
```

Что получится:

вывод в консоль >>>

```python
'add_iti_ons' started
'add_iti_ons' error: division by zero. Inputs: (10, 0), {}
ZeroDivisionError: division by zero
```
Запись в лог-файле LOG.txt >>>

```python
'add_iti_ons' started
'add_iti_ons' error: division by zero. Inputs: (10, 0), {}
```
---

# `— get_project_root —`

Функция находит корневую папку проекта и возвращает путь к ней как объект Path.

Используется другими модулями для построения путей к файлам с данными (например, JSON-файлам в папке data/).

Не зависит от того, откуда запущен скрипт — всегда находит корень по расположению файла.

Пример:

```python
from my_project.project_root_Path_finder import get_project_root

root = get_project_root()
print(root)
```

Что получится: 

-> получение директории корня проекта на примере моей структуры проекта ->

```python
C:\Users\Dindus\PycharmProjects\my-project
```
Используется внутри convert_json_to_python для построения пути:

```python
import json

from my_project.project_root_Path_finder import get_project_root


def convert_json_to_python(filename: str) -> list[dict]:
    """Принимает имя JSON файла и возвращает содержимое, преобразованное в
    Python объект — список словарей"""

    # 1. Прокладываем путь к JSON файлу с помощью импортированной функции.
    root = get_project_root()  # Функция поиска корня проекта.
    file_path = root / "data" / filename  # Путь от корня проекта к файлу JSON

    # 2. Открываем и читаем JSON файл, обрабатываем возможные исключения.
    try:
        with open(file_path, encoding="utf-8") as f:
            try:
                result = json.load(f)  # используем load, так как читаем из файла
            except json.JSONDecodeError:
                print("Ошибка декодирования файла")
                return []
    except FileNotFoundError:
        print("Файл не найден")
        return []

    return result

```
---

# `— convert_json_to_python —`

Читает JSON-файл из папки data/ и возвращает содержимое как список словарей.

Путь к файлу строится автоматически от корня проекта через get_project_root().

Если файл не найден — возвращает пустой список [] (не ломает программу).

Если JSON повреждён — тоже возвращает [].

Пример:

```python
from my_project.utils import convert_json_to_python

data = convert_json_to_python("operations.json")
print(data)
```

Что получится:

```python
[
    {"id": 1, "operationAmount": {"amount": "1000.0", "currency": {"code": "RUB"}}},
    {"id": 2, "operationAmount": {"amount": "10.0", "currency": {"code": "USD"}}},
    ...
]
```
Если файл не существует:

```python
data = convert_json_to_python("nonexistent.json")
print(data)
```

Что получится:

```python
[]
```
---

# `— amound_by_transactions —`

Читает JSON-файл с транзакциями через convert_json_to_python, суммирует суммы в рублях и конвертирует USD и EUR в RUB через внешний API (apilayer.com).

Возвращает итоговую сумму в рублях как float (с округлением до 2 знаков).

Для работы нужен API_KEY в переменных окружения (файл .env).

Если API недоступен — выбрасывает RuntimeError с описанием ошибки.

Если API_KEY не найден — выбрасывает ValueError.

Пример:

```python
from my_project.external_api import amound_by_transactions

total = amound_by_transactions("operations.json")
print(total)
```

Что получится:

```python
2406.0
```

Транзакции в файле могут содержать RUB, USD и EUR — функция сама определит валюту по полю *operationAmount.currency.code* и конвертирует через API.

Если сумма в иностранной валюте равна `0` — то API не вызывается (экономия запросов).
---
---

# `- get_transactions_csv -` 

Читает файл форматы CSV и выводит его содержимое в виде списка словарей.

+ Указать нужно только название файла при вызове функции, она сама находит к нему путь (в пределах вашего проекта)

Пример запуска:
```python
result = get_transactions_csv('transactions.csv')
print(result)
```
---
# `- get_transactions_xlsx -`

Читает файл форматы XLSX и выводит его содержимое в виде списка словарей.

+ Указать нужно только название файла при вызове функции, она сама находит к нему путь (в пределах вашего проекта)

Пример запуска:

```python
result = get_transactions_xlsx('transactions.csv')
print(result)
```
---

## ~ Как использовать функции вместе ~

Сначала подключаем функции - импортируем (блок в начале текста этого файла), потом применяем их по очереди:

* сначала отобрать нужные операции,
* потом отсортировать,
* потом спрятать номера и привести даты к нужному виду.

`Это помогает подготовить данные для вывода в виджете.`
   
---
---
## ~ Как запустить проект (на Windows, в PowerShell) ~

Клонируем проект:

PowerShell

```text
git clone https://github.com/feniball79-rgb/Homework-Widget-Project.git
cd Homework-Widget-Project
```
Ставим зависимости:

PowerShell

```text
poetry install
```
Проверяем код (чтобы всё было аккуратно):

PowerShell

```text
poetry run black src
poetry run flake8 src
poetry run mypy src
```

Все команды делай через 
-***poetry run***-, чтобы использовались нужные библиотеки.

---

# ~ Структура папок ~

```python
├my-project/
├ htmlcov                    # результаты тестирований функций
├──src/
├    └─ my_project/
├        ├── processing.py             # filter_by_state, sort_by_date
├        ├── masks.py                  # get_mask_card_number, get_mask_account
├        ├── widget.py                 # mask_account_card, get_date
├        ├── generators.py             # filter_by_currency, transaction_descriptions, card_number_generator
├        ├── decorators.py             # log
├        ├── utils.py                  # convert_json_to_python
├        ├── external_api.py           # amound_by_transactions
├        └── project_root_Path_finder.py # get_project_root
└──tests/
     ├── test_filter_by_state.py
     ├── test_generators.py
     ├── test_get_date.py
     ├── test_get_mask_account.py
     ├── test_get_mask_card_number.py
     ├── test_mask_account_card.py
     ├── test_sort_by_date.py
     ├── test_utils.py
     ├── test_external_api.py
     └── test_log.py
.coverage
.flake8      
.gitignore
poetry.lock
pyproject.toml
README.md
```
---

# - TESTS -
 
##  Покрытие тестами

---
## ***-filter_by_state-***

+ проверка фильтрации по статусу, 
+ обработка неверных значений и пустого списка.
---
## ***-sort_by_date-***

+ сортировка по дате, обработка битых и отсутствующих дат, 
+ валидация типа входных данных.
---
## ***-mask_account_card-***

+ авто-маскировка номера карты или счёта, 
+ контроль ввода данных правильного формата и длины, 
+ защита от инвалидных и пустых вводов.
---

## ***-get_date-***

+ работа функции, 
+ защита от пустых и инвалидных вводов.
---

## Модуль маскирования ***-masks-*** с функциями:

  -*`get_mask_card_number`*

 -*`get_mask_account`*

+ тесты на корректное маскирование номеров счетов и карт, 
+ обработка крайних случаев (пустой ввод, короткие строки, буквы, пробелы).
---

## Модуль ***-generators-*** с функциями:

-***`filter_by_currency`***

+ фильтрации банковских транзакций по кодам валют

+ тесты на правильную фильтрацию

+ что генератор — это итератор, а не список

+ обработку отсутствия значения кодов валют

+ обработку пустого значения

+ обработку исключения StopIteration
---

***`-transaction_descriptions`***

возвращающий описание каждой операции по очереди

+ тесты на все описания адресатов \ отправителей транзакций

+ отсутствие описания адресата \ отправителя

+ пустое значение в вызове функции
--- 

-***`card_number_generator`***

Генератор номеров банковских карт

+ тест на слишком большой номер и количество номеров будет ограничено
---

## ***-log-***

Записывает логи в файл | консоль, и обрабатывает исключения(ошибки)

+ тесты на работоспособность декорируемой функции.
+ тест на создание лог-файла в директории,
+ тесты на записи логов в файл или в консоль,
+ тесты на перехват и обработку всех выпадающих исключений,
+ тест на запись логов исключений в файл
+ тест на сохранение имени функции через @wraps
---

## Модуль ***-utils-*** с функцией:

-***`convert_json_to_python`***

Чтение JSON-файла и преобразование в Python-объект (список словарей)

+ тест на успешное чтение корректного JSON-файла (мок open через mock_open)

+ тест на обработку отсутствующего файла (возвращает [])

+ тест на обработку невалидного JSON (возвращает [])
---


## ***`Модуль -external_api- с функцией:`***
amound_by_transactions
Суммирование транзакций с конвертацией валют через API

+ тест на успешную конвертацию USD и EUR через API (мок requests.get с side_effect)

+ тест на только рубли — API не вызывается (assert_not_called)

+ тест на ошибку API (статус 401) — выбрасывается RuntimeError

+ тест на нулевую сумму в иностранной валюте — API не вызывается
---

## ***-convert_json_to_python-***
+ правильно реализует __enter__/__exit__ и read()
---

## Модуль ***-project_root_Path_finder-*** с функцией:


Поиск корневой папки проекта

### **-`get_project_root`-**

полностью покрыт тестами: 
+ поиск маркера,
+ Fallback на корень ФС, 
+ работа с разной глубиной вложенности, 
+ поиск ближайшего pyproject.toml и проверка типа возвращаемого объекта.
+ тест на корректное возвращение объекта Path

+ проверка, что возвращаемый путь существует на диске

+ проверка, что путь указывает на корень проекта (содержит pyproject.toml или src/)
---
    
---

## `Общее покрытие кода тестами: 86%.`
