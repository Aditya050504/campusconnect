import csv
import json
from pathlib import Path
from typing import Dict, Iterator

from .exceptions import InvalidAttendanceError
from .models import AttendanceRecord
from .repository import Repository


def read_csv_rows(path: str) -> Iterator[Dict[str, str]]:
    """Generator: yields one CSV row (dict) at a time."""
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            yield row


def read_json_rows(path: str) -> Iterator[Dict]:
    """Generator: yields one item from a JSON list at a time."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    yield from data


def import_students(repo: Repository, path: str) -> int:
    """Import students from .csv or .json. Returns how many were added."""
    suffix = Path(path).suffix.lower()
    if suffix == ".csv":
        rows = read_csv_rows(path)
    elif suffix == ".json":
        rows = read_json_rows(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    count = 0
    for row in rows:
        repo.add_student(row["name"], row["roll_no"], row.get("course", "MCA"))
        count += 1
    return count


def import_attendance(repo: Repository, path: str) -> int:
    """Import attendance from CSV with columns: roll_no, subject, date, present."""
    count = 0
    for row in read_csv_rows(path):
        student = repo.get_student(row["roll_no"])
        present = row["present"].strip().lower() in ("1", "true", "yes", "p")
        try:
            record = AttendanceRecord(
                student.person_id, row["subject"], row["date"], present
            )
        except InvalidAttendanceError:
            continue  # skip rows with bad dates
        repo.add_attendance(record)
        count += 1
    return count
