from functools import wraps
from typing import Any, Callable

# Напишите декоратор log, который будет автоматически логировать начало и конец -
# - выполнения функции, а также ее результаты или возникшие ошибки.

# Если filename задан, логи записываются в указанный файл.
# Если filename не задан, логи выводятся в консоль.

# Логирование должно включать:
# Имя функции и результат выполнения при успешной операции.
# Имя функции, тип возникшей ошибки и входные параметры, если выполнение функции привело к ошибке.


def log(filename: object = None) -> Callable[[Any], Callable[[tuple[Any, ...], dict[str, Any]], Any | None]]:
    """
    Декоратор для логирования процессов функции в консоль или в созданный файл..
    :rtype: None
    """
    def logger(func) -> Callable[[tuple[Any, ...], dict[str, Any]], Any | None]:

        # noinspection PyTypeChecker
        @wraps(func)
        def wrapper(*args, **kwargs):

            info_massage_start = f"Процесс {func.__name__} запущен: Ok\n"
            info_massage_finish = f"Процесс {func.__name__} завершён: Ok"
            info_massage_error = f"Процесс {func.__name__} остановлен из_за ошибки: "

            if filename:                                              # Если filename ЗАДАН -- пишем в файл.
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(info_massage_start)
            else:                                                     # Если filename НЕ задан -- выводим в консоль.
                print(info_massage_start)

            try:
                result = func(*args, **kwargs)
                if filename:                                         # Если filename ЗАДАН -- пишем в файл.
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"{info_massage_finish} \n")
                else:                                                # Если filename НЕ задан -- выводим в консоль.
                    print(info_massage_finish)
                return result

            except Exception as e:
                print(f"Что-то заклинило из-за: <<{e}>> ")

                if filename:                                         # Если filename ЗАДАН -- пишем в файл.
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"{info_massage_error} <<{e}>>\n")
                else:                                                # Если filename НЕ задан -- выводим в консоль.
                    print(f"{info_massage_error} <<{e}>>")

        return wrapper

    return logger




@log()   # (filename="LOG.txt")
def additions(a: int, b: int) -> str:
    return f"ОТВЕТ: {a / b}"


# noinspection PyTypeChecker
result_fin = additions(10, 0)
print(result_fin)
