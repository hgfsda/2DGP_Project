from pico2d import *
import main_system
import game_framework
import title_mode
import project
import result

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# ai Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5


def init():
    global stage_image
    global ai_image
    global ai_run_image
    global frame
    global ai_x
    global ai_state
    global num_image
    global set_image
    global current_time
    global wait_time
    global victory_bgm

    frame = 0
    ai_x = 820
    ai_state = 0
    current_time = main_system.play_time
    wait_time = get_time()
    stage_image = load_image('image\\final_stage.png')
    ai_image = load_image('image\\ai.png')
    ai_run_image = load_image('image\\ai_run.png')
    num_image = load_image('image\\Num.png')
    set_image = load_image('image\\set_check.png')

    victory_bgm = load_music('sound\\victory.mp3')
    victory_bgm.set_volume(8)
    victory_bgm.repeat_play()


def finish():
    pass


def update():
    global frame
    global ai_x
    global ai_state
    global wait_time
    global victory_bgm

    if ai_x > 420:
        frame = (frame + FRAMES_PER_ACTION * ACTION_PER_TIME * 1.5 * game_framework.frame_time) % 5
        ai_x += -1 * RUN_SPEED_PPS * 2.5 * game_framework.frame_time
    else:
        frame = (frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ai_state = 1

    if get_time() - wait_time > 3.0:
        victory_bgm.stop()
        if main_system.ai_win_check1 == 0:
            main_system.ai_win_check1 = 1
            game_framework.change_mode(project)
        elif main_system.ai_win_check1 == 1:
            main_system.ai_win_check2 = 1
            game_framework.change_mode(result)


def draw():
    clear_canvas()
    stage_image.clip_draw(0, 0, 1190, 600, 400, 300, 1000, 600)
    if ai_state == 0:
        ai_run_image.clip_composite_draw(int(frame) * 45, 0, 45, 45, 0, 'h', ai_x - 60, 150, 135, 135)
    elif ai_state == 1:
        ai_image.clip_draw(int(frame) * 45, 45, 45, 45, ai_x, 150, 135, 135)

    # 타이머
    num_image.clip_draw(100 * (int)(current_time % 100 // 10), 0, 100, 100, 360, 530, 80, 100)
    num_image.clip_draw(100 * (int)(current_time % 10), 0, 100, 100, 440, 530, 80, 100)

    # 주인공 세트 확인
    set_image.clip_draw(0, 300 - (main_system.ch_win_check1 * 300), 300, 300, 290, 550, 40, 40)
    set_image.clip_draw(0, 300 - (main_system.ch_win_check2 * 300), 300, 300, 240, 550, 40, 40)

    # 적 세트 확인
    set_image.clip_draw(0, 300 - (main_system.ai_win_check1 * 300), 300, 300, 510, 550, 40, 40)
    set_image.clip_draw(0, 300 - (main_system.ai_win_check2 * 300), 300, 300, 560, 550, 40, 40)

    # 주인공 킬 수 확인
    num_image.clip_draw(100 * (main_system.character_kill % 100 // 10), 0, 100, 100, 270, 500, 30, 30)
    num_image.clip_draw(100 * (main_system.character_kill % 10), 0, 100, 100, 300, 500, 30, 30)

    # 적 킬 수 확인
    num_image.clip_draw(100 * (main_system.ai_kill % 100 // 10), 0, 100, 100, 500, 500, 30, 30)
    num_image.clip_draw(100 * (main_system.ai_kill % 10), 0, 100, 100, 530, 500, 30, 30)
    update_canvas()


def handle_events():
    global victory_bgm
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            victory_bgm.stop()
            game_framework.change_mode(title_mode)


def pause():
    pass


def resume():
    pass
