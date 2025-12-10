from fastapi import status


class CustomException(Exception):
    def __init__(self, status_code: int, detail: str, title: str):
        self.status_code = status_code
        self.detail = detail
        self.title = title

class BadRequestException(CustomException):
    def __init__(self, detail: str, title: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, title=title)

class UnauthorizedException(CustomException):
    def __init__(self, detail: str, title: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, title=title)

class PaymentRequiredException(CustomException):
    def __init__(self, detail: str, title: str = "Payment required"):
        super().__init__(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=detail, title=title)

class ForbiddenException(CustomException):
    def __init__(self, detail: str, title: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail, title=title)

class NotFoundException(CustomException):
    def __init__(self, detail: str, title: str = "Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, title=title)

class ConflictException(CustomException):
    def __init__(self, detail: str, title: str = "Conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail, title=title)

class UnprocessableEntityException(CustomException):
    def __init__(self, detail: str, title: str = "Unprocessable entity"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail, title=title)

class TooManyRequestsException(CustomException):
    def __init__(self, detail: str, title: str = "Too many requests"):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail, title=title)

class InternalServerErrorException(CustomException):
    def __init__(self, detail: str, title: str = "Internal server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail, title=title)

class NotImplementedException(CustomException):
    def __init__(self, detail: str, title: str = "Not implemented"):
        super().__init__(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=detail, title=title)

class BadGatewayException(CustomException):
    def __init__(self, detail: str, title: str = "Bad gateway"):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail, title=title)

class ServiceUnavailableException(CustomException):
    def __init__(self, detail: str, title: str = "Service unavailable"):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail, title=title)

class GatewayTimeoutException(CustomException):
    def __init__(self, detail: str, title: str = "Gateway timeout"):
        super().__init__(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=detail, title=title)

class InsufficientStorageException(CustomException):
    def __init__(self, detail: str, title: str = "Insufficient storage"):
        super().__init__(status_code=507, detail=detail, title=title)  # Not in fastapi.status

class NetworkAuthenticationRequiredException(CustomException):
    def __init__(self, detail: str, title: str = "Network authentication required"):
        super().__init__(status_code=511, detail=detail, title=title)  # Not in fastapi.status

class UnavailableForLegalReasonsException(CustomException):
    def __init__(self, detail: str, title: str = "Unavailable for legal reasons"):
        super().__init__(status_code=451, detail=detail, title=title)  # Not in fastapi.status
