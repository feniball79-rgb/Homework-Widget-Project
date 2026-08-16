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
    # Если нужна строгая валидация, раскомментируй блок ниже:
    # if state_mode not in ALLOWED_STATES:
    #     raise ValueError(f"state_mode должен быть одним из {ALLOWED_STATES}")

    return [record for record in records if record.get("state") == state_mode]


# if __name__ == "__main__":
#
#     print(
#         filter_by_state(
#             [
#                 {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
#                 {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
#                 {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
#                 {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
#             ],
#             state_mode="CANCELED",
#         )
#     )


from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


def sort_by_date(records: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Безопасная сортировка транзакций по дате для банковского виджета.
    Гарантирует работу даже при смешанных форматах дат и отсутствующих полях.
    """

    def get_sort_key(record: Dict[str, Any]) -> Tuple[int, Optional[datetime]]:
        date_str = record.get("date")

        # Если даты нет вообще - возвращаем приоритет 1 (в конец списка)
        if not date_str:
            return (1, None)

        # Пробуем распарсить дату. Поддерживаем форматы с мс и без.
        # Если формат неизвестен - считаем дату битой и отправляем в конец.
        try:
            # Сначала пробуем формат с микросекундами (он строже)
            if "." in str(date_str):
                dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
            else:
                # Если точки нет, пробуем без микросекунд
                dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

            # Возвращаем приоритет 0 (хорошая дата) и сам объект datetime
            return (0, dt)
        except (ValueError, TypeError):
            # Если не удалось распарсить - считаем дату битой (приоритет 1)
            return (1, None)

    # Сортируем по кортежу (приоритет, дата).
    # Сначала идут все хорошие даты (отсортированные по времени), потом битые.
    return sorted(records, key=get_sort_key, reverse=descending)


# if __name__ == "__main__":
#
#      print(sort_by_date([{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
#             {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
#             {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
#             {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}],
#            False))
