class BaseException(Exception):
    def __init__(self, message: str, details: str = ""):
        self.message = message
        self.details = details

        super().__init__(self.message, self.details)


class Conflict(BaseException): ...


class UnknownActionDispatcher(BaseException): ...


class UnreachableConnection(BaseException): ...


class PayloadMalformed(BaseException): ...
