class CampusConnectError(Exception):
    """Base class for all project errors."""


class StudentNotFoundError(CampusConnectError):
    pass


class DuplicateStudentError(CampusConnectError):
    pass


class InvalidAttendanceError(CampusConnectError):
    pass
