import sys
from skim.cli import resolve_types, DISPLAY_LABELS


def test_resolve_types_all():
    assert resolve_types(["all"]) == ["story", "deep"]


def test_resolve_types_single():
    assert resolve_types(["story"]) == ["story"]


def test_resolve_types_multiple():
    assert resolve_types(["story", "deep"]) == ["story", "deep"]


def test_resolve_types_all_overrides():
    assert resolve_types(["story", "all"]) == ["story", "deep"]


def test_resolve_types_dedup():
    assert resolve_types(["story", "story"]) == ["story"]


def test_display_labels():
    assert DISPLAY_LABELS["story"] == "STORY"
    assert DISPLAY_LABELS["deep"] == "DEEP DIVE"


def test_main_version(capsys):
    import pytest
    from skim.cli import main

    with pytest.raises(SystemExit, match="0"):
        sys.argv = ["skim", "--version"]
        main()
    captured = capsys.readouterr()
    assert "0.5.0" in captured.out


def test_main_no_args(capsys):
    import pytest
    from skim.cli import main

    with pytest.raises(SystemExit):
        sys.argv = ["skim"]
        main()


def test_main_init_dispatches(monkeypatch):
    from unittest.mock import patch
    from skim.cli import main

    monkeypatch.setattr("sys.argv", ["skim", "init"])
    with patch("skim.cli.run_init") as mock_init:
        main()
    mock_init.assert_called_once()
