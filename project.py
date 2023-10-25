from pico2d import *


class Stage:
    def __init__(self):
        self.image = load_image('start_stage.png')
        self.frame = 0

    def draw(self):
        self.image.clip_draw(0, 0, 2200, 600, 1100 + self.frame, 300, 2200, 600)

    def update(self):
        self.frame = self.frame - 10
        if self.frame <= -1300:
            self.frame = -100


class Character:
    def __init__(self):
        self.x, self.y = 400, 150
        self.frame = 0
        self.image = load_image('character.png')

    def update(self):
        self.frame = (self.frame + 1) % 4
        delay(0.07)

    def draw(self):
        self.image.clip_draw(self.frame * 45, 495, 45, 45, self.x, self.y, 135, 135)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def reset_world():
    global running
    global stage
    global character
    global world

    running = True
    world = []

    stage = Stage()
    world.append(stage)

    character = Character()
    world.append(character)


def update_world():
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()
