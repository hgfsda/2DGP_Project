from pico2d import *

import game_framework
import title_mode
import main_system


def init():
    global word_image
    global num_image
    global background_image
    global result_bgm

    word_image = load_image('image\\end_word.png')
    num_image = load_image('image\\Num.png')
    background_image = load_image('image\\black_background.png')

    result_bgm = load_music('sound\\result_bgm.mp3')
    result_bgm.set_volume(8)
    result_bgm.repeat_play()

def finish():
    pass

def update():
    pass

def draw():
    clear_canvas()
    background_image.draw(400, 300)
    if main_system.ch_win_check2 == 1:
        word_image.clip_draw(0, 100, 300, 100, 410, 400, 400, 170)
    elif main_system.ai_win_check2 == 1:
        word_image.clip_draw(400, 100, 400, 100, 400, 400, 400, 170)

    word_image.clip_draw(0, 0, 400, 100, 240, 200, 180, 60)
    word_image.clip_draw(400, 0, 500, 100, 560, 200, 180, 60)

    # 주인공 킬 수 확인
    num_image.clip_draw(100 * (main_system.total_ch_kill % 100 // 10), 0, 100, 100, 210, 130, 40, 40)
    num_image.clip_draw(100 * (main_system.total_ch_kill % 10), 0, 100, 100, 250, 130, 40, 40)

    # 적 킬 수 확인
    num_image.clip_draw(100 * (main_system.total_ai_kill % 100 // 10), 0, 100, 100, 550, 130, 40, 40)
    num_image.clip_draw(100 * (main_system.total_ai_kill % 10), 0, 100, 100, 590, 130, 40, 40)
    update_canvas()

def handle_events():
    global check_y
    global result_bgm
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            result_bgm.stop()
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RETURN:
            result_bgm.stop()
            game_framework.change_mode(title_mode)


def pause():
    pass


def resume():
    pass