from my_project.masks import get_mask_account, get_mask_card_number


def mask_account_card(data_receiver: str) -> str:
    """Функция принимает строку с названием карты и номером карты и маскирует номер,
    либо название счёта и номер счёта и маскирует номер
    """
    if data_receiver == "":
        raise ValueError("Нельзя вводить пустые значения")
    if data_receiver.isspace():
        raise ValueError("Слова и номер должны быть разделены пробелом")

    spaces_count = 0
    for dat in data_receiver:
        if dat == " ":
            spaces_count += 1
        elif spaces_count > 2:
            raise ValueError("Нельзя вводить более двух слов и одного номера")

    """
    Строку переводим в список, чтобы отделить слова от номера по индексу.
    После этого приводим разделённый список в строки.
    """
    dat_lst = data_receiver.split(" ")
    nomer = dat_lst[-1]
    pay_system_lst = dat_lst[:-1]
    pay_system_str = " ".join(pay_system_lst)

    """
    Автоматический выбор нужного для работы модуля из двух импортированных.
    """
    if len(nomer) == 16:
        return f"{pay_system_str} {get_mask_card_number(f"{nomer}")}"
    else:
        return f"{pay_system_str} {get_mask_account(f"{nomer}")}"


if __name__ == "__main__":

    result = mask_account_card("Счет 7365410843013582")
    print(result)

# Счет 73654108430135874305
# Visa Platinum 7000792289606361
# Maestro 1596837868705199
# Счет 64686473678894779589
# MasterCard 7158300734726758
# Счет 35383033474447895560
# Visa Classic 6831982476737658
# Visa Platinum 8990922113665229
# Visa Gold 5999414228426353
# Счет 73654108430135874305


from datetime import datetime


def get_date(date_string: str) -> str:
    """
    Преобразует строку с датой из формата ISO
    в формат ДД.ММ.ГГГГ

    Args:
        date_string (str): Дата в формате "2024-03-11T02:26:18.671407"

    Returns:
        str: Дата в формате "11.03.2024"
    """
    # Парсим строку в объект datetime
    date_obj = datetime.fromisoformat(date_string)

    # Форматируем в нужный формат
    return date_obj.strftime("%d.%m.%Y")


print(get_date("2024-03-11T02:26:18.67140"))
