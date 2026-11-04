from collections import defaultdict
from typing import Callable, Dict, List, Tuple

from .models import AttendanceRecord, Student
from .repository import Repository

SHORTAGE_LIMIT = 75.0


def attendance_percentage(records: List[AttendanceRecord]) -> float:
    """Return attendance % for a list of records (0 if empty)."""
    if not records:
        return 0.0
    present = sum(1 for r in records if r.present)
    return round(present * 100 / len(records), 2)


def subject_wise_percentage(records: List[AttendanceRecord]) -> Dict[str, float]:
    """Group records by subject and calculate % for each."""
    grouped = defaultdict(list)
    for r in records:
        grouped[r.subject].append(r)
    return {subject: attendance_percentage(recs) for subject, recs in grouped.items()}


def find_defaulters(
    repo: Repository, limit: float = SHORTAGE_LIMIT
) -> List[Tuple[Student, float]]:
    """Students whose overall attendance is below limit, lowest first."""
    result = []
    for student in repo.list_students():
        pct = attendance_percentage(repo.attendance_for(student.person_id))
        if pct < limit:
            result.append((student, pct))
    result.sort(key=lambda pair: pair[1])
    return result


def top_students(repo: Repository, n: int = 3) -> List[Tuple[Student, float]]:
    """Top-N students by overall attendance."""
    scored = [
        (s, attendance_percentage(repo.attendance_for(s.person_id)))
        for s in repo.list_students()
    ]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:n]


def make_grader(a_min: float, b_min: float) -> Callable[[float], str]:
    """Closure: returns a function that converts % into a grade."""

    def grade(pct: float) -> str:
        if pct >= a_min:
            return "A"
        if pct >= b_min:
            return "B"
        return "Shortage"

    return grade
