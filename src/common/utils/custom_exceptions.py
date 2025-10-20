from fastapi import status


class CustomException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

class BadRequestException(CustomException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedException(CustomException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class PaymentRequiredException(CustomException):
    def __init__(self, detail: str = "Payment required"):
        super().__init__(status_code=status.HTTP_402_PAYMENT_REQUIRED, detail=detail)

class ForbiddenException(CustomException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class NotFoundException(CustomException):
    def __init__(self, detail: str = "Not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ConflictException(CustomException):
    def __init__(self, detail: str = "Conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

class UnprocessableEntityException(CustomException):
    def __init__(self, detail: str = "Unprocessable entity"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

class TooManyRequestsException(CustomException):
    def __init__(self, detail: str = "Too many requests"):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail)

class InternalServerErrorException(CustomException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class NotImplementedException(CustomException):
    def __init__(self, detail: str = "Not implemented"):
        super().__init__(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=detail)

class BadGatewayException(CustomException):
    def __init__(self, detail: str = "Bad gateway"):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)

class ServiceUnavailableException(CustomException):
    def __init__(self, detail: str = "Service unavailable"):
        super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail)

class GatewayTimeoutException(CustomException):
    def __init__(self, detail: str = "Gateway timeout"):
        super().__init__(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=detail)

class InsufficientStorageException(CustomException):
    def __init__(self, detail: str = "Insufficient storage"):
        super().__init__(status_code=507, detail=detail)  # Not in fastapi.status

class NetworkAuthenticationRequiredException(CustomException):
    def __init__(self, detail: str = "Network authentication required"):
        super().__init__(status_code=511, detail=detail)  # Not in fastapi.status

class UnavailableForLegalReasonsException(CustomException):
    def __init__(self, detail: str = "Unavailable for legal reasons"):
        super().__init__(status_code=451, detail=detail)  # Not in fastapi.status
