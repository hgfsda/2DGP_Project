from pico2d import *
from stage import Stage
from main_system import System
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
    global system
    global sword_sound
    global death_sound
    global ai_data_list
    global character_data_list

    stage = Stage()
    game_world.add_object(stage, 0)

    with open('gamedata\\character_data.json', 'r') as f:  # 파일을 오픈해서 f에 연결
        character_data_list = json.load(f)
        character = Character()
        character.__dict__.update(character_data_list[0])
        game_world.add_object(character, 1)

    with open('gamedata\\ai_data.json', 'r') as f:  # 파일을 오픈해서 f에 연결
        ai_data_list = json.load(f)
        ai = Ai()
        ai.__dict__.update(ai_data_list[0])
        game_world.add_object(ai, 1)

    system = System()
    game_world.add_object(system, 3)

    game_world.add_collision_pair('character:ai', character, ai)
    game_world.add_collision_pair('ai:character', ai, character)

    sword_sound = load_wav('sound\\sword.wav')
    sword_sound.set_volume(22)
    death_sound = load_wav('sound\\death_sound.wav')
    death_sound.set_volume(22)


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
