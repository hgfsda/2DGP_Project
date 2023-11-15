from pico2d import *
from stage import Stage
from character import Character
from ai import Ai
import game_world
import game_framework
import title_mode


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            character.handle_event(event)


def init():
    global stage
    global character
    global ai

    stage = Stage()
    game_world.add_object(stage, 0)

    character = Character()
    game_world.add_object(character, 1)

    ai = Ai()
    game_world.add_object(ai, 1)

    game_world.add_collision_pair('character:ai', character, ai)
    game_world.add_collision_pair('ai:character', ai, character)


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass