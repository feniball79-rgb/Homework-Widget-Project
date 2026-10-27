from my_project.search_engines import process_bank_operations, process_bank_search


def test_finds_substring_in_description():
    data = [{"id": 1, "description": "Перевод организации"}, {"id": 2, "description": "Открытие вклада"}]
    assert process_bank_search(data, "организации") == [{"id": 1, "description": "Перевод организации"}]


def test_case_insensitive():
    data = [{"description": "Перевод организации"}]
    assert process_bank_search(data, "перевод") == data


def test_no_match_returns_empty_list():
    data = [{"description": "Открытие вклада"}]
    assert process_bank_search(data, "перевод") == []


def test_part_of_word():
    data = [{"description": "Перевод со счета на счет"}]
    assert process_bank_search(data, "счета") == data


def test_special_characters_are_escaped():
    data = [{"description": "Комиссия 5%"}]
    assert process_bank_search(data, "5%") == data


def test_missing_description_does_not_break():
    data = [{"id": 1}, {"description": "Перевод организации"}]
    assert process_bank_search(data, "перевод") == [{"description": "Перевод организации"}]


# **************************************************************************


def test_counts_categories():
    data = [
        {"description": "Перевод организации"},
        {"description": "Перевод организации"},
        {"description": "Открытие вклада"},
    ]
    assert process_bank_operations(data, ["Перевод организации", "Открытие вклада"]) == {
        "Перевод организации": 2,
        "Открытие вклада": 1,
    }


def test_category_not_found_gives_zero_or_absent():
    data = [{"description": "Перевод организации"}]
    result = process_bank_operations(data, ["Перевод организации", "Вклад"])
    assert result["Перевод организации"] == 1
    assert "Вклад" not in result  # категория без совпадений не попадает в словарь


def test_case_insensitive_():
    data = [{"description": "перевод организации"}]
    assert process_bank_operations(data, ["Перевод организации"]) == {"Перевод организации": 1}


def test_operation_without_description():
    data = [{"id": 1}, {"description": "Открытие вклада"}]
    assert process_bank_operations(data, ["Открытие вклада"]) == {"Открытие вклада": 1}
