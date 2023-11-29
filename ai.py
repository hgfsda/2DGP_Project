import random

from pico2d import *
import game_framework
import main_system
import stage
import lose_stage
import project
import result
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector


def Change_Idle(e):
    return e[0] == 'CHANGE_IDLE'

def Change_Attack(e):
    return e[0] == 'CHANGE_ATTACK'

def Change_Run(e):
    return e[0] == 'CHANGE_RUN'

def Change_Move(e):
    return e[0] == 'CHANGE_MOVE'

def Change_Death(e):
    return e[0] == 'CHANGE_DEATH'


def Change_Win(e):
    return e[0] == 'CHANGE_WIN'


PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 10.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
# ai Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 5

sword_change_cnt = 0
def sword_change(ai):
    if sword_change_cnt == 1:
        if ai.sword_position < 2:
            ai.sword_position += 1
    elif sword_change_cnt == 2:
        if ai.sword_position > 0:
            ai.sword_position -= 1
    elif sword_change_cnt == 3:
        if ai.sword_position > project.character.sword_position:
            ai.sword_position -= 1
        elif ai.sword_position < project.character.sword_position:
            ai.sword_position += 1


class Win:

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
        if get_time() - ai.wait_time > 1.5:
            if main_system.ai_win_check1 == 0:
                main_system.ai_win_check1 = 1
                game_framework.change_mode(project)
            elif main_system.ai_win_check1 == 1:
                main_system.ai_win_check2 = 1
                game_framework.change_mode(result)

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
        if get_time() - ai.wait_time < 0.5:
            if ai.face_dir == 1:
                ai.image.clip_draw(int(ai.frame) * 45, 0, 45, 45, ai.x, 150, 135, 135)
            elif ai.face_dir == 0:
                ai.image.clip_composite_draw(int(ai.frame) * 45, 0, 45, 45, 0, 'h', ai.x - 90, 150,
                                             135, 135)
        if get_time() - ai.wait_time > 2:
            # 2초후 리스폰
            if(project.character.x < 630):
                ai.x, ai.sword_position, ai.face_dir, ai.dir = 780, 1, 0, 0
            else:
                ai.x, ai.sword_position, ai.face_dir, ai.dir = 500, 1, 1, 0
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
        ai.x = clamp(70, ai.x, 820)
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
        ai.wait_time = get_time()

    @staticmethod
    def exit(ai, e):
        pass

    @staticmethod
    def do(ai):
        global sword_change_cnt
        ai.frame = (ai.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ai.x += ai.dir * RUN_SPEED_PPS * game_framework.frame_time
        ai.x = clamp(70, ai.x, 820)
        # if get_time() - ai.wait_time > 0.5:
        #     sword_change_cnt = random.randint(1,4)
        #     sword_change(ai)
        #     ai.wait_time = get_time()

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
        ai.wait_time = get_time()

    @staticmethod
    def exit(ai, e):
        pass

    @staticmethod
    def do(ai):
        global sword_change_cnt
        ai.frame = (ai.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        # if get_time() - ai.wait_time > 0.5:
        #     sword_change_cnt = random.randint(1,4)
        #     sword_change(ai)
        #     ai.wait_time = get_time()

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
        self.wait_time = get_time()
        self.transitions = {
            Idle: {Change_Move: Move, Change_Run: Run, Change_Attack: Attack,
                   Change_Death: Death, Change_Win: Win},
            Move: {Change_Idle: Idle, Change_Run: Run, Change_Attack: Attack,
                   Change_Death: Death, Change_Win: Win},
            Run: {Change_Idle: Idle, Change_Move: Move, Change_Attack: Attack,
                   Change_Death: Death, Change_Win: Win},
            Attack: {Change_Idle: Idle, Change_Death: Death, Change_Win: Win},
            Death: {Change_Idle: Idle},
            Win: {},
        }

    def start(self):
        self.cur_state.enter(self.ai, ('START', 0))

    def update(self):
        self.cur_state.do(self.ai)
        if main_system.ai_kill == 15:
            self.handle_event(('CHANGE_WIN', 0))
        if self.ai.x < 75 and stage.ai_stage < 5:
            stage.ai_stage += 1
            stage.character_stage -= 1
            project.character.x, project.character.face_dir = 110, 1
            self.ai.x = 820
        elif self.ai.x < 75 and stage.ai_stage == 5:
            game_framework.change_mode(lose_stage)
        if main_system.play_time <= 0:
            if main_system.character_kill < main_system.ai_kill:
                self.handle_event(('CHANGE_WIN', 0))

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
        self.x = 780
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
        self.build_behavior_tree()

    def update(self):
        self.state_machine.update()
        self.bt.run()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def handle_collision_sword_body(self, group, other):
        if group == 'character:ai':
            main_system.character_kill += 1
            main_system.total_ch_kill += 1
            self.state_machine.handle_event(('CHANGE_DEATH', 0))

    def handle_collision_sword_sword(self, group, other):
        if self.face_dir == 0:
            if self.x < 820:
                self.x += 2 * RUN_SPEED_PPS * game_framework.frame_time
        elif self.face_dir == 1:
            self.x += -2 * RUN_SPEED_PPS * game_framework.frame_time


    def run_range(self):
        _, _, ch_x, _ = project.character.state_machine.cur_state.character_get_bb(project.character)
        if ch_x + 220 < self.x:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL


    def run_to_wall(self):
        self.dir, self.face_dir = -1, 0
        self.state_machine.handle_event(('CHANGE_RUN', 0))
        return BehaviorTree.RUNNING

    def move_front_range(self):
        _, _, ch_x, _ = project.character.state_machine.cur_state.character_get_bb(project.character)
        if ch_x + 220 >= self.x and ch_x + 150 < self.x:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_ch(self):
        self.dir, self.face_dir = -1, 0
        self.state_machine.handle_event(('CHANGE_MOVE', 0))
        return BehaviorTree.RUNNING

    def Idle_range(self):
        _, _, ch_x, _ = project.character.state_machine.cur_state.character_get_bb(project.character)
        if ch_x + 150 >= self.x and ch_x < self.x:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def Idle_ai(self):
        self.face_dir = 0
        self.state_machine.handle_event(('CHANGE_IDLE', 0))
        return BehaviorTree.RUNNING

    def move_to_back(self):
        self.dir, self.face_dir = 1, 0
        self.state_machine.handle_event(('CHANGE_MOVE', 0))
        return BehaviorTree.RUNNING

    def run_to_back(self):
        self.dir, self.face_dir = 1, 1
        self.state_machine.handle_event(('CHANGE_RUN', 0))
        return BehaviorTree.RUNNING

    def front_attack(self):
        self.face_dir = 0
        self.state_machine.handle_event(('CHANGE_ATTACK', 0))
        return BehaviorTree.SUCCESS

    def back_attack(self):
        self.face_dir = 1
        self.state_machine.handle_event(('CHANGE_ATTACK', 0))
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        c1 = Condition('ch + 220 < ai', self.run_range)
        a1 = Action('달려가는 중', self.run_to_wall)
        SEQ_run = Sequence('캐릭터가 멀면 달리기', c1, a1)

        c2 = Condition('ch + 190 < ai < ch + 220', self.move_front_range)
        a2 = Action('앞으로 가기', self.move_to_ch)
        SEQ_front_move = Sequence('캐릭터 앞으로 가기', c2, a2)

        c3 = Condition('ch + 170 < ai < ch + 190', self.Idle_range)
        a3 = Action('가만히 있기', self.Idle_ai)

        a4 = Action('뒤로 이동', self.move_to_back)
        a5 = Action('앞에 공격', self.front_attack)
        a6 = Action('뒤로 달리기', self.run_to_back)
        a7 = Action('뒤에 공격', self.back_attack)

        SEQ_idle = Sequence('Idle', c3, a5)

        root = SEL_pattern = Selector('패턴', SEQ_run, SEQ_front_move, SEQ_idle)
        self.bt = BehaviorTree(root)