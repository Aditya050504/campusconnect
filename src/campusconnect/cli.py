import argparse
import logging
import sys
from typing import List, Optional

from .analytics import (
    attendance_percentage,
    find_defaulters,
    make_grader,
    subject_wise_percentage,
    top_students,
)
from .exceptions import CampusConnectError
from .importers import import_attendance, import_students
from .models import AttendanceRecord
from .repository import Repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="campusconnect",
        description="Student Attendance & Performance Tracker",
    )
    parser.add_argument("--db", default="campusconnect.db", help="database file path")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show log messages"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add-student", help="add one student")
    p.add_argument("name")
    p.add_argument("roll_no")
    p.add_argument("--course", default="MCA")

    p = sub.add_parser("import-students", help="import students from CSV/JSON")
    p.add_argument("path")

    p = sub.add_parser("import-attendance", help="import attendance from CSV")
    p.add_argument("path")

    p = sub.add_parser("mark", help="mark attendance for one student")
    p.add_argument("roll_no")
    p.add_argument("subject")
    p.add_argument("date", help="YYYY-MM-DD")
    p.add_argument("status", choices=["present", "absent"])

    p = sub.add_parser("defaulters", help="students below attendance limit")
    p.add_argument("--limit", type=float, default=75.0)

    p = sub.add_parser("top", help="top students by attendance")
    p.add_argument("--n", type=int, default=3)

    p = sub.add_parser("report", help="report of one student")
    p.add_argument("roll_no")

    return parser


def run(args: argparse.Namespace) -> None:
    repo = Repository(args.db)

    if args.command == "add-student":
        sid = repo.add_student(args.name, args.roll_no, args.course)
        print(f"Added student #{sid}: {args.name} ({args.roll_no})")

    elif args.command == "import-students":
        print(f"Imported {import_students(repo, args.path)} students.")

    elif args.command == "import-attendance":
        print(f"Imported {import_attendance(repo, args.path)} attendance records.")

    elif args.command == "mark":
        student = repo.get_student(args.roll_no)
        record = AttendanceRecord(
            student.person_id, args.subject, args.date, args.status == "present"
        )
        repo.add_attendance(record)
        print(f"Marked {student.name} {args.status} for {args.subject} on {args.date}")

    elif args.command == "defaulters":
        rows = find_defaulters(repo, args.limit)
        if not rows:
            print("No defaulters. Everyone is above the limit.")
        for student, pct in rows:
            print(f"{student.roll_no}  {student.name:<15} {pct:>6}%")

    elif args.command == "top":
        for rank, (student, pct) in enumerate(top_students(repo, args.n), start=1):
            print(f"{rank}. {student.name:<15} {pct:>6}%")

    elif args.command == "report":
        student = repo.get_student(args.roll_no)
        records = repo.attendance_for(student.person_id)
        grade = make_grader(90, 75)
        print(student)
        for subject, pct in subject_wise_percentage(records).items():
            print(f"  {subject:<12} {pct:>6}%  {grade(pct)}")
        overall = attendance_percentage(records)
        print(f"  Overall      {overall:>6}%  {grade(overall)}")


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s | %(message)s",
    )
    try:
        run(args)
    except CampusConnectError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
