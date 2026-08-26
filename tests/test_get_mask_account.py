import pytest

from my_project.masks import get_mask_account

# Примеры номеров счетов, для вводимых данных
# 35383033474447895560
# 64686473678894779589
# 73654108430135874305


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("35383033474447895560", "**5560"),
        ("64686473678894779589", "**9589"),
        ("73654108430135874305", "**4305"),
    ],
)
def test_get_mask_get_mask_account_param(card_number: str, expected: str) -> None:
    assert get_mask_account(card_number) == expected


@pytest.fixture
def fixt() -> str:
    return "73654108430135874305"


def test_get_mask_account(fixt) -> None:
    assert get_mask_account(fixt) == "**4305"


def test_get_mask_account_empty_str(fixt) -> None:
    with pytest.raises(ValueError):
        get_mask_account("")


def test_get_mask_account_is_space(fixt) -> None:
    with pytest.raises(ValueError):
        get_mask_account(" ")


def test_get_mask_account_is_letters(fixt) -> None:
    with pytest.raises(ValueError):
        get_mask_account("card")


def test_get_mask_account_is_short_number(fixt) -> None:
    with pytest.raises(ValueError):
        get_mask_account("123")
