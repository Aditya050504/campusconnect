from unittest.mock import MagicMock

import pytest

from campusconnect.analytics import (
    attendance_percentage,
    find_defaulters,
    make_grader,
    subject_wise_percentage,
    top_students,
)
from campusconnect.models import AttendanceRecord, Student


def rec(present, subject="Python"):
    return AttendanceRecord(1, subject, "2026-11-01", present)


@pytest.mark.parametrize(
    "flags, expected",
    [
        ([], 0.0),
        ([True, True, True, True], 100.0),
        ([True, True, True, False], 75.0),
        ([True, False, False], 33.33),
        ([False, False], 0.0),
    ],
)
def test_attendance_percentage(flags, expected):
    assert attendance_percentage([rec(f) for f in flags]) == expected


def test_subject_wise_percentage():
    records = [rec(True, "Python"), rec(False, "Python"), rec(True, "Java")]
    assert subject_wise_percentage(records) == {"Python": 50.0, "Java": 100.0}


@pytest.mark.parametrize(
    "pct, expected",
    [
        (100, "A"),
        (90, "A"),
        (89.9, "B"),
        (75, "B"),
        (74.9, "Shortage"),
        (0, "Shortage"),
    ],
)
def test_grader_closure(pct, expected):
    assert make_grader(90, 75)(pct) == expected


def test_find_defaulters(filled_repo):
    result = find_defaulters(filled_repo)
    assert [(s.name, pct) for s, pct in result] == [("Sneha Reddy", 25.0)]


def test_top_students(filled_repo):
    result = top_students(filled_repo, 2)
    assert [s.name for s, _ in result] == ["Ravi Kumar", "Arjun Rao"]


def test_find_defaulters_with_mock():
    """Mock: database ki jagah nakli repo, koi real DB nahi chahiye."""
    repo = MagicMock()
    s1, s2 = Student(1, "A", "R1"), Student(2, "B", "R2")
    repo.list_students.return_value = [s1, s2]
    repo.attendance_for.side_effect = lambda sid: {
        1: [rec(True)],
        2: [rec(False)],
    }[sid]

    result = find_defaulters(repo)

    assert [s.name for s, _ in result] == ["B"]
    assert repo.attendance_for.call_count == 2
