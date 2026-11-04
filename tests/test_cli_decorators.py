import logging

from campusconnect.cli import main
from campusconnect.decorators import log_call, timed


def test_cli_add_and_report(tmp_path, capsys):
    db = str(tmp_path / "c.db")
    assert main(["--db", db, "add-student", "Ravi", "R1"]) == 0
    assert main(["--db", db, "mark", "R1", "Python", "2026-11-01", "present"]) == 0
    assert main(["--db", db, "report", "R1"]) == 0
    out = capsys.readouterr().out
    assert "Ravi" in out
    assert "Python" in out


def test_cli_defaulters_and_top(tmp_path, capsys):
    db = str(tmp_path / "c.db")
    main(["--db", db, "add-student", "Ravi", "R1"])
    main(["--db", db, "mark", "R1", "Python", "2026-11-01", "absent"])
    assert main(["--db", db, "defaulters"]) == 0
    assert "Ravi" in capsys.readouterr().out
    assert main(["--db", db, "top", "--n", "1"]) == 0


def test_cli_no_defaulters(tmp_path, capsys):
    db = str(tmp_path / "c.db")
    assert main(["--db", db, "defaulters"]) == 0
    assert "No defaulters" in capsys.readouterr().out


def test_cli_error_returns_1(tmp_path, capsys):
    db = str(tmp_path / "c.db")
    assert main(["--db", db, "report", "NOPE"]) == 1
    assert "Error" in capsys.readouterr().err


def test_cli_import_commands(tmp_path, capsys):
    db = str(tmp_path / "c.db")
    s = tmp_path / "s.csv"
    s.write_text("name,roll_no\nA,R1\n")
    a = tmp_path / "a.csv"
    a.write_text("roll_no,subject,date,present\nR1,Python,2026-11-01,yes\n")
    assert main(["--db", db, "import-students", str(s)]) == 0
    assert main(["--db", db, "import-attendance", str(a)]) == 0


def test_decorators_keep_name_and_log(caplog):
    @log_call
    @timed
    def add(a, b):
        return a + b

    with caplog.at_level(logging.INFO, logger="campusconnect"):
        assert add(2, 3) == 5
    assert add.__name__ == "add"
    assert "add took" in caplog.text
