# CampusConnect

![CI](https://github.com/Aditya050504/campusconnect/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Student Attendance & Performance Tracker**: a command-line tool that stores
attendance in SQLite, imports CSV/JSON data, detects attendance shortage and
ranks students.

## Features

- Add students and mark attendance from the command line
- Bulk import from CSV / JSON (lazy generators for large files)
- Defaulter detection (default limit 75%)
- Top-N students and subject-wise reports with grades
- Custom exceptions with clean error messages

## Installation

    pip install -e .

## Usage

    campusconnect add-student "Ravi Kumar" MCA001
    campusconnect import-attendance attendance.csv
    campusconnect defaulters --limit 75
    campusconnect top --n 3
    campusconnect report MCA001

## Project structure

    src/campusconnect/
      models.py        classes, ABC, dataclass
      repository.py    sqlite3 + context manager
      analytics.py     percentage, defaulters, ranking, closure
      importers.py     CSV/JSON generators
      decorators.py    @timed, @log_call
      cli.py           argparse commands
    tests/             pytest suite

## Run tests

    pip install pytest pytest-cov
    pytest --cov=campusconnect

## License

MIT
