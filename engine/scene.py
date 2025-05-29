from .gameobject import GameObject
from .utils import PriorityList
from .game import Game
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

    def run(self, game: Game, screen_manager: 'SceneManager'):
        for part in self.to_run:
            if part[0].active:
                if isinstance(part[0], Scene):
                    part[0].run(game, screen_manager)
                else:
                    part[0].run(game, screen_manager, self)

    def on_load(self):
        for game_object in self.gameObjects.values():
            game_object.reinit()


class SceneManager:
    scenes: dict[str, Scene]
    current_scene: Optional[Scene]

    def __init__(self):
        self.scenes = {}
        self.current_scene = None

    def get_scene(self, name: str) -> Optional[Scene]:
        return self.scenes.get(name)

    def get_current_scene(self) -> Optional[Scene]:
        return self.current_scene

    def add_scene(self, scene: Scene) -> None:
        if scene.name in self.scenes:
            raise ValueError(f"Scene '{scene.name}' already exists")
        self.scenes[scene.name] = scene

    @overload
    def remove_scene(self, scene: str) -> None:
       ...

    @overload
    def remove_scene(self, scene: Scene) -> None:
       ...

    def remove_scene(self, scene: Scene | str) -> None:
        if isinstance(scene, Scene):
            self.remove_scene(scene.name)
        del self.scenes[scene]

    def change_scene(self, name: Optional[str]) -> None:
        if name is None:  # This, pretty much, means we want to stop the game.
                          # The only exception is changing to None and then setting new one,
                          # but that's just stupid to do it this way tbh
            self.current_scene = None
            return

        if name not in self.scenes:
            raise ValueError(f"Scene '{name}' does not exist")
        if self.current_scene:
            raise RuntimeError("You really wanted to change scene to itself?? What a funny guy. Why did you expect that to do???" 
                               "You might want to reset the game state or something like that instead." 
                               "Good luck with that. Just don't change scene to itself.")

        self.current_scene = self.scenes[name]
        self.current_scene.on_load()

    def run(self, game: Game) -> bool:
        if self.current_scene is None:
            return False
        self.current_scene.run(game, self)
