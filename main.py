"""This is an example of a simple game using the engine."""
from engine import Game, Scene

game = Game()

scene1 = Scene("Scene 1")
game.scene_manager.add_scene(scene1)
game.scene_manager.change_scene(scene1)

game.run()
