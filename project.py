from pico2d import *
from stage import Stage
from character import Character
import game_world
import game_framework


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            character.handle_event(event)


def init():
    global stage
    global character

    stage = Stage()
    game_world.add_object(stage, 0)

    character = Character()
    game_world.add_object(character, 1)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass