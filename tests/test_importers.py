import json

import pytest

from campusconnect.importers import (
    import_attendance,
    import_students,
    read_csv_rows,
)


def test_read_csv_rows_is_generator(tmp_path):
    f = tmp_path / "s.csv"
    f.write_text("name,roll_no\nA,R1\nB,R2\n")
    gen = read_csv_rows(str(f))
    assert next(gen)["name"] == "A"
    assert next(gen)["name"] == "B"


def test_import_students_csv(repo, tmp_path):
    f = tmp_path / "s.csv"
    f.write_text("name,roll_no,course\nA,R1,MCA\nB,R2,MCA\n")
    assert import_students(repo, str(f)) == 2
    assert repo.get_student("R1").name == "A"


def test_import_students_json(repo, tmp_path):
    f = tmp_path / "s.json"
    f.write_text(json.dumps([{"name": "A", "roll_no": "R1"}]))
    assert import_students(repo, str(f)) == 1


def test_import_students_bad_type(repo, tmp_path):
    f = tmp_path / "s.txt"
    f.write_text("x")
    with pytest.raises(ValueError):
        import_students(repo, str(f))


def test_import_attendance_skips_bad_dates(repo, tmp_path):
    repo.add_student("A", "R1")
    f = tmp_path / "a.csv"
    f.write_text(
        "roll_no,subject,date,present\n"
        "R1,Python,2026-11-01,yes\n"
        "R1,Python,bad-date,yes\n"
        "R1,Python,2026-11-02,no\n"
    )
    assert import_attendance(repo, str(f)) == 2
