import pytest

from campusconnect.exceptions import DuplicateStudentError, StudentNotFoundError
from campusconnect.models import AttendanceRecord


def test_add_and_get_student(repo):
    repo.add_student("Ravi", "MCA001")
    assert repo.get_student("MCA001").name == "Ravi"


def test_duplicate_roll_no(repo):
    repo.add_student("Ravi", "MCA001")
    with pytest.raises(DuplicateStudentError):
        repo.add_student("Other", "MCA001")


def test_missing_student(repo):
    with pytest.raises(StudentNotFoundError):
        repo.get_student("NOPE")


def test_attendance_saved(repo):
    sid = repo.add_student("Ravi", "MCA001")
    repo.add_attendance(AttendanceRecord(sid, "Python", "2026-11-04", True))
    records = repo.attendance_for(sid)
    assert len(records) == 1
    assert records[0].present is True
