import sqlite3
from contextlib import contextmanager
from typing import Iterator, List

from .exceptions import DuplicateStudentError, StudentNotFoundError
from .models import AttendanceRecord, Student


class Repository:
    def __init__(self, db_path: str = "campusconnect.db"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    roll_no TEXT NOT NULL UNIQUE,
                    course TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    subject TEXT NOT NULL,
                    on_date TEXT NOT NULL,
                    present INTEGER NOT NULL,
                    FOREIGN KEY (student_id) REFERENCES students(id)
                );
            """)

    def add_student(self, name: str, roll_no: str, course: str = "MCA") -> int:
        try:
            with self._connect() as conn:
                cur = conn.execute(
                    "INSERT INTO students (name, roll_no, course) VALUES (?, ?, ?)",
                    (name, roll_no, course),
                )
                assert cur.lastrowid is not None
                return cur.lastrowid
        except sqlite3.IntegrityError as exc:
            raise DuplicateStudentError(f"Roll no {roll_no} already exists") from exc

    def get_student(self, roll_no: str) -> Student:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM students WHERE roll_no = ?", (roll_no,)
            ).fetchone()
        if row is None:
            raise StudentNotFoundError(f"No student with roll no {roll_no}")
        return Student(row["id"], row["name"], row["roll_no"], row["course"])

    def list_students(self) -> List[Student]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM students").fetchall()
        return [Student(r["id"], r["name"], r["roll_no"], r["course"]) for r in rows]

    def add_attendance(self, record: AttendanceRecord) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO attendance (student_id, subject, on_date, present) "
                "VALUES (?, ?, ?, ?)",
                (
                    record.student_id,
                    record.subject,
                    record.on_date,
                    int(record.present),
                ),
            )

    def attendance_for(self, student_id: int) -> List[AttendanceRecord]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM attendance WHERE student_id = ?", (student_id,)
            ).fetchall()
        return [
            AttendanceRecord(
                r["student_id"], r["subject"], r["on_date"], bool(r["present"])
            )
            for r in rows
        ]
