from typing import Any, Optional
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    field: Optional[str] = None
    reason: str
    extra: Optional[Any] = None


class ErrorBody(BaseModel):
    code: str
    message: str
    details: list[ErrorDetail] = []


class ErrorResponse(BaseModel):
    ok: bool = False
    error: ErrorBody


class AppError(Exception):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[list[dict]] = None,
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or []
        super().__init__(message)
