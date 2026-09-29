from collections.abc import Iterator
from typing import Any


def filter_by_currency(transactions: list[dict[str, Any]], currency_code: str) -> Iterator[dict[str, Any]]:
    """
    Возвращает генератор по транзакциям, где код валюты совпадает с currency_code.

    :param transactions: список словарей-транзакций
    :param currency_code: код валюты (например, "USD")
    :return: генератор подходящих транзакций
    """
    for t in transactions:
        curr_code = t.get("operationAmount", {}).get("currency", {}).get("code")
        if curr_code == currency_code:
            yield t


transactions: list[dict[str, Any]] = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 123456789,
        "state": "EXECUTED",
        "date": "2020-01-01T12:00:00.000000",
        "operationAmount": {"amount": "5000.00", "currency": {"name": "RUB", "code": "RUB"}},
        "description": "Перевод в рублях",
        "from": "Счет 11112222333344445555",
        "to": "Счет 66667777888899990000",
    },
]

if __name__ == "__main__":
    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        print(next(usd_transactions))


print("______________________________________________________________")


def transaction_descriptions(trans_actions: list[dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, возвращающий описание каждой операции по очереди.

    :param trans_actions: список словарей-транзакций
    :return: генератор строк с описаниями операций
    """
    for t in trans_actions:
        description = t.get("description", "Нет описания")
        yield description


trans_actions: list[dict[str, Any]] = [
    # ... (данные не меняются)
]

if __name__ == "__main__":
    descriptions = transaction_descriptions(trans_actions)
    for _ in range(5):
        print(next(descriptions))


print("________________________________________________________________")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    :param start: начальное значение номера (целое число)
    :param end: конечное значение номера (целое число)
    :return: генератор строк с номерами карт
    """
    start = max(1, start)
    end = min(9999999999999999, end)

    if start > end:
        return

    for number in range(start, end + 1):
        num_str = f"{number:016d}"
        card_numberr = f"{num_str[0:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
        yield card_numberr


if __name__ == "__main__":
    for card_number in card_number_generator(1, 5):
        print(card_number)
