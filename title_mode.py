from pico2d import *

import game_framework
import main_system
import project


def init():
    global start_stage_image
    global start_word_image
    global title_bgm
    global choose_menu
    global confirmed_menu
    global check_y  # 시작 화면에서 start exit 표시해주는 화살표 위치
    global frame
    frame = 0
    check_y = 0
    start_stage_image = load_image('image\\start_stage.png')
    start_word_image = load_image('image\\start.png')
    title_bgm = load_music('sound\\title.mp3')
    title_bgm.set_volume(10)
    title_bgm.repeat_play()
    choose_menu = load_wav('sound\\choose_menu.wav')
    confirmed_menu = load_wav('sound\\confirmed_menu.wav')
    choose_menu.set_volume(80)
    confirmed_menu.set_volume(13)


def finish():
    pass


def update():
    global frame

    frame -= 5
    if frame <= -1300:
        frame = -100
    delay(0.03)


def draw():
    clear_canvas()
    start_stage_image.clip_draw(0, 0, 2200, 600, 1100 + frame, 300, 2200, 600)  # 배경
    start_word_image.clip_draw(0, 150, 500, 100, 465, 450, 800, 200)  # 펜싱 게임 제목
    start_word_image.clip_draw(0, 80, 200, 60, 420, 250, 400, 120)  # start
    start_word_image.clip_draw(0, 10, 200, 60, 465, 150, 400, 120)  # exit
    start_word_image.clip_draw(200, 10, 30, 60, 165, 260 - (110 * check_y), 60, 120)  # 화살표 위치
    update_canvas()


def game_start_reset():
    main_system.total_ai_kill, main_system.total_ch_kill = 0, 0
    main_system.ch_win_check1, main_system.ch_win_check2 = 0, 0
    main_system.ai_win_check1, main_system.ai_win_check2 = 0, 0


def handle_events():
    global check_y
    global title_bgm
    global choose_menu
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and (event.key == SDLK_UP or event.key == SDLK_DOWN):
            choose_menu.play()
            check_y = 1 - check_y
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RETURN):
            if check_y == 0:
                game_start_reset()
                confirmed_menu.play()
                title_bgm.stop()
                game_framework.change_mode(project)
            elif check_y == 1:
                game_framework.quit()


def pause():
    pass


def resume():
    pass
