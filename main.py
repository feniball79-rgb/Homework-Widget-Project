from typing import Any

import pandas as pd

from my_project.df_readers import get_transactions_csv, get_transactions_xlsx
from my_project.generators import filter_by_currency
from my_project.processing import filter_by_state, sort_by_date
from my_project.search_engines import process_bank_search
from my_project.utils import convert_json_to_python
from my_project.widget import get_date, mask_account_card

# """type Transaction = dict[str, Any] # — это именованный псевдоним вместо list[dict[str, Any]]"""

# Псевдонимы для стыков конвейера
type Transaction = dict[str, Any]  # Для типизации по новому обновлению в Python 3.12.10
# JSON-путь даёт список словарей, CSV/XLSX — DataFrame
type Data = list[Transaction] | pd.DataFrame  # Для типизации по новому обновлению в Python 3.12.10


def main() -> None:
    """Реализует основную логику пользовательского виджета банка"""

    print(
        "Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n"
        "Выберите необходимый пункт меню:\n"
        "1. Получить информацию о транзакциях из JSON-файла\n"
        "2. Получить информацию о транзакциях из CSV-файла\n"
        "3. Получить информацию о транзакциях из XLSX-файла"
    )

    read_file: Data  # Типизация # декларация: «здесь будет Data»

    while True:
        file_format = input("Ваш выбор: ")
        if file_format == "1":
            print("Для обработки выбран - JSON-файл.")
            read_file = convert_json_to_python("operations.json")
            break
        elif file_format == "2":
            print("Для обработки выбран - CSV-файл.")
            read_file = get_transactions_csv("transactions.csv", delimiter=";")
            break
        elif file_format == "3":
            print("Для обработки выбран - XLSX-файл.")
            read_file = get_transactions_xlsx("transactions_excel.xlsx")
            break
        else:
            print("Не верный ввод.\n" "Попробуйте заново.")

    def main_filter_by_state() -> Data:
        """Фильтрует операции по статусу"""

        while True:
            print(
                "\nВведите статус, по которому необходимо выполнить фильтрацию. \n"
                "Доступные для фильтровки статусы: \n"
                "EXECUTED, CANCELED, PENDING"
            )

            status_word = input().upper()
            ALLOWED_STATES = {"EXECUTED", "CANCELED", "PENDING"}

            if status_word in ALLOWED_STATES:

                filtered_file_by_status = filter_by_state(read_file, status_word)
                if filtered_file_by_status:
                    print(f"Операции отфильтрованы по статусу - {status_word}")
                    return filtered_file_by_status

                else:
                    print(
                        f"\nВ этом отчёте статус -> {status_word} <- отсутствует. \n"
                        f"Выберите другой статус, кроме - {status_word}."
                    )
                    continue

            else:
                print(f"\nСтатус операции - {status_word} - недоступен.")

    # Вызов и определение типизации вывода в новом формате.
    filtered_state: Data = main_filter_by_state()  # Перезаписываем данные в псевдоним Data.
    # filtered_state = main_filter_by_state() # - старое выражение.
    # print(filtered_state)

    def main_sort_by_date() -> Data:  # Для типизации по-новому. Применяем Data с новыми данными.
        """Сортирует транзакции по дате"""
        while True:
            answer_by_date = input("\nОтсортировать операции по дате? Да/Нет -> ").upper()
            if answer_by_date in ("ДА", "НЕТ"):
                break
            print("\nНе верный ввод. Попробуйте заново.")

        if file_format == "1":
            if answer_by_date == "ДА":
                while True:
                    answer_choice = input("Отсортировать по возрастанию ( 1 ) или по убыванию ( 2 ) ? -> ")
                    if answer_choice in ("1", "2"):
                        break
                    print("\nНе верный ввод. Нужно 1 или 2.")
                return sort_by_date(filtered_state, descending=(answer_choice == "2"))
            return filtered_state
        else:
            # CSV/XLSX: всегда вернётся DataFrame, сортировка — только если попросили
            df = pd.DataFrame(filtered_state)
            if answer_by_date == "ДА":
                while True:
                    answer_choice = input("Отсортировать по возрастанию ( 1 ) или по убыванию ( 2 ) ? -> ")
                    if answer_choice in ("1", "2"):
                        break
                    print("\nНе верный ввод. Нужно 1 или 2.")
                return df.sort_values(by="date", ascending=(answer_choice == "1"), kind="stable", na_position="last")
            return df

    sorted_by_date: Data = main_sort_by_date()  # Типизация и вызов new
    # sorted_by_date = main_sort_by_date()
    # print(sorted_by_date)

    def main_filter_by_currency() -> Data:
        """Фильтрует по коду валюты"""
        while True:
            answer_currency = input("\nВыводить только рублевые транзакции? Да/Нет -> ").upper()
            if answer_currency in ("ДА", "НЕТ"):
                break
            print("\nНеверный ввод. Нужно: Да или Нет.")

        if file_format == "1":

            if answer_currency == "ДА":
                curr_transactions = filter_by_currency(sorted_by_date, "RUB")
            else:
                return sorted_by_date

            return list(curr_transactions)

        else:
            assert isinstance(sorted_by_date, pd.DataFrame)  # <-не заглушка «для галочки», а настоящая защита от ->
            # -> неожидаемых форматов - Программа упадёт с внятной ошибкой на месте проблемы, а не с .loc-глюком

            if answer_currency == "ДА":
                curr_transactions = sorted_by_date.loc[sorted_by_date.currency_code.isin(["RUB"])]
            else:
                curr_transactions = sorted_by_date

        return curr_transactions

    filtered_by_currency: Data = main_filter_by_currency()  # Типизация и вызов *new
    # filtered_by_currency = main_filter_by_currency()
    # print(filtered_by_currency)

    def main_transaction_descriptions() -> Data | None:
        """Фильтрует по описанию операции в ячейке description"""
        while True:
            answer_description = input(
                "\nОтфильтровать список транзакций по определенному слову в описании?\n" "Да/Нет -> "
            ).upper()

            if answer_description in ("ДА", "НЕТ"):
                if answer_description == "ДА":
                    break
                else:
                    return filtered_by_currency
            print("\nОтвет не верный. Попробуйте ответить: Да или Нет.")

        # Шаблон допустимых ответов
        ALLOWED_WORDS = {
            "открытие вклада",
            "перевод организации",
            "перевод с карты на карту",
            "перевод со счета на счет",
        }

        while True:
            choice_description = input(
                "\nВведите слово для фильтрации по нему:\n"
                "Открытие вклада          - \n"
                "Перевод организации      - \n"
                "Перевод с карты на карту - \n"
                "Перевод со счета на счет - \n"
                "Ваш выбор -> "
            ).lower()

            if choice_description in ALLOWED_WORDS:
                break
            print("\nТакого слова нет в списке. Попробуйте ещё...")
            continue

        if file_format == "1":
            if answer_description == "ДА":
                filtered_descriptions = process_bank_search(filtered_by_currency, choice_description)

                if filtered_descriptions:
                    print("\nПрограмма завершила фильтрацию.\n")
                    return filtered_descriptions

            elif answer_description == "НЕТ":
                return filtered_by_currency

            else:
                print("\nНе найдено ни одной транзакции, подходящей под ваши условия фильтрации.")

        elif file_format in ("2", "3"):
            assert isinstance(filtered_by_currency, pd.DataFrame)  # <- не заглушка «для галочки», а настоящая защита:
            if answer_description == "ДА":
                filtered_descriptions = filtered_by_currency.loc[
                    filtered_by_currency.description.str.lower() == choice_description
                ]
                print("\nПрограмма завершила фильтрацию.\n")
                return filtered_descriptions
            else:
                return filtered_by_currency

        return None

    filtered_by_descriptions: Data | None = main_transaction_descriptions()  # Типизация и вызов. *new
    # filtered_by_descriptions = main_transaction_descriptions()  # old.

    if isinstance(filtered_by_descriptions, pd.DataFrame):

        # Приказывает печатать DataFrame развёрнутыми таблицами - глобально.
        pd.set_option("display.max_columns", None)
        pd.set_option("display.width", 160)
    # else:
    #     for t in filtered_by_descriptions:       # <- для JSON, если понадобится.
    #         print(t)
    #         print(type(t))
    # print(filtered_by_descriptions)
    # print(type(filtered_by_descriptions))

    while True:
        answer = input("\nРаспечатать итоговый список транзакций? Да/Нет -> ").upper()
        if answer == "ДА":
            break
        if answer == "НЕТ":
            print("\nПоказ пропущен по вашему желанию.")
            break
        print("\nНе верный ввод. Нужно Да или Нет.")

    def parsing_filtered_data() -> str | None:
        """Формирует и выводит в удобный формат обработанных данных для ответа пользователю."""

        if filtered_by_descriptions is None:
            print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")
            return None

        if file_format == "1":
            """Для JSON"""

            lines = []

            for pars in filtered_by_descriptions:
                date = pars.get("date", {})
                description = pars.get("description", {})
                amount = pars.get("operationAmount", {}).get("amount", {})
                currency = pars.get("operationAmount", {}).get("currency", {}).get("name", {})
                from_ = pars.get("from", "")
                to_ = pars.get("to", "")

                # Отсекаем возможную ошибку = пустого ввода "" в функцию mask_account_card
                if from_:
                    accounts_line = f"{mask_account_card(from_)} -> {mask_account_card(to_)}"
                else:
                    accounts_line = mask_account_card(to_)

                # Формируем вывод
                lines.append(f"{get_date(date)} {description}\n" f"{accounts_line}\n" f"Сумма: {amount} {currency}")

            print(f"\nВсего банковских операций в выборке:{len(lines)}\n\n")

            if lines:
                return "\n\n".join(lines)  # пустая строка между записями, при выводе сообщений пользователю приложения
            else:
                print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
                return None

                # """DataFrame"""

        else:
            assert isinstance(filtered_by_descriptions, pd.DataFrame)  # Защита от нежданных данных.
            lines = []
            # убирает (.0) при выводе amount
            filtered_by_descriptions["amount"] = filtered_by_descriptions["amount"].astype(str).str.removesuffix(".0")

            for pars in filtered_by_descriptions.to_dict(orient="records"):  # (to_dict) Перевод из DF в JSON
                date = pars.get("date", "")
                description = pars.get("description", "")
                amount = pars.get("amount", {})
                currency = pars.get("currency_code", {})
                from_ = pars.get("from", "")
                if pd.isna(from_):  # Проверка значений NaN. Если True, то заменяет на ""
                    from_ = ""
                to_ = pars.get("to", "")  # Проверка значений NaN. Если True, то заменяет на ""
                if pd.isna(to_):
                    to_ = ""

                # Отсекаем возможную ошибку -> пустого ввода "" -> в функцию mask_account_card
                if from_:
                    accounts_line = f"{mask_account_card(from_)} -> {mask_account_card(to_)}"
                else:
                    accounts_line = mask_account_card(to_)

                lines.append(f"{get_date(date)} {description}\n" f"{accounts_line}\n" f"Сумма: {amount} {currency}")

            print(f"\nВсего банковских операций в выборке:{len(lines)}\n\n")

            if lines:
                return "\n\n".join(lines)  # пустая строка между записями
            else:
                print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
                return None

    # result = parsing_filtered_data() # old
    result: str | None = parsing_filtered_data()  # *new
    print(result)


if __name__ == "__main__":
    main()
