from typing import Generic, Optional, Sequence, TypeVar, Union

from pydantic import BaseModel

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    success: bool
    msg: str
    data: Optional[T] = None
    errors: Optional[Union[Sequence[dict], dict]] = None
