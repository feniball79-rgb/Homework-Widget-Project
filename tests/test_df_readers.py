from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from my_project.df_readers import get_transactions_csv, get_transactions_xlsx


def test_get_transactions_csv_success():
    """
    Тест: успешный разбор CSV.
    Мок должен быть итерируемым (отдавать строки), а не просто иметь .read().
    """
    mock_file_content = [
        "date,amount,category\n",
        "2024-01-01,100.5,food\n",
        "2024-01-02,-50.0,transport\n",
    ]

    # Создаём мок-файл, который ведёт себя как настоящий файл:
    mock_file = MagicMock()
    # Важно: DictReader итерирует по файлу, поэтому нужен __iter__
    mock_file.__iter__.return_value = iter(mock_file_content)
    # Для совместимости с контекстным менеджером:
    mock_file.__enter__ = lambda self: self
    mock_file.__exit__ = lambda *args: None

    with patch("my_project.df_readers.open", return_value=mock_file) as mock_open:
        result = get_transactions_csv("transactions.csv")

        # Проверяем, что open вызвали с нужными аргументами
        mock_open.assert_called_once()
        _, kwargs = mock_open.call_args
        assert kwargs.get("encoding") == "utf-8"
        assert kwargs.get("newline") == ""

        # Проверяем результат
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["date"] == "2024-01-01"
        assert float(result[0]["amount"]) == pytest.approx(100.5)
        assert result[1]["category"] == "transport"


def test_get_transactions_csv_wrong_extension():
    """Тест: неверный формат файла — должна быть ValueError."""
    with pytest.raises(ValueError, match="Ожидается CSV-файл"):
        get_transactions_csv("transactions.xlsx")


@patch("my_project.df_readers.open")
def test_get_transactions_csv_file_not_found(mock_open):
    """Тест: файл не найден — должна быть FileNotFoundError."""
    mock_open.side_effect = FileNotFoundError("Нет такого файла")

    with pytest.raises(FileNotFoundError):
        get_transactions_csv("transactions.csv")

    mock_open.assert_called_once()


print("*****************************************")


@patch("my_project.df_readers.pd.read_excel")
def test_get_transactions_xlsx_success(mock_read_excel):
    """Тест: успешный разбор XLSX через pandas."""
    # Подготовим фейковые данные, которые read_excel якобы прочитал
    mock_df = pd.DataFrame(
        [
            {"date": "2024-01-01", "amount": 100.5, "category": "food"},
            {"date": "2024-01-02", "amount": -50.0, "category": "transport"},
        ]
    )
    mock_read_excel.return_value = mock_df

    result = get_transactions_xlsx("transactions.xlsx")

    # Проверяем, что read_excel вызвали с правильным путём (мы его не видим внутри, но вызов был)
    assert mock_read_excel.called

    # Проверяем результат
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["category"] == "food"
    assert pytest.approx(result[1]["amount"]) == -50.0


def test_get_transactions_xlsx_wrong_extension():
    """Тест: неверный формат файла."""
    with pytest.raises(ValueError, match="Ожидается Excel-файл"):
        get_transactions_xlsx("transactions.csv")


@patch("my_project.df_readers.pd.read_excel", side_effect=FileNotFoundError("Нет файла"))
def test_get_transactions_xlsx_file_not_found(mock_read_excel):
    """Тест: файл не найден."""
    with pytest.raises(FileNotFoundError):
        get_transactions_xlsx("transactions.xlsx")

    assert mock_read_excel.called
