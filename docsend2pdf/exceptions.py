class InvalidPDFError(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidURLError(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidCredentialsError(Exception):
    def __init__(self, message):
        super().__init__(message)