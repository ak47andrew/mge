from .scene import Scene, SceneManager

class Game:
    scene_manager: SceneManager

    def __init__(self):
        self.scene_manager = SceneManager()

    def run(self):
        print(f"Game {self} started")
        while self.scene_manager.run(self): pass

    def stop_game(self):
        self.scene_manager.change_scene(None)
