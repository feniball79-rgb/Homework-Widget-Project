import csv
from typing import Any

import pandas as pd

from my_project.project_root_Path_finder import get_project_root


def get_transactions_csv(filename: str) -> list[Any]:
    """
    Читает CSV-файл с финансовыми операциями и возвращает список словарей.

    :param filename: имя CSV-файла (без пути, только имя файла)
    :return: list[dict] — список транзакций
    :raises FileNotFoundError: если файл не найден
    :raises ValueError: если расширение не .csv
    """
    root = get_project_root()
    file_path = root / "data" / filename

    # Проверка расширения
    if file_path.suffix.lower() != ".csv":
        raise ValueError(f"Ожидается CSV-файл, но передано: {filename}")

    with open(file_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        # Если CSV пустой или нет заголовков, DictReader всё равно вернёт пустой список
        return list(reader)


if __name__ == "__main__":
    res = get_transactions_csv("transactions.csv")
    print(res)

print("******************************************************")


def get_transactions_xlsx(filename: str) -> Any:
    """
    Читает XLSX-файл с финансовыми операциями и возвращает список словарей.

    :param filename: имя файла (например, 'transactions.xlsx')
    :return: list[dict] — список транзакций
    :raises ValueError: если расширение не .xlsx
    :raises FileNotFoundError: если файл не найден
    """
    root = get_project_root()
    file_path = root / "data" / filename

    # 1. Проверка расширения
    if file_path.suffix.lower() not in (".xlsx", ".xls"):
        raise ValueError(f"Ожидается Excel-файл (.xlsx или .xls), но передано: {filename}")

    # 2. Читаем напрямую по пути.
    # pd.read_excel сам откроет файл, ему не нужен контекстный менеджер open()
    df = pd.read_excel(file_path)

    # 3. Превращаем DataFrame в список словарей
    # orient='records' даёт список dict: [{'date': ..., 'amount': ...}, ...]
    return df.to_dict(orient="records")


if __name__ == "__main__":
    res = get_transactions_xlsx("transactions_excel.xlsx")
    print(res)
