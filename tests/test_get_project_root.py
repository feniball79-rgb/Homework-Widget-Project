from pathlib import Path

from my_project.project_root_Path_finder import get_project_root


def test_get_project_root_finds_pyproject_toml(tmp_path: Path, monkeypatch):
    """Когда pyproject.toml есть в корне, функция возвращает путь к этой папке."""
    root = tmp_path
    (root / "pyproject.toml").touch()
    src = root / "src"
    src.mkdir()
    my_project = src / "my_project"
    my_project.mkdir()

    fake_file = my_project / "project_root_Path_finder.py"
    fake_file.touch()

    monkeypatch.setattr("my_project.project_root_Path_finder.__file__", str(fake_file))
    result = get_project_root()

    assert result == root
    assert (result / "pyproject.toml").exists()


def test_get_project_root_fallback_to_top_if_no_marker(tmp_path: Path, monkeypatch):
    """Если pyproject.toml нигде нет — функция доходит до корня ФС и возвращает его."""
    deep = tmp_path / "a" / "b" / "c" / "d"
    deep.mkdir(parents=True)

    fake_file = deep / "project_root_Path_finder.py"
    fake_file.touch()

    monkeypatch.setattr("my_project.project_root_Path_finder.__file__", str(fake_file))
    result = get_project_root()

    assert isinstance(result, Path)
    assert result.exists()


def test_get_project_root_works_from_different_depths(tmp_path: Path, monkeypatch):
    """Функция находит корень независимо от глубины вызова."""
    root = tmp_path
    (root / "pyproject.toml").touch()

    paths_to_test = [
        root,
        root / "src",
        root / "src" / "my_project",
        root / "src" / "my_project" / "utils",
        root / "data",
        root / "tests",
    ]

    for p in paths_to_test:
        p.mkdir(parents=True, exist_ok=True)
        fake_file = p / "project_root_Path_finder.py"
        fake_file.touch()

        monkeypatch.setattr("my_project.project_root_Path_finder.__file__", str(fake_file))
        result = get_project_root()

        assert result == root, f"Не найден корень при вызове из {p}"


def test_get_project_root_finds_nearest_pyproject(tmp_path: Path, monkeypatch):
    """Если pyproject.toml есть на нескольких уровнях — возвращается ближайший."""
    root = tmp_path
    (root / "pyproject.toml").touch()
    sub = root / "sub"
    sub.mkdir()
    (sub / "pyproject.toml").touch()

    fake_file = sub / "project_root_Path_finder.py"
    fake_file.touch()

    monkeypatch.setattr("my_project.project_root_Path_finder.__file__", str(fake_file))
    result = get_project_root()

    assert result == sub
    assert (result / "pyproject.toml").exists()


def test_get_project_root_returns_valid_path_object(tmp_path: Path, monkeypatch):
    """Результат — существующий абсолютный объект Path."""
    root = tmp_path
    (root / "pyproject.toml").touch()

    fake_file = root / "src" / "my_project" / "project_root_Path_finder.py"
    fake_file.parent.mkdir(parents=True, exist_ok=True)
    fake_file.touch()

    monkeypatch.setattr("my_project.project_root_Path_finder.__file__", str(fake_file))
    result = get_project_root()

    assert isinstance(result, Path)
    assert result.exists()
    assert result.is_absolute()
