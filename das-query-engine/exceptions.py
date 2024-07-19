class BaseException(Exception):
    def __init__(self, message: str, details: str = ""):
        self.message = message
        self.details = details

        super().__init__(self.message, self.details)


class Conflict(BaseException):
    # pragma: no cover
    ...


class UnknownActionDispatcher(BaseException):
    # pragma: no cover
    ...


class UnreachableConnection(BaseException):
    # pragma: no cover
    ...


class PayloadMalformed(BaseException):
    # pragma: no cover
    ...
