from typing import ClassVar, Optional

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.error import ErrorResponse


class AppError(Exception):
    """Base class for application errors that map to a structured error response."""

    code: ClassVar[str] = "INTERNAL_ERROR"
    status_code: ClassVar[int] = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str, *, code: Optional[str] = None):
        self.message = message
        if code is not None:
            self.code = code
        super().__init__(message)


class BadRequestError(AppError):
    """Raise when request is invalid"""

    code = "BAD_REQUEST"
    status_code = status.HTTP_400_BAD_REQUEST


class UnauthorizedError(AppError):
    """Raise when user is not authorized"""

    code = "UNAUTHORIZED"
    status_code = status.HTTP_401_UNAUTHORIZED


class AccessDeniedError(AppError):
    """Raise when user is not allowed to access resource"""

    code = "ACCESS_DENIED"
    status_code = status.HTTP_403_FORBIDDEN


class NotFoundError(AppError):
    """Raise when resource not found"""

    code = "NOT_FOUND"
    status_code = status.HTTP_404_NOT_FOUND


class LimitExceededError(AppError):
    """Raise when limit exceeded"""

    code = "LIMIT_EXCEEDED"
    status_code = status.HTTP_429_TOO_MANY_REQUESTS


class InternalServerError(AppError):
    """Raise when internal error occurs"""

    code = "INTERNAL_ERROR"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(ErrorResponse(code=exc.code, message=exc.message)),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                ErrorResponse(
                    code="VALIDATION_ERROR",
                    message="Invalid request body",
                    details=exc.errors(),
                )
            ),
        )
