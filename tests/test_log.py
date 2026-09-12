import pytest

from my_project.decorators import log


# noinspection PyTypeChecker
def test_log_():

    # ====== ТЕСТ 1: Работоспособность декоратора @log.
    @log(filename=None)
    def for_testing_foo(a: int, b: int):
        return a / b

    result_fun = for_testing_foo(10, 5)
    assert result_fun == 2.0

    # ====== ТЕСТ 2: Вызов исключения - деление на ноль.

    with pytest.raises(Exception, match="division by zero"):
        for_testing_foo(1, 0)

    # ====== ТЕСТ 3: Вызов исключения - недопустимый тип аргументов.

    with pytest.raises(Exception, match="unsupported operand type"):
        for_testing_foo(1, "0")

    # ====== ТЕСТ 4: Вызов исключения - отсутствие аргументов в вызываемой функции.

    with pytest.raises(Exception, match="missing 2 required positional arguments"):
        for_testing_foo()


# ====== ТЕСТ 5: Ошибка в функции — лог в файл ======


def test_error_file(tmp_path):
    """
    Что проверяем:
    1. При ошибке лог записывается в файл.
    2. В файле есть имя функции и слово об ошибке.
    """
    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def divide(a, b):
        return a / b

    result = divide(10, 0)

    assert result is None
    content = log_file.read_text(encoding="utf-8")
    assert "by zero" in content.lower()
    assert "divide" in content


# ====== ТЕСТ 6: Декоратор сохраняет имя функции ======


def test_preserves_name():
    """
    Что проверяем:
    @wraps(func) копирует имя и документацию оригинальной функции.
    Без @wraps имя было бы "wrapper" — и отладка превратилась бы
    в угадайку: не понять, какая функция на самом деле вызвана.
    """

    @log(filename=None)
    def my_function():
        """Докстринг функции."""
        return 42

    assert my_function.__name__ == "my_function"
    assert my_function.__doc__ == "Докстринг функции."


# ====== ТЕСТ 7: Успешный вызов — лог в файл ======


def test_success_file(tmp_path):
    """
    Что проверяем:
    1. Функция возвращает правильный результат.
    2. Лог записывается в файл (а не в консоль).
    3. В файле есть сообщения о запуске и завершении.
    """

    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def add(a, b):
        return a + b

    result = add(2, 3)

    assert result == 5

    # Файл реально создался
    assert log_file.exists()

    # Читаем содержимое файла
    content = log_file.read_text(encoding="utf-8")
    assert "started" in content
    assert "Ok" in content
    assert "add" in content
