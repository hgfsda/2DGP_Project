from pico2d import *
import main_system
import game_framework
import title_mode

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
    global character_x
    global character_state
    global num_image
    global set_image
    global current_time

    frame = 0
    character_x = 70
    character_state = 0
    current_time = main_system.play_time
    stage_image = load_image('image\\final_stage.png')
    character_image = load_image('image\\character.png')
    character_run_image = load_image('image\\Character_run.png')
    num_image = load_image('image\\Num.png')
    set_image = load_image('image\\set_check.png')
    pass

def finish():
    pass

def update():
    global frame
    global character_x
    global character_state
    if character_x < 400:
        frame = (frame + FRAMES_PER_ACTION * ACTION_PER_TIME * 1.5 * game_framework.frame_time) % 5
        character_x += RUN_SPEED_PPS * 2.5 * game_framework.frame_time
    else:
        frame = (frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        character_state = 1
    pass

def draw():
    clear_canvas()
    stage_image.clip_draw(0, 0, 1190, 600, 400, 300, 1000, 600)
    if character_state == 0:
        character_run_image.clip_draw(int(frame) * 45, 0, 45, 45, character_x, 150, 135, 135)
    elif character_state == 1:
        character_image.clip_draw(int(frame) * 45, 45, 45, 45, character_x, 150, 135, 135)

    # 타이머
    num_image.clip_draw(100 * (int)(current_time % 100 // 10), 0, 100, 100, 360, 530, 80, 100)
    num_image.clip_draw(100 * (int)(current_time % 10), 0, 100, 100, 440, 530, 80, 100)

    # 주인공 세트 확인
    set_image.clip_draw(0, 300, 300, 300, 290, 550, 40, 40)
    set_image.clip_draw(0, 300, 300, 300, 240, 550, 40, 40)

    # 적 세트 확인
    set_image.clip_draw(0, 300, 300, 300, 510, 550, 40, 40)
    set_image.clip_draw(0, 300, 300, 300, 560, 550, 40, 40)

    # 주인공 킬 수 확인
    num_image.clip_draw(100 * (main_system.character_kill % 100 // 10), 0, 100, 100, 270, 500, 30, 30)
    num_image.clip_draw(100 * (main_system.character_kill % 10), 0, 100, 100, 300, 500, 30, 30)

    # 적 킬 수 확인
    num_image.clip_draw(100 * (main_system.ai_kill % 100 // 10), 0, 100, 100, 500, 500, 30, 30)
    num_image.clip_draw(100 * (main_system.ai_kill % 10), 0, 100, 100, 530, 500, 30, 30)
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