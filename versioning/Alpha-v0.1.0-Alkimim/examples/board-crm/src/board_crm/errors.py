"""Application errors; the transport maps them to HTTP responses."""

class CrmError(Exception):
    code = "crm_error"


class AuthenticationRequired(CrmError):
    code = "authentication_required"


class AccessDenied(CrmError):
    code = "access_denied"


class Invalid(CrmError):
    code = "invalid"


class Missing(CrmError):
    code = "not_found"


class Conflict(CrmError):
    code = "conflict"


class Unavailable(CrmError):
    code = "unavailable"


