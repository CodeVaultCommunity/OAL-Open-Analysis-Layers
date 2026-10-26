"""Errors raised by the core without choosing an interface representation."""


class WorkBoardError(Exception):
    code = "work_board_error"


class AuthenticationRequired(WorkBoardError):
    code = "authentication_required"


class AccessDenied(WorkBoardError):
    code = "access_denied"


class Invalid(WorkBoardError):
    code = "invalid"


class Missing(WorkBoardError):
    code = "not_found"


class Conflict(WorkBoardError):
    code = "conflict"


class Unavailable(WorkBoardError):
    """Storage could not confirm success; the write outcome is explicit."""

    code = "unavailable"

    def __init__(self, message="storage unavailable; reload before retrying", *,
                 write_outcome="unknown"):
        super().__init__(message)
        self.write_outcome = write_outcome
