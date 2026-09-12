# Homework-Widget-Project

Учебный проект: обработка банковских транзакций для виджета.

## Что делает проект

Программа помогает подготовить банковские операции для показа пользователю:
* оставить только выполненные операции;
* расставить их по дате;
* спрятать номера карт и счетов;
* показать дату в привычном формате (ДД.ММ.ГГГГ).

---

## Как подключить функции (самое важное для запуска)

Чтобы использовать функции в своём скрипте, нужно сначала их «подключить» через `import`. Вот откуда брать каждую функцию:


```python
from src.my_project.processing import filter_by_state, sort_by_date
from src.my_project.masks import get_mask_card_number, get_mask_account
from src.my_project.widget import mask_account_card, get_date
````
После этих строк можно спокойно вызывать `filter_by_state`, `get_date` и остальные — Python их увидит.

________
## — `filter_by_state` — 

+ Фильтрует список операций по статусам 'EXECUTED' или 'CANCELED'.

По умолчанию, берёт список операций и возвращает те, у которых статус EXECUTED (по умолчанию).

При вызове функции можете поменять режим на 'CANCELED' - 
````python
filter_by_state(records, state_mode="CANCELED")
````
Пример:
````python
operations = [
    {'id': 1, 'state': 'EXECUTED', 'date': '2023-10-01T10:00:00'},
    {'id': 2, 'state': 'CANCELED', 'date': '2023-10-02T11:00:00'},
    {'id': 3, 'state': 'EXECUTED', 'date': '2023-10-03T12:00:00'}
]

result = filter_by_state(operations, state_mode="EXECUTED")
````
Что получится:
```python
[
    {'id': 1, 'state': 'EXECUTED', 'date': '2023-10-01T10:00:00'},
    {'id': 3, 'state': 'EXECUTED', 'date': '2023-10-03T12:00:00'}
]
```
_______
## —` sort_by_date `— 


+ Функция сортирует операции по дате: (по умолчанию) новые будут в начале списка.

Пример:
```python
ops = [
    {'id': 1, 'date': '2023-10-03T12:00:00'},
    {'id': 2, 'date': '2023-10-01T10:00:00'},
    {'id': 3, 'date': '2023-10-02T11:00:00'}
]

sorted_ops = sort_by_date(ops, descending=True)
````
Что получится:
````python
[
    {'id': 1, 'date': '2023-10-03T12:00:00'},
    {'id': 3, 'date': '2023-10-02T11:00:00'},
    {'id': 2, 'date': '2023-10-01T10:00:00'}
]
````
+ *****Если у какой-то операции нет даты или она записана странно, 
эта операция окажется в конце — программа не сломается.*****


________
## — `get_mask_card_number` — 


+ Функция маскирует номер карты (16 цифр), оставляя начало и конец видимыми, а середину прячет за звёздочками.

Пример:
````python
card = "7000792289606361"
masked = get_mask_card_number(card)
````
Что получится:
```python
"7000 79** **** 6361"
````
+ Если передать что-то не то (не 16 цифр, буквы и т.п.), 
функция сообщит об ошибке — это защита от неправильных данных.

_________

## — `get_mask_account` — 


+ Функция маскирует номер счёта (20 цифр) и оставляет только две звёздочки и последние 4 цифры.

Пример:
````python
account = "73654108430135874305"
masked = get_mask_account(account)
````
Что получится:
````python
"**4305"
````
_________
## — `mask_account_card` — 

+ Универсальный маскировщик, симбиоз функций - `get_mask_account` и `get_mask_card_number`

+ Функция сама понимает, карта это или счёт, и прячет номер правильно. 
+ На вход задаётся строка с описанием банковского инструмента и номером.

Пример:
````python
data_1 = "Счет 73654108430135874305"
data_2 = "Visa Platinum 7000792289606361"

r1 = mask_account_card(data_1)
r2 = mask_account_card(data_2)
````
Что получится:
````python
"Счет **4305"                        # для счёта
"Visa Platinum 7000 79** **** 6361"  # для карты
````
___

## — `get_date` — 

+ Приводит дату к формату ДД.ММ.ГГГГ
+ Функция превращает длинную дату из базы в простой формат, который удобно читать.

Пример:
````python
date_str = "2023-10-05T14:30:00.123456"
formatted = get_date(date_str)
````
Что получится:
````python
"05.10.2023"
````
___

## — `filter_by_currency`  —
+ Возвращает итератор (генератор) по транзакциям, где код валюты совпадает с currency_code.

Пример:
````python
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
````
Что получится:
````python
{'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572', 'operationAmount': {'amount': '9824.07', 'currency': {'name': 'USD', 'code': 'USD'}}, 'description': 'Перевод организации', 'from': 'Счет 75106830613657916952', 'to': 'Счет 11776614605963066702'}
{'id': 142264268, 'state': 'EXECUTED', 'date': '2019-04-04T23:20:05.206878', 'operationAmount': {'amount': '79114.93', 'currency': {'name': 'USD', 'code': 'USD'}}, 'description': 'Перевод со счета на счет', 'from': 'Счет 19708645243227258542', 'to': 'Счет 75651667383060284188'}
````
___

## — `transaction_descriptions` —
+ Генератор, возвращающий описание каждой операции по очереди.

Пример:
````python
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
````
Что получится:
````
Перевод организации
Перевод со счета на счет
Перевод со счета на счет
Перевод с карты на карту
Перевод организации

````
___

## — card_number_generator —
+ Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

Пример:
````python
for card_number in card_number_generator(1, 5):
    print(card_number)
````
Что получится:
````
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
0000 0000 0000 0004
0000 0000 0000 0005
````
___
___

##  ~ `Как использовать функции вместе` ~


Сначала подключаем функции - импортируем (блок в начале текста этого файла), потом применяем их по очереди: 
+ сначала отобрать нужные операции, 
+ потом отсортировать, 
+ потом спрятать номера и привести даты 
к нужному виду.

*****Это помогает подготовить данные для вывода в виджете.*****
___


## ~ `Как запустить проект (Windows, PowerShell)` ~

Клонируем проект:

`PowerShell`
````
git clone https://github.com/feniball79-rgb/Homework-Widget-Project.git
cd Homework-Widget-Project
````
Ставим зависимости:

`PowerShell`
````
poetry install
````
Проверяем код (чтобы всё было аккуратно):

`PowerShell`
````
poetry run black src
poetry run flake8 src
poetry run mypy src
````
## `Все команды делай через `poetry run`, чтобы использовались нужные библиотеки.`
___
___
## ~ `Структура папок` ~
````python
├my-project/
├
├──src/
├    └─ my_project/
├        ├── processing.py   # filter_by_state, sort_by_date
├        ├── masks.py        # get_mask_card_number, get_mask_account
├        └── widget.py       # mask_account_card, get_date
├──tests/
     ├── test_filter_by_state.py
     ├── test_generators.py
     ├── test_get_date.py
     ├── test_get_mask_account.py
     ├── test_get_mask_card_number.py
     ├── test_mask_account_card.py
     └──test_sort_by_date.py
.coverage
.flake8      
.gitignore
poetry.lock
pyproject.toml
README.md
````
___
# ~  tests  ~
## Покрытие тестами

+ `filter_by_state`:

*проверка фильтрации по статусу, обработка неверных значений и пустого списка.*
___

+ `sort_by_date`: 

*сортировка по дате, обработка битых и отсутствующих дат, валидация типа входных данных.*
___

+ `mask_account_card`:

*авто-маскировка номера карты или счёта, контроль ввода данных правильного формата и длины, защита 
от инвалидных и пустых вводов.* 
___

+ `get_date`: 

*работа функции, защита от пустых и инвалидных вводов.*
___

### **Модуль маскирования (`masks.py`) с функциями:**


+ `get_mask_card_number`
+ `get_mask_account`

*тесты на корректное маскирование номеров счетов и карт, обработка крайних случаев (пустой ввод, короткие строки, буквы, пробелы).*
___

### **Модуль `generators` с функциями:**


+ `filter_by_currency` 

**фильтрации банковских транзакций по кодам валют**

*тесты на правильную фильтрацию*

*что генератор — это итератор, а не список*

*обработку отсутствия значения кодов валют*

*обработку пустого значения*

*обработку исключения StopIteration*
___

+ `transaction_descriptions`

**возвращающий описание каждой операции по очереди**

*тесты на все описания адресатов \ отправителей транзакций*

*отсутствие описания адресата \ отправителя*

*пустое значение в вызове функции*
___

+ `card_number_generator`

**Генератор номеров банковских карт**

*слишком большой номер и количество номеров будет ограничено*
___
___


+ ## Общее покрытие кода тестами: 92%.


