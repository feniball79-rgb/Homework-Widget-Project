import json
from pathlib import Path
from unittest.mock import mock_open, patch

from my_project.utils import convert_json_to_python


def test_convert_json_to_python_success():
    mock_data = [{"id": 1, "amount": 100.0}, {"id": 2, "amount": 200.5}]
    mock_json_str = json.dumps(mock_data)

    # mock_open правильно реализует __enter__/__exit__ и read()
    m = mock_open(read_data=mock_json_str)

    with patch("my_project.utils.open", m) as mock_open_func:
        with patch("my_project.utils.get_project_root") as mock_get_root:
            mock_get_root.return_value = Path("/fake/path")

            result = convert_json_to_python("operations.json")

            assert result == mock_data

            expected_path = Path("/fake/path/data/operations.json")
            mock_open_func.assert_called_once_with(expected_path, encoding="utf-8")


def test_convert_json_to_python_file_not_found():
    with patch("my_project.utils.get_project_root") as mock_get_root:
        mock_get_root.return_value = Path("/fake/path")

        with patch("my_project.utils.open", side_effect=FileNotFoundError):
            result = convert_json_to_python("nonexistent.json")
            assert result == []


def test_convert_json_to_python_invalid_json():
    m = mock_open(read_data="{ invalid json }")

    with patch("my_project.utils.open", m):
        with patch("my_project.utils.get_project_root") as mock_get_root:
            mock_get_root.return_value = Path("/fake/path")

            result = convert_json_to_python("bad.json")
            assert result == []
