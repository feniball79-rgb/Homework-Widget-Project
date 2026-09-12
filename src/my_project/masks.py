def get_mask_card_number(card_number: str) -> str:
    """Функция принимает номер карты клиента банка и маскирует часть цифр под звёздочками.
    Выводит замаскированный номер в формате ХХХХ ХХ** **** ХХХХ.
    :rtype: str
    """
    card_num = str(card_number)
    if card_num == "":
        raise ValueError("Нельзя вводить пустые значения")
    if not str(card_num).isdigit():
        raise ValueError("Номар карты должен состоять ТОЛЬКО из цифры")
    if len(str(card_num)) != 16:
        raise ValueError("Номер карты должен содержать ровно 16 символов")

    nbr_mask = str(card_num)[0:6] + "******" + str(card_num)[-4:]
    nbr_mask_parts = nbr_mask[:4] + " " + nbr_mask[4:8] + " " + nbr_mask[8:12] + " " + nbr_mask[12:]

    return nbr_mask_parts


if __name__ == "__main__":

    result = get_mask_card_number("7000792289606361")
    print(result)


def get_mask_account(acc_nmbr: str) -> str:
    """Функция принимает строку с нимером счёта в банке, маскирует цифры под звёздочками
    возвращает 2 звёздочки и последние 4 цифры номера счёта.
    """
    nmbr_str = str(acc_nmbr)

    if nmbr_str == "":
        raise ValueError("Пустое значение вводить недопустимо. " "Введите 20 цифр номера счёта БЕЗ пробелов.")
    if nmbr_str.isspace():
        raise ValueError("Нельзя вводить только пробел")
    if not nmbr_str.isdigit():
        raise ValueError(
            "Ввод номеров счёта или карты необходимо производить раздельно от букв: "
            "сначала слова - и через пробел - номер (16 или 20 цифр)!"
        )  # эта строка для работы mask_account_card
    if len(nmbr_str) != 20:
        raise ValueError(
            "Не верное количество введённых цифр номера. "
            "Номер счёта должен состоять из 20 цифр. "
            "Номер карты должен состоять из 16 цифр."
        )

    masked_nmbr = "**" + nmbr_str[-4:]

    return masked_nmbr


if __name__ == "__main__":

    result = get_mask_account("73654108430135874305")
    print(result)


# "73654108430135874305"
