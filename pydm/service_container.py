from typing import TypeVar, Type

T = TypeVar("T")

class ServiceContainer:
    @classmethod
    def get(cls, name: Type) -> T:
        return