from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from src.common.errors import ErrorResponse, ErrorBody, ErrorDetail, AppError


def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    payload = ErrorResponse(
        error=ErrorBody(
            code=exc.code,
            message=exc.message,
            details=[ErrorDetail(**d) for d in exc.details],
        )
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    details = []
    for e in exc.errors():
        # loc: ('body','email') -> "email"
        loc = e.get("loc", [])
        field = ".".join(str(x) for x in loc if x not in ("body", "query", "path"))
        details.append({"field": field or None, "reason": e.get("msg", "invalid")})

    payload = ErrorResponse(
        error=ErrorBody(
            code="VALIDATION_ERROR",
            message="Invalid request",
            details=[ErrorDetail(**d) for d in details],
        )
    )
    return JSONResponse(status_code=422, content=payload.model_dump())


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    # nếu vẫn có chỗ raise HTTPException, map về format chung
    payload = ErrorResponse(
        error=ErrorBody(
            code=f"HTTP_{exc.status_code}",
            message=str(exc.detail),
            details=[],
        )
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    payload = ErrorResponse(
        error=ErrorBody(
            code="INTERNAL_ERROR",
            message="Something went wrong",
            details=[],
        )
    )
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content=payload.model_dump())
