from fastapi import HTTPException, status


class DomainError(HTTPException):
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail: str | None = None) -> None:
        super().__init__(status_code=self.status_code, detail=detail or self.__class__.__name__)


class NotFound(DomainError):
    status_code = status.HTTP_404_NOT_FOUND


class Conflict(DomainError):
    status_code = status.HTTP_409_CONFLICT


class Unauthorized(DomainError):
    status_code = status.HTTP_401_UNAUTHORIZED


class Forbidden(DomainError):
    status_code = status.HTTP_403_FORBIDDEN


class UpstreamError(DomainError):
    status_code = status.HTTP_502_BAD_GATEWAY


class ServiceUnavailable(DomainError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class PayloadTooLarge(DomainError):
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE


class UnsupportedMedia(DomainError):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
