import json
import logging
from typing import Any, List

from my_project.project_root_Path_finder import get_project_root

# Создание папки logs/ если такая отсутствует
logs_dir = get_project_root() / "logs"
logs_dir.mkdir(exist_ok=True)

utils_logger = logging.getLogger(__name__)  # создание логера с именем модуля
utils_logger.setLevel(logging.DEBUG)  # уровень важности логов

file_handler = logging.FileHandler(logs_dir / "utils.log", mode="w", encoding="utf-8")  # создание хэндлера и файла
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")  # формат логов
file_handler.setFormatter(file_formatter)  # привязка форматера к хэндлеру
utils_logger.addHandler(file_handler)  # привязка хэндлера к логеру


def convert_json_to_python(filename: str) -> List[dict[str, Any]]:
    """Принимает имя JSON файла и возвращает содержимое, преобразованное в
    Python объект — список словарей.
    """
    root = get_project_root()
    file_path = root / "data" / filename
    utils_logger.info(f"Чтение файла: {filename}")
    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
            # Явно проверяем, что это список, чтобы успокоить mypy
            if not isinstance(data, list):
                print("Ошибка: ожидался список в JSON")
                utils_logger.error(f"Ошибка: ожидался список в JSON в файле {filename}")
                return []

            for item in data:
                if not isinstance(item, dict):
                    print("Ошибка: не все элементы в JSON — словари")
                    utils_logger.error(f"Ошибка: не все элементы в JSON — словари в файле {filename}")
                    return []

            utils_logger.info(f"Успешно прочитано {len(data)} транзакций из {filename}")
            return data

    except FileNotFoundError:
        utils_logger.error(f"Файл не найден: {filename}")
        print("Файл не найден")
        return []

    except json.JSONDecodeError:
        utils_logger.error(f"Ошибка декодирования JSON в файле {filename}")
        print("Ошибка декодирования файла")
        return []


# if __name__ == "__main__":
#     converted = convert_json_to_python("operations.json")
#     print(converted)
