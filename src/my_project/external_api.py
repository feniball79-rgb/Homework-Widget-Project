import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

from my_project.utils import convert_json_to_python


def amount_by_transactions(filename: str) -> float:
    """Принимает имя JSON-файла с транзакциями, переводит USD и EUR в RUB по курсу через API."""
    read_file = convert_json_to_python(filename)

    sum_rub: float = 0.0
    sum_usd: float = 0.0
    sum_eur: float = 0.0

    for x in read_file:
        test_search = x.get("operationAmount", {}).get("currency", {}).get("code")

        if test_search == "RUB":
            amount = x.get("operationAmount", {}).get("amount")
            if amount is not None:
                sum_rub += float(amount)
        elif test_search == "USD":
            amount = x.get("operationAmount", {}).get("amount")
            if amount is not None:
                sum_usd += float(amount)
        elif test_search == "EUR":
            amount = x.get("operationAmount", {}).get("amount")
            if amount is not None:
                sum_eur += float(amount)

    load_dotenv()
    api_key: Optional[str] = os.getenv("API_KEY")
    if api_key is None:
        raise RuntimeError("Не задан API_KEY в .env")

    headers: Dict[str, str] = {"apikey": api_key}

    def convert_to_rub(amount: float, currency: str) -> float:
        """Конвертирует сумму в RUB через API."""
        if amount == 0:
            return 0.0

        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise RuntimeError(f"Ошибка API: {response.status_code} — {response.text}")

        data: Any = response.json()
        # Явно проверяем тип результата, чтобы успокоить mypy
        raw_result = data.get("result")
        if raw_result is None:
            return 0.0
        try:
            result = float(raw_result)
        except (TypeError, ValueError):
            return 0.0
        return result

    usd_in_rub = convert_to_rub(sum_usd, "USD")
    eur_in_rub = convert_to_rub(sum_eur, "EUR")

    total_rub = sum_rub + usd_in_rub + eur_in_rub
    return round(total_rub, 2)


if __name__ == "__main__":
    test_res = amount_by_transactions("operations.json")
    print(test_res)
    print(type(test_res))
