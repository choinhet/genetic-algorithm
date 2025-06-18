from typing import Literal, TypeVar, Generic

from pydantic import BaseModel, Field

T = TypeVar("T")


class Unit(BaseModel, Generic[T]):
    content: T
    generation: int = Field(default=0)
    score: int = Field(default=0)
    origin: Literal["mutation", "cross_over", "random"] = Field(default="random")
