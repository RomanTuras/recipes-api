from abc import ABC
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


class Result(Generic[T], ABC):
    pass


@dataclass
class Ok(Result[T]):
    value: T

    def __repr__(self):
        return f"Result.ok({self.value!r})"


@dataclass
class Error(Result[T]):
    error: Exception

    def __repr__(self):
        return f"Result.error({self.error!r})"
