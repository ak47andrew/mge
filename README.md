# Moddable Game Engine (MGE)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ak47andrew/mge)

> [!CAUTION]
> Engine is still under active development and core features (as well as written in this README) can be missing. Also, this README can be outdated: current focus is code and not documentation

## Description
This is just a simple little project to learn how to handle modding and public API. 
I just got a bit of determination out of YouTube video as usual and urgent to create something. 
This will quite possible not be used anywhere, but why not, right? :)

Using Python bc it's quite fast to develop and I feel like it. Maybe will switch over to C# or Go or whatever later 
in a separate branch.

## Schema

Overall schema can be separated like this:
- `Game` -(through the `SceneManager`)> `Scene(s)`
- `Scene` -> `GameObject(s)`
- `GameObject` -> `Component(s)`

The whole idea of the engine is that you describe your custom `Components` (or use built-in), then add them to 
`GameObjects`. This `GameObjects` then arranged in the `Scenes`. `Scenes` are added to `SceneManager`,
part of the `Game`. `Game` then runs, changing `Scenes`, processing logic and rendering the image.

Let's take it bit by bit:

### Component

Each component contains two things: handlers and storage, kept in the `GameObject`. Handlers are explained in the 
`Creating custom Components` section. Storage is a `Dict[name, Dict[str, Any]]` data type stored in the `GameObject`. 
Each component has its own dedicated storage where component's name (typically their class name) is the key in the 
storage dict. Each component can change any `Component's` storage without any problems or warnings.

#### Built-in Components

Here's list of all built-in components and their documentation:

*TODO: change this after you add some*

#### Creating custom Components

Creating custom components are done through creating an instance of `CustomComponent` class. 
Then you need to add custom handlers to it. Each handler is created with two parts: **checker** and **executioner**:
- **Checker** is a function that takes `GameObject` and returns `bool`: whether the handler should be executed. For example 
for the keyboard handler, checker will return True if any (or any of the specified) keys are pressed.
- **Executioner** is the "body" of the handler. It takes `Gameobject`, returned value is discarded. Here you change 
`GameObject's` coordinates, update internal storage and so on.

Here's a very simple example of a custom component:

```python
mover = CustomComponent()


# Moving player up each tick
def update_mover(game_object: GameObject):
    game_object.position.x -= game_object.get_storage("mover").speed

mover.addHandler(
    lambda game_object: True,
    update_mover
)
```

When attaching component to GameObject you should use `build(str, **kwargs)` method to set some storage values 
and setup component's name

```python
player.addCompoent(
    mover.build(
        "mover",
        speed=5
    )
)
```

Storage is set every time `Scene` is loaded

### GameObject

`GameObject` is every entity (both visible like Player, Enemies and the Ground and invisible like day-night loop manager).
In the constructor you should specify its position. Later you should add `Components` to it as mentioned before.

```python
player = GameObject(50, 50)
```

`GameObject` is responsible for updating its components and, if said shortly, just a collection of components and common
storage for them

### Scene

`Scene` is a collection of `GameObjects` with its constructor taking one argument: name of the `Scene`

```python
gameplay_scene = Scene("gameplay_scene")
```

You can add `GameObjects` to `Scene` by using `addGameObject(GameObject)` method

```python
gameplay_scene.addGameObject(player)
```

`Scene` is responsible for updating each GameObject

### Game

`Game` is the main object of the game, holding all the information about your game. 

```python
game = Game()
```

You can change scenes and add/remove scenes in runtime using `SceneManager`:

```python
game.scene_manger.addScene(main_menu)
game.scene_manger.addScene(gameplay_scene)
game.scene_manger.addScene(final_menu)

game.scene_manger.changeScene(main_menu) # both using instance or...
game.scene_manger.changeScene("gameplay_scene") # ...scene name!

# Same here~
game.scene_manger.removeScene(main_menu)
game.scene_manger.removeScene("final_menu")
```

`Game's` mainloop can can be started using `run()` function. It's always should be last line in your program apart from 
error handling, because `run()` is a blocking call, releasing only when exited, game ended or error happened
```python
game.run()
```

`Game` is responsible for handling I/O, managing `Scenes`, handling ticks and notifying `Scene` every in-game tick
