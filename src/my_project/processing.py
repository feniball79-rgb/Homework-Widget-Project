from typing import Any, Dict, List, Optional

ALLOWED_STATES = {"EXECUTED", "CANCELED"}  # можно расширить, если появятся новые статусы


def filter_by_state(records: List[Dict[str, Any]], state_mode: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Возвращает новый список словарей, содержащих только те элементы,
    у которых ключ 'state' равен state_mode.

    :param records: список словарей с данными
    :param state_mode: значение для ключа 'state', по умолчанию 'EXECUTED'
    :return: отфильтрованный список словарей
    """
    # Если хочешь строгую валидацию, раскомментируй блок ниже:
    # if state_mode not in ALLOWED_STATES:
    #     raise ValueError(f"state_mode должен быть одним из {ALLOWED_STATES}")

    return [record for record in records if record.get("state") == state_mode]
