import pytest

from my_project.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)

# --- Фикстуры ---


@pytest.fixture
def transactions():
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 1",
            "to": "Счет 2",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 3",
            "to": "Счет 4",
        },
    ]


@pytest.fixture
def mixed_transactions():
    return [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
        },
        {
            "id": 2,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "5000.00", "currency": {"name": "RUB", "code": "RUB"}},
            "description": "Перевод в рублях",
        },
        {
            "id": 3,
            "state": "EXECUTED",
            "date": "2020-01-01T12:00:00.000000",
            "operationAmount": {"amount": "120.50", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Перевод в евро",
        },
    ]


@pytest.fixture
def transactions_with_missing_description():
    return [{"description": "Есть описание"}, {}, {"description": "Ещё одно описание"}]  # нет description


# --- Тесты filter_by_currency ---


@pytest.mark.parametrize(
    "currency,expected_count",
    [
        ("USD", 1),
        ("RUB", 1),
        ("EUR", 1),
        ("JPY", 0),
    ],
)
def test_filter_by_currency_counts(mixed_transactions, currency, expected_count):
    result = list(filter_by_currency(mixed_transactions, currency))
    assert len(result) == expected_count


def test_filter_by_currency_empty_list():
    transactions = []
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []


def test_filter_by_currency_no_matching_currency():
    transactions = [
        {"operationAmount": {"currency": {"code": "RUB"}}},
        {"operationAmount": {"currency": {"code": "EUR"}}},
    ]
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []


def test_filter_by_currency_returns_iterator():
    gen = filter_by_currency([{"operationAmount": {"currency": {"code": "USD"}}}], "USD")
    # генератор — это итератор, но не список
    assert hasattr(gen, "__iter__")
    assert not isinstance(gen, list)


# --- Тесты transaction_descriptions ---


def test_transaction_descriptions_returns_all_descriptions(mixed_transactions):
    descriptions = list(transaction_descriptions(mixed_transactions))
    expected = [
        "Перевод организации",
        "Перевод в рублях",
        "Перевод в евро",
    ]
    assert descriptions == expected


def test_transaction_descriptions_empty_list():
    result = list(transaction_descriptions([]))
    assert result == []


def test_transaction_descriptions_missing_description(transactions_with_missing_description):
    descriptions = list(transaction_descriptions(transactions_with_missing_description))
    # по нашей реализации отсутствующее description заменяется на "Нет описания"
    assert descriptions == ["Есть описание", "Нет описания", "Ещё одно описание"]


def test_transaction_descriptions_iterator_behavior():
    gen = transaction_descriptions([{"description": "Test"}])
    assert next(gen) == "Test"
    with pytest.raises(StopIteration):
        next(gen)


# --- Тесты card_number_generator ---


@pytest.mark.parametrize(
    "start,end,expected",
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (
            9999999999999995,
            9999999999999999,
            [
                "9999 9999 9999 9995",
                "9999 9999 9999 9996",
                "9999 9999 9999 9997",
                "9999 9999 9999 9998",
                "9999 9999 9999 9999",
            ],
        ),
    ],
)
def test_card_number_generator_range_and_format(start, end, expected):
    result = list(card_number_generator(start, end))
    assert result == expected


def test_card_number_generator_invalid_range():
    # start > end — генератор ничего не возвращает
    result = list(card_number_generator(10, 5))
    assert result == []


def test_card_number_generator_clamped_bounds():
    # слишком большой end будет ограничен
    result = list(card_number_generator(9999999999999998, 999999999999999999))
    assert len(result) == 2
    assert result[0] == "9999 9999 9999 9998"
    assert result[1] == "9999 9999 9999 9999"


def test_card_number_generator_iterator_behavior():
    gen = card_number_generator(1, 3)
    assert next(gen) == "0000 0000 0000 0001"
    assert next(gen) == "0000 0000 0000 0002"
    assert next(gen) == "0000 0000 0000 0003"
    with pytest.raises(StopIteration):
        next(gen)
