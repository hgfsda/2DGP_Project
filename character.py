from pico2d import *
import game_framework
import main_system
import win_stage
import stage
import project
import result

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


def A_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def Change_Idle(e):
    return e[0] == 'CHANGE_IDLE'


def Change_Death(e):
    return e[0] == 'CHANGE_DEATH'


def Change_Win(e):
    return e[0] == 'CHANGE_WIN'


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# character Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5


class Win:

    @staticmethod
    def enter(character, e):
        character.frame = 0
        character.wait_time = get_time()
        main_system.win_move_check = 1
        pass

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if get_time() - character.wait_time > 1.5:
            if main_system.ch_win_check1 == 0:
                main_system.ch_win_check1 = 1
                game_framework.change_mode(project)
            elif main_system.ch_win_check1 == 1:
                main_system.ch_win_check2 = 1
                game_framework.change_mode(result)

    @staticmethod
    def draw(character):
        character.image.clip_draw(int(character.frame) * 45, 45, 45, 45, character.x, 150, 135, 135)

    @staticmethod
    def character_get_bb(character):
        return -1000, 0, -1000, 0

    @staticmethod
    def sword_get_bb(character):
        return 0, 0, 0, 0


class Death:

    @staticmethod
    def enter(character, e):
        character.frame = 0
        character.wait_time = get_time()
        pass

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        if character.frame < 3:
            character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

    @staticmethod
    def draw(character):
        if get_time() - character.wait_time < 0.5:
            if character.face_dir == 1:
                character.image.clip_draw(int(character.frame) * 45, 0, 45, 45, character.x, 150, 135, 135)
            elif character.face_dir == 0:
                character.image.clip_composite_draw(int(character.frame) * 45, 0, 45, 45, 0, 'h', character.x - 90, 150,
                                                    135, 135)
        if get_time() - character.wait_time > 2:
            # 2초후 리스폰
            if project.ai.x > 170:
                character.x, character.sword_position, character.face_dir, character.dir = 110, 1, 1, 0
            else:
                character.x, character.sword_position, character.face_dir, character.dir = 390, 1, 0, 0
            character.state_machine.handle_event(('CHANGE_IDLE', 0))

    @staticmethod
    def character_get_bb(character):
        return -1000, 0, -1000, 0

    @staticmethod
    def sword_get_bb(character):
        return 0, 0, 0, 0


class Attack:

    @staticmethod
    def enter(character, e):
        character.frame = 0
        character.wait_time = get_time()
        project.sword_sound.play()

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if get_time() - character.wait_time > 0.5:
            character.state_machine.handle_event(('CHANGE_IDLE', 0))

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.image.clip_draw(int(character.frame) * 45, 360 - (135 * character.sword_position), 45, 45,
                                      character.x,
                                      150, 135, 135)
        elif character.face_dir == 0:
            character.image.clip_composite_draw(int(character.frame) * 45, 360 - (135 * character.sword_position), 45,
                                                45, 0,
                                                'h', character.x - 90, 150, 135, 135)

    @staticmethod
    def character_get_bb(character):
        return character.x - 70, 150 - 60, character.x - 20, 150 + 10

    @staticmethod
    def sword_get_bb(character):
        if character.face_dir == 1:
            return character.x - 20, 105 + (
                    20 * character.sword_position), character.x + 27 + (int(character.frame) * 10), 115 + (
                           20 * character.sword_position)
        elif character.face_dir == 0:
            return character.x - 120 - (int(character.frame) * 10), 105 + (
                    20 * character.sword_position), character.x - 70, 115 + (
                           20 * character.sword_position)


class Run:

    @staticmethod
    def enter(character, e):
        if right_down(e):  # 오른쪽으로 Move
            character.dir, character.face_dir, character.right_check = 1, 1, True
        elif left_down(e):  # 왼쪽으로 Move
            character.dir, character.face_dir, character.left_check = -1, 0, True
        if right_up(e):  # 오른쪽으로 Move
            character.dir, character.face_dir, character.right_check = -1, 0, False
        elif left_up(e):  # 왼쪽으로 Move
            character.dir, character.face_dir, character.left_check = 1, 1, False

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * 1.5 * game_framework.frame_time) % 5
        character.x += character.dir * RUN_SPEED_PPS * 2.5 * game_framework.frame_time
        character.x = clamp(70, character.x, 820)
        if not character.left_check and not character.right_check:
            character.face_dir = 0 if character.face_dir == 1 else 1
            character.state_machine.handle_event(('CHANGE_IDLE', 0))

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.run_image.clip_draw(int(character.frame) * 45, 0, 45, 45, character.x, 150, 135, 135)
        elif character.face_dir == 0:
            character.run_image.clip_composite_draw(int(character.frame) * 45, 0, 45, 45, 0, 'h', character.x - 60, 150,
                                                    135, 135)

    @staticmethod
    def character_get_bb(character):
        return character.x - 50, 150 - 70, character.x - 10, 150 + 10

    @staticmethod
    def sword_get_bb(character):
        return 0, 0, 0, 0


class Move:
    @staticmethod
    def enter(character, e):
        if right_down(e):  # 오른쪽으로 Move
            character.dir, character.face_dir, character.right_check = 1, 1, True
        elif left_down(e):  # 왼쪽으로 Move
            character.dir, character.face_dir, character.left_check = -1, 0, True
        if right_up(e):  # 오른쪽으로 Move
            character.dir, character.face_dir, character.right_check = -1, 0, False
        elif left_up(e):  # 왼쪽으로 Move
            character.dir, character.face_dir, character.left_check = 1, 1, False
        if up_down(e) and character.sword_position < 2:
            character.sword_position += 1
        elif down_down(e) and character.sword_position > 0:
            character.sword_position -= 1

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        character.x += character.dir * RUN_SPEED_PPS * game_framework.frame_time
        character.x = clamp(70, character.x, 820)
        if not character.left_check and not character.right_check:
            character.face_dir = 0 if character.face_dir == 1 else 1
            character.state_machine.handle_event(('CHANGE_IDLE', 0))

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.image.clip_draw(int(character.frame) * 45, 405 - (135 * character.sword_position), 45, 45,
                                      character.x,
                                      150, 135, 135)
        elif character.face_dir == 0:
            character.image.clip_composite_draw(int(character.frame) * 45, 405 - (135 * character.sword_position), 45,
                                                45, 0,
                                                'h', character.x - 90, 150, 135, 135)

    @staticmethod
    def character_get_bb(character):
        return character.x - 70, 150 - 60, character.x - 20, 150 + 10

    @staticmethod
    def sword_get_bb(character):
        if character.face_dir == 1:
            return character.x - 20, 105 + (20 * character.sword_position), character.x + 30, 115 + (
                    20 * character.sword_position)
        elif character.face_dir == 0:
            return character.x - 120, 105 + (20 * character.sword_position), character.x - 70, 115 + (
                    20 * character.sword_position)


class Idle:
    @staticmethod
    def enter(character, e):
        if up_down(e) and character.sword_position < 2:
            character.sword_position += 1
        if down_down(e) and character.sword_position > 0:
            character.sword_position -= 1
        character.right_check = False
        character.left_check = False

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(character):
        if character.face_dir == 1:
            character.image.clip_draw(int(character.frame) * 45, 450 - (135 * character.sword_position), 45, 45,
                                      character.x,
                                      150, 135, 135)
        elif character.face_dir == 0:
            character.image.clip_composite_draw(int(character.frame) * 45, 450 - (135 * character.sword_position), 45,
                                                45, 0,
                                                'h', character.x - 90, 150, 135, 135)

    @staticmethod
    def character_get_bb(character):
        return character.x - 70, 150 - 60, character.x - 20, 150 + 10

    @staticmethod
    def sword_get_bb(character):
        if character.face_dir == 1:
            return character.x - 20, 105 + (20 * character.sword_position), character.x + 30, 115 + (
                    20 * character.sword_position)
        elif character.face_dir == 0:
            return character.x - 120, 105 + (20 * character.sword_position), character.x - 70, 115 + (
                    20 * character.sword_position)


class StateMachine:
    def __init__(self, character):
        self.character = character
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Move, left_down: Move, up_down: Idle, down_down: Idle, A_down: Attack,
                   Change_Death: Death, Change_Win: Win},
            Move: {right_down: Move, left_down: Move, right_up: Move, left_up: Move, up_down: Move, down_down: Move,
                   Change_Idle: Idle, A_down: Attack, D_down: Run, Change_Death: Death, Change_Win: Win},
            Run: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, Change_Idle: Idle, D_up: Move,
                  Change_Death: Death, Change_Win: Win},
            Attack: {Change_Idle: Idle, Change_Death: Death, Change_Win: Win},
            Death: {Change_Idle: Idle},
            Win: {},
        }

    def start(self):
        self.cur_state.enter(self.character, ('START', 0))

    def update(self):
        self.cur_state.do(self.character)
        if main_system.character_kill == 15:
            self.handle_event(('CHANGE_WIN', 0))
        if self.character.x > 815 and stage.character_stage < 5:
            stage.character_stage += 1
            stage.ai_stage -= 1
            project.ai.x, project.ai.face_dir = 780, 0
            self.character.x = 70
        elif self.character.x > 815 and stage.character_stage == 5:
            project.stage.bgm.stop()
            game_framework.change_mode(win_stage)
        if main_system.play_time <= 0:
            if main_system.character_kill > main_system.ai_kill:
                self.handle_event(('CHANGE_WIN', 0))
        if main_system.win_move_check == 2:
            self.handle_event(('CHANGE_IDLE', 0))


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
        draw_rectangle(*self.cur_state.character_get_bb(self.character))
        draw_rectangle(*self.cur_state.sword_get_bb(self.character))


class Character:
    def __init__(self):
        self.x = 110
        self.sword_position = 1  # 검의 위치 / 상단 2 , 중단 1, 하단 0
        self.face_dir = 1  # 캐릭터가 바라보는 방향  / 왼쪽 0, 오른쪽 1
        self.dir = 0
        self.frame = 0
        self.left_check = False
        self.right_check = False
        self.image = load_image('image\\character.png')
        self.run_image = load_image('image\\Character_run.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        if main_system.win_move_check == 0:
            self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def handle_collision_sword_body(self, group, other):
        if group == 'ai:character':
            main_system.ai_kill += 1
            main_system.total_ai_kill += 1
            self.state_machine.handle_event(('CHANGE_DEATH', 0))

    def handle_collision_sword_sword(self, group, other):
        if group == 'character:ai':
            if self.face_dir == 0:
                self.x += 2 * RUN_SPEED_PPS * game_framework.frame_time
            elif self.face_dir == 1:
                if self.x > 70:
                    self.x += -2 * RUN_SPEED_PPS * game_framework.frame_time


