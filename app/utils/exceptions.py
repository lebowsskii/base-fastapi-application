from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.utils.response import BaseResponse


class LimitExceededError(Exception):
    """Raise when limit exceeded"""


class NotFoundError(Exception):
    """Raise when resource not found"""


class BadRequestError(Exception):
    """Raise when request is invalid"""


class InternalServerError(Exception):
    """Raise when internal error occurs"""


class UnauthorizedError(Exception):
    """Raise when user is not authorized"""


class AccessDeniedError(Exception):
    """Raise when user is not allowed to access resource"""


def register_exception_handlers(app):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                BaseResponse(
                    success=False,
                    msg="invalid request body",
                    errors=exc.errors(),
                )
            ),
        )

    @app.exception_handler(NotFoundError)
    async def not_found_exception_handler(_: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(
                BaseResponse(
                    success=False,
                    msg=str(exc),
                )
            ),
        )

    @app.exception_handler(InternalServerError)
    async def internal_server_error_exception_handler(
        _: Request, exc: InternalServerError
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(
                BaseResponse(
                    success=False,
                    msg=str(exc),
                )
            ),
        )

    @app.exception_handler(BadRequestError)
    async def bad_request_exception_handler(_: Request, exc: BadRequestError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(
                BaseResponse(
                    success=False,
                    msg=str(exc),
                )
            ),
        )

    @app.exception_handler(UnauthorizedError)
    async def unauthorized_error_exception_handler(_: Request, exc: UnauthorizedError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder(
                BaseResponse(
                    success=False,
                    msg=str(exc),
                )
            ),
        )

    @app.exception_handler(AccessDeniedError)
    async def access_denied_error_exception_handler(_: Request, exc: AccessDeniedError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=jsonable_encoder(
                BaseResponse(
                    success=False,
                    msg=str(exc),
                )
            ),
        )

    @app.exception_handler(LimitExceededError)
    async def limit_exceeded_error_exception_handler(
        _: Request, exc: LimitExceededError
    ):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content=jsonable_encoder(
                BaseResponse(
                    success=False,
                    msg=str(exc),
                )
            ),
        )
