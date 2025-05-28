from .gameobject import GameObject
from .scene import Scene, SceneManager
from .component import Component

class Game:
    def __init__(self):
        pass

    def run(self):
        print(f"Game <{self}> started")
