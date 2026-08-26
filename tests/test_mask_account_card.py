import pytest

from my_project.widget import mask_account_card


@pytest.mark.parametrize(
    "data_receiver, expected",
    [
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
    ],
)
def test_mask_account_card_param(data_receiver: str, expected: str) -> None:
    assert mask_account_card(data_receiver) == expected


@pytest.fixture
def fixt() -> None:
    return


def test_get_mask_account_empty_str(fixt) -> None:
    with pytest.raises(ValueError):
        mask_account_card("")


def test_get_mask_account_is_space(fixt) -> None:
    with pytest.raises(ValueError):
        mask_account_card(" ")


def test_get_mask_account_is_letters(fixt) -> None:
    with pytest.raises(ValueError):
        mask_account_card("card")


def test_get_mask_account_is_short_number(fixt) -> None:
    with pytest.raises(ValueError):
        mask_account_card("123")
