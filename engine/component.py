from .gameobject import GameObject
from typing import Callable, Any

# types
CheckerT = Callable[[GameObject], bool]
ExecutionerT = Callable[[GameObject], Any]


class Handler:
    checker: CheckerT
    executioner: ExecutionerT

    def __init__(self, checker: CheckerT, executioner: ExecutionerT):
        self.checker = checker
        self.executioner = executioner

    def run(self, game_object: GameObject) -> None:
        if self.checker(game_object):
            self.executioner(game_object)


class Component:
    name: str
    execution_order: int
    handlers: list[Handler]

    def get_default_storage(self):
        raise NotImplementedError("Subclasses must implement get_default_storage")

    def run(self, game_object: GameObject) -> None:
        for handler in self.handlers:
            handler.run(game_object)


class _BuiltCustomComponent(Component):
    storage_data: dict[str, Any]

    def __init__(self, name: str, execution_order: int, handlers: list[Handler], **kwargs):
        self.name = name
        self.execution_order = execution_order
        self.handlers = handlers
        self.storage_data = kwargs

    def get_default_storage(self) -> Any:
        return self.storage_data


class CustomComponent:
    def __init__(self):
        self.handlers = []

    def addHandler(self, checker: CheckerT, executioner: ExecutionerT) -> None:
        self.handlers.append(Handler(checker, executioner))

    def build(self, name: str, execution_order: int, **kwargs) -> _BuiltCustomComponent:
        return _BuiltCustomComponent(
            name,
            execution_order,
            self.handlers,
            **kwargs,
        )
