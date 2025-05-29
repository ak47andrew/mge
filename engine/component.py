from .gameobject import GameObject
from .game import Game
from .scene import Scene, SceneManager
from typing import Callable, Any

# types
CheckerT = Callable[[Game, SceneManager, Scene, GameObject, 'Component'], bool]
ExecutionerT = Callable[[Game, SceneManager, Scene, GameObject, 'Component'], Any]


class Handler:
    checker: CheckerT
    executioner: ExecutionerT

    def __init__(self, checker: CheckerT, executioner: ExecutionerT):
        self.checker = checker
        self.executioner = executioner

    def run(self, game: Game, scene_manager: SceneManager, scene: Scene, game_object: GameObject, component: 'Component') -> None:
        if self.checker(game, scene_manager, scene, game_object, component):
            self.executioner(game, scene_manager, scene, game_object, component)


class Component:
    name: str
    execution_order: int
    handlers: list[Handler]

    def get_default_storage(self):
        raise NotImplementedError("Subclasses must implement get_default_storage")

    def run(self, game: Game, scene_manager: SceneManager, scene: Scene, game_object: GameObject) -> None:
        for handler in self.handlers:
            handler.run(game, scene_manager, scene, game_object, self)


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
