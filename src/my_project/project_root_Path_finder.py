from pathlib import Path


def get_project_root() -> Path:
    """Всегда безошибочно прокладывает путь от текущего файла использующей её функции
    (из !любого! текущего места нахождения вызывающей функции в проекте) до
    директории корня проекта, чтобы уже от него легко указывать путь до другого нужного файла.
     Маркером поиска корня проекта является pyproject.toml - если проект создаётся
    с помощью Poetry.
    НО !! можно любой другой ориентировочный маркер подставить из корня
    проекта - например, .gitignore, README.md или другие...
    Можно импортировать и использовать в других функциях"""

    current = Path(__file__).resolve()
    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return current
