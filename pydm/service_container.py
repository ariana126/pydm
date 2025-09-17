from inspect import signature
from typing import TypeVar, Type, Dict
from underpy import Encapsulated

T = TypeVar("T")

class ServiceContainer(Encapsulated):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls._instance = super(ServiceContainer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "__services"):
            self.__services: dict[Type[T], T] = {}

    @classmethod
    def get_instance(cls) -> 'ServiceContainer':
        if not cls.__instance:
            cls.__instance = cls()
        return cls.__instance

    def get_service(self, cls: Type[T]) -> T:
        if cls in self.__services:
            return self.__services[cls]

        dependencies: dict[str, T] = {}
        arguments = signature(cls.__init__).parameters
        for arg_name, arg in arguments.items():
            if 'self' == arg_name or arg.VAR_POSITIONAL == arg.kind or arg.VAR_KEYWORD == arg.kind:
                continue

            arg_cls = arg.annotation
            if arg.empty == arg_cls:
                raise ValueError(f"Dependency '{arg_name}' in '{cls.__name__}' constructor is missing a type hint.")

            dependencies[arg_name] = self.get_service(arg_cls)

        instance = cls(**dependencies)
        self.__services[cls] = instance

        return instance