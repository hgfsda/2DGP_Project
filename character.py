from pico2d import *
import game_framework


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def D_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def D_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# Boy Action Speed
# fill here
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Run:

    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e):
            character.dir = 1
        elif left_down(e) or right_up(e):
            character.dir = -1
        pass

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 5
        character.x += character.dir * 15
        delay(0.05)

    @staticmethod
    def draw(character):
        if character.dir == 1:
            character.run_image.clip_draw(character.frame * 45, 0, 45, 45, character.x, 150, 135, 135)
        elif character.dir == -1:
            character.run_image.clip_composite_draw(character.frame * 45, 0, 45, 45, 0, 'h', character.x - 90, 150, 135, 135)


class Move:

    @staticmethod
    def enter(character, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 Move
            character.dir = 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 Move
            character.dir = -1
        if up_down(e) and character.sword_position < 2:
            character.sword_position += 1
        if down_down(e) and character.sword_position > 0:
            character.sword_position -= 1

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 4
        character.x += character.dir * 5
        delay(0.05)

    @staticmethod
    def draw(character):
        if character.dir == 1:
            character.image.clip_draw(character.frame * 45, 405 - (135 * character.sword_position), 45, 45, character.x,
                                      150, 135, 135)
        elif character.dir == -1:
            character.image.clip_composite_draw(character.frame * 45, 405 - (135 * character.sword_position), 45, 45, 0,
                                                'h', character.x - 90, 150, 135, 135)


class Idle:
    @staticmethod
    def enter(character, e):
        if up_down(e) and character.sword_position < 2:
            character.sword_position += 1
        if down_down(e) and character.sword_position > 0:
            character.sword_position -= 1

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 4
        delay(0.15)

    @staticmethod
    def draw(character):
        if character.dir == 1:
            character.image.clip_draw(character.frame * 45, 450 - (135 * character.sword_position), 45, 45, character.x,
                                      150, 135, 135)
        elif character.dir == -1:
            character.image.clip_composite_draw(character.frame * 45, 450 - (135 * character.sword_position), 45, 45, 0,
                                                'h', character.x - 90, 150, 135, 135)


class StateMachine:
    def __init__(self, character):
        self.character = character
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Move, left_down: Move, left_up: Move, right_up: Move, up_down: Idle, down_down: Idle},
            Move: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, up_down: Move, down_down: Move,
                   D_down: Run},
            Run: {right_down: Run, left_down: Run, right_up: Idle, left_up: Idle, D_down: Run, D_up: Move},
        }

    def start(self):
        self.cur_state.enter(self.character, ('START', 0))

    def update(self):
        self.cur_state.do(self.character)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.character, e)
                self.cur_state = next_state
                self.cur_state.enter(self.character, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.character)


class Character:
    def __init__(self):
        self.x = 200
        self.sword_position = 1  # 검의 위치 / 상단 2 , 중단 1, 하단 0
        self.dir = 1  # 캐릭터의 방향
        self.frame = 0
        self.image = load_image('character.png')
        self.run_image = load_image('Character_run.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
