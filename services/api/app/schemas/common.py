from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
