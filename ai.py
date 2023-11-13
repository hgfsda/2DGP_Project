from pico2d import *
import game_framework


def Change_Idle(e):
    return e[0] == 'CHANGE_IDLE'


def Change_Death(e):
    return e[0] == 'CHANGE_DEATH'


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# ai Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5


class Win:

    @staticmethod
    def enter(ai, e):
        ai.frame = 0
        pass

    @staticmethod
    def exit(ai, e):
        pass

    @staticmethod
    def do(ai):
        ai.frame = (ai.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(ai):
        ai.image.clip_draw(int(ai.frame) * 45, 45, 45, 45, ai.x, 150, 135, 135)

    @staticmethod
    def character_get_bb(ai):
        return 0, 1, 0, 1

    @staticmethod
    def sword_get_bb(ai):
        return 0, 1, 0, 1


class Death:

    @staticmethod
    def enter(ai, e):
        ai.frame = 0
        ai.wait_time = get_time()
        pass

    @staticmethod
    def exit(ai, e):
        pass

    @staticmethod
    def do(ai):
        if ai.frame < 3:
            ai.frame = (ai.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)

    @staticmethod
    def draw(ai):
        if get_time() - ai.wait_time < 1.5:
            if ai.face_dir == 1:
                ai.image.clip_draw(int(ai.frame) * 45, 0, 45, 45, ai.x, 150, 135, 135)
            elif ai.face_dir == 0:
                ai.image.clip_composite_draw(int(ai.frame) * 45, 0, 45, 45, 0, 'h', ai.x - 90, 150,
                                             135, 135)
        if get_time() - ai.wait_time > 3:
            # 3초후 리스폰
            ai.x = 680
            ai.sword_position = 1
            ai.face_dir = 0
            ai.dir = 0
            ai.state_machine.handle_event(('CHANGE_IDLE', 0))

    @staticmethod
    def character_get_bb(ai):
        return 0, 1, 0, 1

    @staticmethod
    def sword_get_bb(ai):
        return 0, 1, 0, 1


class Attack:

    @staticmethod
    def enter(ai, e):
        ai.frame = 0
        ai.wait_time = get_time()
        pass

    @staticmethod
    def exit(ai, e):
        pass

    @staticmethod
    def do(ai):
        ai.frame = (ai.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if get_time() - ai.wait_time > 0.5:
            ai.state_machine.handle_event(('CHANGE_IDLE', 0))

    @staticmethod
    def draw(ai):
        if ai.face_dir == 1:
            ai.image.clip_draw(int(ai.frame) * 45, 360 - (135 * ai.sword_position), 45, 45, ai.x,
                               150, 135, 135)
        elif ai.face_dir == 0:
            ai.image.clip_composite_draw(int(ai.frame) * 45, 360 - (135 * ai.sword_position), 45, 45, 0,
                                         'h', ai.x - 90, 150, 135, 135)

    @staticmethod
    def character_get_bb(ai):
        return ai.x - 70, 150 - 60, ai.x - 20, 150 + 10

    @staticmethod
    def sword_get_bb(ai):
        if ai.face_dir == 1:
            return ai.x - 20, 105 + (
                    20 * ai.sword_position), ai.x + 27 + (int(ai.frame) * 10), 115 + (20 * ai.sword_position)
        elif ai.face_dir == 0:
            return ai.x - 120 - (int(ai.frame) * 10), 105 + (20 * ai.sword_position), ai.x - 70, 115 + (
                    20 * ai.sword_position)


class Run:

    @staticmethod
    def enter(ai, e):
        pass

    @staticmethod
    def exit(ai, e):
        pass

    @staticmethod
    def do(ai):
        ai.frame = (ai.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * 1.5 * game_framework.frame_time) % 5
        ai.x += ai.dir * RUN_SPEED_PPS * 2.5 * game_framework.frame_time
        pass

    @staticmethod
    def draw(ai):
        if ai.face_dir == 1:
            ai.run_image.clip_draw(int(ai.frame) * 45, 0, 45, 45, ai.x, 150, 135, 135)
        elif ai.face_dir == 0:
            ai.run_image.clip_composite_draw(int(ai.frame) * 45, 0, 45, 45, 0, 'h', ai.x - 60, 150,
                                             135, 135)

    @staticmethod
    def character_get_bb(ai):
        return ai.x - 50, 150 - 70, ai.x - 10, 150 + 10

    @staticmethod
    def sword_get_bb(ai):
        return 0, 1, 0, 1


class Move:
    @staticmethod
    def enter(ai, e):
        pass

    @staticmethod
    def exit(ai, e):
        pass

    @staticmethod
    def do(ai):
        ai.frame = (ai.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ai.x += ai.dir * RUN_SPEED_PPS * game_framework.frame_time
        pass

    @staticmethod
    def draw(ai):
        if ai.face_dir == 1:
            ai.image.clip_draw(int(ai.frame) * 45, 405 - (135 * ai.sword_position), 45, 45, ai.x,
                               150, 135, 135)
        elif ai.face_dir == 0:
            ai.image.clip_composite_draw(int(ai.frame) * 45, 405 - (135 * ai.sword_position), 45, 45, 0,
                                         'h', ai.x - 90, 150, 135, 135)

    @staticmethod
    def character_get_bb(ai):
        return ai.x - 70, 150 - 60, ai.x - 20, 150 + 10

    @staticmethod
    def sword_get_bb(ai):
        if ai.face_dir == 1:
            return ai.x - 20, 105 + (20 * ai.sword_position), ai.x + 30, 115 + (
                    20 * ai.sword_position)
        elif ai.face_dir == 0:
            return ai.x - 120, 105 + (20 * ai.sword_position), ai.x - 70, 115 + (
                    20 * ai.sword_position)


class Idle:
    @staticmethod
    def enter(ai, e):
        pass

    @staticmethod
    def exit(ai, e):
        pass

    @staticmethod
    def do(ai):
        ai.frame = (ai.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    @staticmethod
    def draw(ai):
        if ai.face_dir == 1:
            ai.image.clip_draw(int(ai.frame) * 45, 450 - (135 * ai.sword_position), 45, 45,
                               ai.x,
                               150, 135, 135)
        elif ai.face_dir == 0:
            ai.image.clip_composite_draw(int(ai.frame) * 45, 450 - (135 * ai.sword_position), 45,
                                         45, 0,
                                         'h', ai.x - 90, 150, 135, 135)

    @staticmethod
    def character_get_bb(ai):
        return ai.x - 70, 150 - 60, ai.x - 20, 150 + 10

    @staticmethod
    def sword_get_bb(ai):
        if ai.face_dir == 1:
            return ai.x - 20, 105 + (20 * ai.sword_position), ai.x + 30, 115 + (
                    20 * ai.sword_position)
        elif ai.face_dir == 0:
            return ai.x - 120, 105 + (20 * ai.sword_position), ai.x - 70, 115 + (
                    20 * ai.sword_position)


class StateMachine:
    def __init__(self, ai):
        self.ai = ai
        self.cur_state = Idle
        self.transitions = {
            Idle: {Change_Death: Death},
            Move: {Change_Death: Death},
            Run: {Change_Death: Death},
            Attack: {Change_Death: Death},
            Death: {Change_Idle: Idle},
            Win: {},
        }

    def start(self):
        self.cur_state.enter(self.ai, ('START', 0))

    def update(self):
        self.cur_state.do(self.ai)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.ai, e)
                self.cur_state = next_state
                self.cur_state.enter(self.ai, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.ai)
        draw_rectangle(*self.cur_state.character_get_bb(self.ai))
        draw_rectangle(*self.cur_state.sword_get_bb(self.ai))


class Ai:
    def __init__(self):
        self.x = 680
        self.sword_position = 1  # 검의 위치 / 상단 2 , 중단 1, 하단 0
        self.face_dir = 0  # 캐릭터가 바라보는 방향  / 왼쪽 0, 오른쪽 1
        self.dir = 0
        self.frame = 0
        self.left_check = False
        self.right_check = False
        self.image = load_image('image\\ai.png')
        self.run_image = load_image('image\\ai_run.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def handle_collision_sword_body(self, group, other):
        if group == 'character:ai':
            self.state_machine.handle_event(('CHANGE_DEATH', 0))

    def handle_collision_sword_sword(self, group, other):
        if self.face_dir == 0:
            self.x += 2 * RUN_SPEED_PPS * game_framework.frame_time
        elif self.face_dir == 1:
            self.x += -2 * RUN_SPEED_PPS * game_framework.frame_time

