from typing import Any

import pytest

from my_project.masks import get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1596837868705199", "1596 83** **** 5199"),
        ("7158300734726758", "7158 30** **** 6758"),
        ("6831982476737658", "6831 98** **** 7658"),
    ],
)
def test_get_mask_card_number_param(card_number: str, expected: str) -> None:
    assert get_mask_card_number(card_number) == expected


# примеры вводимых данных
# "7000792289606361", "1596837868705199", "7158300734726758", "6831982476737658" - примеры вводимых данных


@pytest.fixture
def fixt() -> list[dict[str, Any]]:
    return


def test_get_mask_card_number_empty_str(fixt):
    with pytest.raises(ValueError):
        get_mask_card_number("")


def test_get_mask_card_number_is_space(fixt):
    with pytest.raises(ValueError):
        get_mask_card_number(" ")


def test_get_mask_card_number_is_letters(fixt):
    with pytest.raises(ValueError):
        get_mask_card_number("card")


def test_get_mask_card_number_is_short(fixt):
    with pytest.raises(ValueError):
        get_mask_card_number("123")
