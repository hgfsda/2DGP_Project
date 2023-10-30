from pico2d import *
from stage import *
from character import Character
import game_world


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif stage.state_machine.cur_state == StartStage:
            stage.handle_event(event)
            if stage.running == False:
                running = False
        elif stage.state_machine.cur_state == PlayStage:
            character.handle_event(event)




def reset_world():
    global running
    global stage
    global character

    running = True

    stage = Stage()
    game_world.add_object(stage, 0)

    character = Character()
    game_world.add_object(character, 1)


def update_world():
    game_world.update()


def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()


open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()

close_canvas()
