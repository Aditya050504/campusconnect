from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date

from .exceptions import InvalidAttendanceError


class Person(ABC):
    def __init__(self, person_id: int, name: str):
        self.person_id = person_id
        self.name = name

    @abstractmethod
    def role(self) -> str:
        """Return the role name (Student / Faculty)."""

    def __str__(self) -> str:
        return f"{self.role()} #{self.person_id}: {self.name}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self.person_id!r}, name={self.name!r})"

    def __eq__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return (type(self), self.person_id) == (type(other), other.person_id)

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.person_id))


class Student(Person):
    def __init__(self, person_id: int, name: str, roll_no: str, course: str = "MCA"):
        super().__init__(person_id, name)
        self.roll_no = roll_no
        self.course = course

    def role(self) -> str:
        return "Student"

    def __lt__(self, other: "Student") -> bool:
        return self.roll_no < other.roll_no


class Faculty(Person):
    def __init__(self, person_id: int, name: str, subject: str):
        super().__init__(person_id, name)
        self.subject = subject

    def role(self) -> str:
        return "Faculty"


@dataclass(frozen=True)
class AttendanceRecord:
    student_id: int
    subject: str
    on_date: str  # format: YYYY-MM-DD
    present: bool

    def __post_init__(self):
        try:
            date.fromisoformat(self.on_date)
        except ValueError as exc:
            raise InvalidAttendanceError(f"Bad date: {self.on_date}") from exc
