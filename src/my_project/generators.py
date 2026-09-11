from typing import Any, Generator


def filter_by_currency(transactions, currency_code) -> Generator[Any, Any, None]:
    """
    Возвращает итератор (генератор) по транзакциям, где код валюты совпадает с currency_code.

    :type transactions:list[dict]
    :param transactions: список словарей-транзакций
    :param currency_code: код валюты (например, "USD")
    :return: итератор подходящих транзакций
    """
    for t in transactions:
        # Безопасно получаем код валюты, избегая ошибок при отсутствии ключей
        curr_code = t.get("operationAmount", {}).get("currency", {}).get("code")
        if curr_code == currency_code:
            yield t


transactions = [
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

# ___________________________________________________________


def transaction_descriptions(trans_actions) -> Generator[Any, Any, None]:
    """
    Генератор, возвращающий описание каждой операции по очереди.

    :param trans_actions: список словарей-транзакций
    :return: итератор (генератор) строк с описаниями операций
    """
    for t in trans_actions:
        description = t.get("description", "Нет описания")
        yield description


trans_actions = [
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
        "description": "Перевод со счета на счет",
        "from": "Счет 11112222333344445555",
        "to": "Счет 66667777888899990000",
    },
    {
        "id": 987654321,
        "state": "EXECUTED",
        "date": "2020-02-01T12:00:00.000000",
        "operationAmount": {"amount": "3000.00", "currency": {"name": "RUB", "code": "RUB"}},
        "description": "Перевод с карты на карту",
        "from": "Карта 1111222233334444",
        "to": "Карта 5555666677778888",
    },
    {
        "id": 112233445,
        "state": "EXECUTED",
        "date": "2020-03-01T12:00:00.000000",
        "operationAmount": {"amount": "4000.00", "currency": {"name": "RUB", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Счет 22223333444455556666",
        "to": "Счет 77778888999900001111",
    },
]


if __name__ == "__main__":

    descriptions = transaction_descriptions(trans_actions)
    for _ in range(5):
        print(next(descriptions))


# ________________________________________________________________


def card_number_generator(start, end) -> Any:
    """
    Генератор номеров банковских карт в формате XXXX XXXX XXXX XXXX.

    :param start: начальное значение номера (целое число)
    :param end: конечное значение номера (целое число)
    :return: итератор (генератор) строк с номерами карт
    """
    # Ограничиваем диапазон допустимыми значениями
    start = max(1, start)
    end = min(9999999999999999, end)

    if start > end:
        return  # пустой диапазон — ничего не генерируем

    for number in range(start, end + 1):
        # Формируем 16‑значную строку с ведущими нулями
        num_str = f"{number:016d}"
        # Разбиваем на группы по 4 цифры через пробел
        card_numberr = f"{num_str[0:4]} {num_str[4:8]} {num_str[8:12]} {num_str[12:16]}"
        yield card_numberr


if __name__ == "__main__":

    for card_number in card_number_generator(1, 5):
        print(card_number)
