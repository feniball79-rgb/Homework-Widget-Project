from typing import Any, Dict, List, Optional

import pytest

from my_project.processing import filter_by_state


@pytest.fixture
def fixt(state_mode="EXECUTED") -> List[Dict[str, Any]]:

    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_filter_by_state(fixt: List[Dict[str, Any]]) -> None:
    result = filter_by_state(fixt, state_mode="CANCELED")
    expected = [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    assert result == expected


def test_filter_by_state_2(fixt: List[Dict[str, Any]]) -> None:
    resultat = filter_by_state(fixt, state_mode="EXECUTED")
    expecteds = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    assert resultat == expecteds


def test_filter_by_state_empty_lst(fixt) -> None:
    with pytest.raises(ValueError):
        filter_by_state([])


def test_filter_by_state_state_is_wrong(fixt: str) -> None:
    with pytest.raises(ValueError):
        filter_by_state(fixt, state_mode="BUBBLED")
