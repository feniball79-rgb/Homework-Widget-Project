import pytest

from my_project.widget import get_date


@pytest.fixture
def fixt() -> None:
    return


def test_get_date_empty_str() -> None:
    with pytest.raises(ValueError):
        get_date("")


def test_get_date_space() -> None:
    with pytest.raises(ValueError):
        get_date("  ")


@pytest.mark.parametrize(
    "date_string, expected",
    [
        ("2026-04-11T02:30:18.67140", "11.04.2026"),
        ("2024-03-15T02:26:18.67140", "15.03.2024"),
        ("2022-02-22T02:26:01.67140", "22.02.2022"),
    ],
)
def test_get_date_param(date_string: str, expected: str) -> None:
    assert get_date(date_string) == expected
