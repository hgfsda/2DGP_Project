from pico2d import *

import game_framework
import title_mode
import project

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# character Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

def init():
    global stage_image
    global character_image
    global character_run_image
    global frame
    frame = 0
    stage_image = load_image('image\\final_stage.png')
    character_image = load_image('image\\character.png')
    character_run_image = load_image('image\\Character_run.png')
    pass

def finish():
    pass

def update():
    global frame
    pass

def draw():
    clear_canvas()
    stage_image.clip_draw(0, 0, 1190, 600, 400, 300, 1000, 600)
    update_canvas()
    pass

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)


def pause():
    pass


def resume():
    pass