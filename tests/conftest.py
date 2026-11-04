import pytest

from campusconnect.models import AttendanceRecord
from campusconnect.repository import Repository


@pytest.fixture
def repo(tmp_path):
    """Fresh empty database for every test."""
    return Repository(str(tmp_path / "test.db"))


@pytest.fixture
def filled_repo(repo):
    """Database with 3 students and 4 days of attendance."""
    data = {
        "MCA001": ("Ravi Kumar", [True, True, True, True]),
        "MCA002": ("Sneha Reddy", [True, False, False, False]),
        "MCA003": ("Arjun Rao", [True, True, True, False]),
    }
    for roll, (name, days) in data.items():
        sid = repo.add_student(name, roll)
        for i, present in enumerate(days, start=1):
            repo.add_attendance(
                AttendanceRecord(sid, "Python", f"2026-11-0{i}", present)
            )
    return repo
