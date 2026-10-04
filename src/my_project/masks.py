import logging

from my_project.project_root_Path_finder import get_project_root

# Создание папки logs/ если такая отсутствует
logs_dir = get_project_root() / "logs"
logs_dir.mkdir(exist_ok=True)

masks_logger = logging.getLogger(__name__)  # создание логера с именем модуля
masks_logger.setLevel(logging.DEBUG)  # уровень важности логов

file_handler = logging.FileHandler(logs_dir / "masks.log", mode="w", encoding="utf-8")  # создание хэндлера и файла
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")  # формат логов
file_handler.setFormatter(file_formatter)  # привязка форматера к хэндлеру
masks_logger.addHandler(file_handler)  # привязка хэндлера к логеру


def get_mask_card_number(card_number: str) -> str:
    """Функция принимает номер карты клиента банка и маскирует часть цифр под звёздочками.
    Выводит замаскированный номер в формате ХХХХ ХХ** **** ХХХХ.
    :rtype: str
    """
    masks_logger.info(f"Чтение введённого номера КАРТЫ: {card_number}")

    card_num = str(card_number)

    if card_num == "":
        masks_logger.error("Ошибка: Нельзя вводить пустые значения")
        raise ValueError("Нельзя вводить пустые значения")

    if not str(card_num).isdigit():
        masks_logger.error("Ошибка: Номер КАРТЫ должен состоять ТОЛЬКО из цифры")
        raise ValueError("Номер КАРТЫ должен состоять ТОЛЬКО из цифры")

    if len(str(card_num)) != 16:
        masks_logger.error("Ошибка: Номер КАРТЫ должен содержать ровно 16 символов")
        raise ValueError("Номер КАРТЫ должен содержать ровно 16 символов")

    nbr_mask = str(card_num)[0:6] + "******" + str(card_num)[-4:]
    nbr_mask_parts = nbr_mask[:4] + " " + nbr_mask[4:8] + " " + nbr_mask[8:12] + " " + nbr_mask[12:]

    masks_logger.info(f"Маскировка введённого номера КАРТЫ: {card_number} - проведена успешно")

    return nbr_mask_parts


if __name__ == "__main__":
    result = get_mask_card_number("7000792289606361")
    print(result)


# "7000792289606361"
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def get_mask_account(acc_nmbr: str) -> str:
    """Функция принимает строку с номером счёта в банке, маскирует цифры под звёздочками
    возвращает 2 звёздочки и последние 4 цифры номера счёта.
    :rtype: str
    """
    masks_logger.info(f"Чтение введённого номера СЧЁТА: {acc_nmbr}")
    nmbr_str = str(acc_nmbr)

    if nmbr_str == "":
        masks_logger.error(
            f"Ошибка: Пустое значение -{acc_nmbr}- вводить недопустимо. \n"
            "Введите 20 цифр номера СЧЁТА БЕЗ пробелов."
        )
        raise ValueError("Пустое значение вводить недопустимо. " "Введите 20 цифр номера СЧЁТА БЕЗ пробелов.")
    if nmbr_str.isspace():
        masks_logger.error(f"Ошибка: Нельзя вводить только пробел -{acc_nmbr}-")
        raise ValueError("Нельзя вводить только пробел")
    if not nmbr_str.isdigit():
        masks_logger.error(
            f"Ввод номеров СЧЁТА или КАРТЫ необходимо производить раздельно от букв: \n"
            "сначала слова - и через пробел - номер (16 или 20 цифр)!"
        )
        raise ValueError(
            f"Ввод номеров СЧЁТА или КАРТЫ необходимо производить раздельно от букв: \n"
            "сначала слова - и через пробел - номер (16 или 20 цифр)!"
        )
    # эта строка текста ошибки - для работы функции mask_account_card в модуле widget.py
    if len(nmbr_str) != 20:
        masks_logger.error(
            f"Не верное количество введённых цифр номера. \n"
            "Номер СЧЁТА должен состоять из 20 цифр. \n"
            "Номер КАРТЫ должен состоять из 16 цифр."
        )
        raise ValueError(
            f"Не верное количество введённых цифр номера. \n"
            "Номер СЧЁТА должен состоять из 20 цифр. \n"
            "Номер КАРТЫ должен состоять из 16 цифр."
        )

    masks_logger.info(f"Маскировка введённого номера СЧЁТА: {acc_nmbr} - проведена успешно")

    masked_nmbr = "**" + nmbr_str[-4:]

    return masked_nmbr


# if __name__ == "__main__":
#     result = get_mask_account("73654108430135874305")
#     print(result)

# "73654108430135874305"
