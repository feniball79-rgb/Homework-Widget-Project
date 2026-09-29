from functools import wraps
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для логирования процессов функции в консоль или в созданный файл,
    и перехвата, обработки возникающих исключений.
    """

    def logger(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            info_message_start = f"'{func.__name__}' started"
            info_message_finish = f"'{func.__name__}' Ok"

            # Логирование начала
            if filename:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(f"{info_message_start}\n")
                print(info_message_start)
            else:
                print(info_message_start)

            try:
                result = func(*args, **kwargs)

                # Логирование успеха
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"{info_message_finish}\n")
                print(info_message_finish)

                return result

            except Exception as e:
                error_msg = f"'{func.__name__}' error: {e}. Inputs: {args}, {kwargs}"

                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"{error_msg}\n")
                    # Важно: НЕ возвращаем print(...), он всегда None
                    raise  # пробрасываем исключение дальше, чтобы не скрывать ошибку
                else:
                    # В консоль: печатаем и пробрасываем
                    print(error_msg)
                    raise

        return wrapper

    return logger


if __name__ == "__main__":

    @log()  # filename="LOG.txt"
    def add_iti_ons(a: int | float, b: int | float) -> str:
        if b == 0:
            raise ZeroDivisionError("Деление на ноль")
        return f"ОТВЕТ: {a / b}"

    result_fin = add_iti_ons(7, 5)
    print(result_fin)
