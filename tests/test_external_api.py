from unittest.mock import MagicMock, patch

import pytest

from my_project.external_api import amount_by_transactions


def test_amound_by_transactions_success():
    """Все валюты есть, API отвечает корректно"""

    transactions = [
        {"operationAmount": {"currency": {"code": "RUB"}, "amount": 1000.0}},
        {"operationAmount": {"currency": {"code": "USD"}, "amount": 10.0}},
        {"operationAmount": {"currency": {"code": "EUR"}, "amount": 5.0}},
    ]

    with patch("my_project.external_api.convert_json_to_python") as mock_convert:
        mock_convert.return_value = transactions

        with patch("my_project.external_api.os.getenv") as mock_getenv:
            mock_getenv.return_value = "fake_key"

            # API возвращает итоговую сумму конвертации, а не курс
            mock_resp_usd = MagicMock()
            mock_resp_usd.status_code = 200
            mock_resp_usd.json.return_value = {"result": 905.0}

            mock_resp_eur = MagicMock()
            mock_resp_eur.status_code = 200
            mock_resp_eur.json.return_value = {"result": 501.0}

            with patch(
                "my_project.external_api.requests.get",
                side_effect=[mock_resp_usd, mock_resp_eur],
            ) as mock_get:
                result = amount_by_transactions("dummy.json")

                # 1000 RUB + 905.0 (USD) + 501.0 (EUR) = 2406.0
                assert result == 2406.0
                assert mock_get.call_count == 2


def test_amound_by_transactions_only_rub():
    """Только рубли — API не вызывается"""

    transactions = [
        {"operationAmount": {"currency": {"code": "RUB"}, "amount": 500.0}},
        {"operationAmount": {"currency": {"code": "RUB"}, "amount": 250.5}},
    ]

    with patch("my_project.external_api.convert_json_to_python") as mock_convert:
        mock_convert.return_value = transactions

        with patch("my_project.external_api.os.getenv"):
            with patch("my_project.external_api.requests.get") as mock_get:
                result = amount_by_transactions("dummy.json")

                assert result == 750.5
                mock_get.assert_not_called()


def test_amound_by_transactions_api_error():
    """API вернул ошибку — функция выбрасывает RuntimeError"""

    transactions = [
        {"operationAmount": {"currency": {"code": "USD"}, "amount": 10.0}},
    ]

    with patch("my_project.external_api.convert_json_to_python") as mock_convert:
        mock_convert.return_value = transactions

        with patch("my_project.external_api.os.getenv"):
            mock_resp = MagicMock()
            mock_resp.status_code = 401
            mock_resp.text = "Unauthorized"

            with patch("my_project.external_api.requests.get", return_value=mock_resp):
                with pytest.raises(RuntimeError) as exc_info:
                    amount_by_transactions("dummy.json")

                assert "Ошибка API: 401" in str(exc_info.value)


def test_amound_by_transactions_zero_foreign():
    """Сумма в USD и EUR равна 0 — API не вызывается"""

    transactions = [
        {"operationAmount": {"currency": {"code": "RUB"}, "amount": 300.0}},
        {"operationAmount": {"currency": {"code": "USD"}, "amount": 0.0}},
    ]

    with patch("my_project.external_api.convert_json_to_python") as mock_convert:
        mock_convert.return_value = transactions

        with patch("my_project.external_api.os.getenv"):
            with patch("my_project.external_api.requests.get") as mock_get:
                result = amount_by_transactions("dummy.json")

                assert result == 300.0
                mock_get.assert_not_called()
