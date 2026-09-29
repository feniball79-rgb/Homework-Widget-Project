import json
from pathlib import Path
from typing import Any, List

from my_project.project_root_Path_finder import get_project_root


def convert_json_to_python(filename: str) -> List[dict[str, Any]]:
    """Принимает имя JSON файла и возвращает содержимое, преобразованное в
    Python объект — список словарей.
    """
    root = get_project_root()
    file_path = root / "data" / filename

    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
            # Явно проверяем, что это список, чтобы успокоить mypy
            if not isinstance(data, list):
                print("Ошибка: ожидался список в JSON")
                return []
            # Убеждаемся, что элементы — словари (mypy всё равно не проверит это в рантайме,
            # но так код понятнее и безопаснее)
            for item in data:
                if not isinstance(item, dict):
                    print("Ошибка: не все элементы в JSON — словари")
                    return []
            return data  # Теперь mypy видит, что data — это list, и мы его проверили
    except FileNotFoundError:
        print("Файл не найден")
        return []
    except json.JSONDecodeError:
        print("Ошибка декодирования файла")
        return []


if __name__ == "__main__":
    converted = convert_json_to_python("operations.json")
    print(converted)
