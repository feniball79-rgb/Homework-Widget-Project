import pytest

from my_project.decorators import log


def test_log_success_console(capsys):
    """Успешный вызов без файла — лог в консоль, результат возвращается."""

    @log(filename=None)
    def for_testing_foo(a: int, b: int):
        return a / b

    result = for_testing_foo(10, 5)

    assert result == 2.0
    captured = capsys.readouterr()
    assert "started" in captured.out
    assert "Ok" in captured.out


def test_log_exception_console(capsys):
    """Ошибка без файла — исключение пробрасывается, лог в консоль."""

    @log(filename=None)
    def for_testing_foo(a: int, b: int):
        return a / b

    with pytest.raises(ZeroDivisionError, match="division by zero"):
        for_testing_foo(1, 0)

    captured = capsys.readouterr()
    assert "error" in captured.out
    assert "division by zero" in captured.out


def test_log_exception_wrong_type(capsys):
    """Ошибка типа — исключение пробрасывается."""

    @log(filename=None)
    def for_testing_foo(a: int, b: int):
        return a / b

    with pytest.raises(TypeError, match="unsupported operand"):
        for_testing_foo(1, "0")

    captured = capsys.readouterr()
    assert "error" in captured.out


def test_log_exception_missing_args(capsys):
    """Нехватка аргументов — исключение пробрасывается."""

    @log(filename=None)
    def for_testing_foo(a: int, b: int):
        return a / b

    with pytest.raises(TypeError, match="missing 2 required positional arguments"):
        for_testing_foo()

    captured = capsys.readouterr()
    assert "error" in captured.out


def test_error_file(tmp_path):
    """Ошибка с файлом — лог пишется в файл, исключение пробрасывается."""

    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError, match="division by zero"):
        divide(10, 0)

    content = log_file.read_text(encoding="utf-8")
    assert "by zero" in content.lower()
    assert "divide" in content


def test_preserves_name():
    """@wraps сохраняет имя и докстринг функции."""

    @log(filename=None)
    def my_function():
        """Докстринг функции."""
        return 42

    assert my_function.__name__ == "my_function"
    assert my_function.__doc__ == "Докстринг функции."


def test_success_file(tmp_path):
    """Успешный вызов с файлом — результат возвращается, лог в файле."""

    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def add(a, b):
        return a + b

    result = add(2, 3)

    assert result == 5
    assert log_file.exists()

    content = log_file.read_text(encoding="utf-8")
    assert "started" in content
    assert "Ok" in content
    assert "add" in content


def test_error_file_contains_inputs(tmp_path):
    """В файл пишутся аргументы, вызвавшие ошибку."""

    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def divide(a, b):
        return a / b

    with pytest.raises(TypeError):
        divide("строка", 42)

    content = log_file.read_text(encoding="utf-8")
    assert "Inputs" in content
    assert "divide" in content
