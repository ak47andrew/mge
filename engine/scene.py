from .gameobject import GameObject
from .utils import PriorityList
from typing import Self, Optional, overload


class Scene:
    name: str
    gameObjects: dict[str, GameObject]
    subScenes: dict[str, Self]
    to_run: PriorityList[GameObject | Self]
    priority: Optional[int]  # Can be None for root scene (priority is not relevant)
    active: bool  # Indicates if the scene is currently active and should be processed
                  # Root scene is always active, it's `active` flag is ignored

    def __init__(self, name: str, priority: Optional[int] = None) -> None:
        self.gameObjects = {}
        self.subScenes = {}
        self.to_run = PriorityList()
        self.name = name
        self.priority = priority
        self.active = True

    def add_game_object(self, game_object: GameObject) -> None:
        if game_object.name in self.gameObjects:
            raise ValueError(f"Game object '{game_object.name}' already exists")
        self.gameObjects[game_object.name] = game_object
        self.to_run.add(game_object, game_object.priority)

    @overload
    def remove_game_object(self, game_object: str) -> None:
        ...

    @overload
    def remove_game_object(self, game_object: GameObject) -> None:
        ...

    def remove_game_object(self, game_object: GameObject | str) -> None:
        if isinstance(game_object, GameObject):
            self.remove_game_object(game_object.name)

        self.to_run.remove(self.gameObjects[game_object])
        del self.gameObjects[game_object]

    def add_sub_scene(self, sub_scene: Self) -> None:
        if sub_scene.name in self.subScenes:
            raise ValueError(f"Sub-scene '{sub_scene.name}' already exists")
        self.subScenes[sub_scene.name] = sub_scene
        self.to_run.add(sub_scene, sub_scene.priority)

    @overload
    def remove_sub_scene(self, sub_scene: str) -> None:
        ...

    @overload
    def remove_sub_scene(self, sub_scene: Self) -> None:
        ...

    def remove_sub_scene(self, sub_scene: Self | str) -> None:
        if isinstance(sub_scene, Scene):
            self.remove_sub_scene(sub_scene.name)
        self.to_run.remove(self.subScenes[sub_scene])
        del self.subScenes[sub_scene]

    def set_active(self, active: bool) -> None:
        self.active = active

    def run(self):
        for part in self.to_run:
            if part[0].active:
                part[0].run()

    def on_load(self):
        for game_object in self.gameObjects.values():
            game_object.reinit()


class SceneManager:
    pass
