import dataclasses

import pytest

from campusconnect.exceptions import InvalidAttendanceError
from campusconnect.models import AttendanceRecord, Faculty, Student


def test_student_str():
    assert str(Student(1, "Ravi", "MCA001")) == "Student #1: Ravi"


def test_equality_and_hash():
    a = Student(1, "Ravi", "MCA001")
    b = Student(1, "Ravi Kumar", "MCA001")
    assert a == b
    assert len({a, b}) == 1


def test_student_not_equal_to_faculty_with_same_id():
    assert Student(1, "A", "R1") != Faculty(1, "A", "Python")


def test_students_sort_by_roll_no():
    s1, s2 = Student(1, "A", "MCA002"), Student(2, "B", "MCA001")
    assert sorted([s1, s2]) == [s2, s1]


def test_attendance_record_is_frozen():
    r = AttendanceRecord(1, "Python", "2026-11-04", True)
    with pytest.raises(dataclasses.FrozenInstanceError):
        r.present = False


@pytest.mark.parametrize("bad_date", ["not-a-date", "2026-13-01", "04-11-2026", ""])
def test_bad_dates_rejected(bad_date):
    with pytest.raises(InvalidAttendanceError):
        AttendanceRecord(1, "Python", bad_date, True)
