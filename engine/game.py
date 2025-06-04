from .scene import SceneManager
from .utils import Context

class Game:
    scene_manager: SceneManager

    def __init__(self):
        self.scene_manager = SceneManager()

    def run(self):
        print(f"Game {self} started")
        ctx = Context()
        ctx.game = self
        while self.scene_manager.run(ctx): pass

    def stop_game(self):
        self.scene_manager.change_scene(None)
