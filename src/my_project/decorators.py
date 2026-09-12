from functools import wraps
from typing import Any


def log(filename=None) -> Any:
    """
    Декоратор для логирования процессов функции в консоль или в созданный файл,
    и перехвата, обработки возникающих исключений.
    :rtype: Any
    :input: Any
    """

    def logger(func: Any) -> Any:
        """
        :type func: Any
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            info_massage_start = f"'{func.__name__}' started"
            info_massage_finish = f"'{func.__name__}' Ok"

            # Запись лога об успешном запуске функции
            if filename:

                # Если filename ЗАДАН -- пишем в файл.
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(f"{info_massage_start} \n")

            # Если filename НЕ задан -- выводим в консоль.
            else:
                print(info_massage_start)

            # Запуск функции с обработкой исключений.
            try:
                result = func(*args, **kwargs)

                # Запись лога(в файл|в консоль) об успешном завершении функции.
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"{info_massage_finish} \n")
                else:
                    print(info_massage_finish)
                return result

            # Отлов исключений.
            except Exception as e:

                # Запись логов(в файл|в консоль) о возникших исключениях.
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"'{func.__name__}'error: {e}  Inputs:{args, kwargs}\n")

                # Отлов и обработка исключений
                else:
                    raise Exception(f"'{func.__name__}'error: {e}. Inputs:{args, kwargs}")

                return print(f"'{func.__name__}'error: {e}. Inputs:{args, kwargs}")

        return wrapper

    return logger


if __name__ == "__main__":

    @log()  # (filename="LOG.txt")
    def add_iti_ons(a: Any, b: Any) -> Any:
        return f"ОТВЕТ: {a / b}"

    result_fin = add_iti_ons(7, 5)
    print(result_fin)
