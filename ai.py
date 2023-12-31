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


PIXEL_PER_METER = (10.0 / 0.2)
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
        main_system.win_move_check = 2

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
        ai.first_in_pattern = False
        project.death_sound.play()

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
            if (project.character.x < 630):
                ai.__dict__.update(project.ai_data_list[0])
            else:
                ai.__dict__.update(project.ai_data_list[1])
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
        project.sword_sound.play()

    @staticmethod
    def exit(ai, e):
        pass

    @staticmethod
    def do(ai):
        ai.frame = (ai.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if get_time() - ai.wait_time > 0.5:
            ch_x, _, _, _ = project.character.state_machine.cur_state.character_get_bb(project.character)
            if ch_x == -1000:  # 캐릭터가 죽어있으면
                ai.first_in_pattern = False
                ai.state_machine.handle_event(('CHANGE_IDLE', 0))
            else:
                ai.face_dir, ai.dir = 0, -1
                ai.pattern_check = 1
                ai.state_machine.handle_event(('CHANGE_MOVE', 0))

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
        ai.sword_time = get_time()
        if ai.first_in_pattern == True:
            ai.pattern_time = get_time()

    @staticmethod
    def exit(ai, e):
        pass

    @staticmethod
    def do(ai):
        global sword_change_cnt
        ai.frame = (ai.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        ai.x += ai.dir * RUN_SPEED_PPS * game_framework.frame_time
        ai.x = clamp(70, ai.x, 820)
        if get_time() - ai.sword_time > 0.5:
            sword_change_cnt = random.randint(1, 4)
            sword_change(ai)
            ai.sword_time = get_time()
        if ai.first_in_pattern == True:
            if get_time() - ai.pattern_time > 0.5:
                ai.first_in_pattern = False

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
        ai.sword_time = get_time()
        if ai.first_in_pattern == True:
            ai.pattern_time = get_time()

    @staticmethod
    def exit(ai, e):
        pass

    @staticmethod
    def do(ai):
        global sword_change_cnt
        ai.frame = (ai.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if get_time() - ai.sword_time > 0.5:
            sword_change_cnt = random.randint(1, 4)
            sword_change(ai)
            ai.sword_time = get_time()
        if ai.first_in_pattern == True:
            if get_time() - ai.pattern_time > 0.5:
                ai.first_in_pattern = False

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
            Attack: {Change_Idle: Idle, Change_Move: Move, Change_Death: Death, Change_Win: Win},
            Death: {Change_Idle: Idle},
            Win: {},
        }

    def start(self):
        self.cur_state.enter(self.ai, ('START', 0))

    def update(self):
        self.cur_state.do(self.ai)
        if main_system.ai_kill == 10:
            self.handle_event(('CHANGE_WIN', 0))
        if self.ai.x < 75 and stage.ai_stage < 5:
            stage.ai_stage += 1
            stage.character_stage -= 1
            project.character.x, project.character.face_dir = 110, 1
            self.ai.x = 820
        elif self.ai.x < 75 and stage.ai_stage == 5:
            project.stage.bgm.stop()
            game_framework.change_mode(lose_stage)
        if main_system.play_time <= 0:
            if main_system.character_kill < main_system.ai_kill:
                self.handle_event(('CHANGE_WIN', 0))
        if main_system.win_move_check == 1:
            self.handle_event(('CHANGE_IDLE', 0))

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


class Ai:
    def __init__(self, x=0, face_dir=0, dir=0, sword_position=0):
        self.x, self.face_dir = x, face_dir  # 캐릭터가 바라보는 방향  / 왼쪽 0, 오른쪽 1
        self.dir, self.sword_position = dir, sword_position  # 검의 위치 / 상단 2 , 중단 1, 하단 0
        self.frame = 0
        self.pattern_check = 0
        self.first_in_pattern = False
        self.pattern_time = 0
        self.image = load_image('image\\ai.png')
        self.run_image = load_image('image\\ai_run.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.build_behavior_tree()

    def update(self):
        self.state_machine.update()
        if main_system.win_move_check == 0:
            self.bt.run()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def handle_collision_sword_body(self, group, other):
        if group == 'character:ai':
            self.state_machine.handle_event(('CHANGE_DEATH', 0))
            main_system.character_kill += 1
            main_system.total_ch_kill += 1

    def handle_collision_sword_sword(self, group, other):
        if self.face_dir == 0:
            if self.x < 820:
                self.x += 2 * RUN_SPEED_PPS * game_framework.frame_time
        elif self.face_dir == 1:
            self.x += -2 * RUN_SPEED_PPS * game_framework.frame_time

    def ai_behind_character(self):  # ai가 주인공보다 오른쪽에 있는 경우
        ai_x, _, _, _ = self.state_machine.cur_state.character_get_bb(self)
        _, _, ch_x, _ = project.character.state_machine.cur_state.character_get_bb(project.character)
        if ai_x >= ch_x:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def ai_front_character(self):  # ai가 주인공보다 왼쪽에 있는 경우
        _, _, ai_x, _ = self.state_machine.cur_state.character_get_bb(self)
        ch_x, _, _, _ = project.character.state_machine.cur_state.character_get_bb(project.character)
        if ai_x < ch_x:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

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
        if ch_x + 220 >= self.x and ch_x + 150 < self.x and self.first_in_pattern == False:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_ch(self):
        self.dir, self.face_dir = -1, 0
        self.state_machine.handle_event(('CHANGE_MOVE', 0))
        return BehaviorTree.RUNNING

    def total_pattern_range(self):
        _, _, ch_x, _ = project.character.state_machine.cur_state.character_get_bb(project.character)
        if ch_x + 150 >= self.x and ch_x < self.x + 70:
            if self.first_in_pattern == False:  # 만약 범위에 처음 들어오면
                self.first_in_pattern = True  # 처음이 아니라고 표시
                self.pattern_check = random.randint(0, 3)  # 패턴 3가지 랜덤 행동
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def total_pattern(self):
        if self.pattern_check == 0 and self.state_machine.cur_state != Death:  # 가만히 있기
            self.face_dir = 0
            self.state_machine.handle_event(('CHANGE_IDLE', 0))
            return BehaviorTree.RUNNING
        elif self.pattern_check == 1 and self.state_machine.cur_state != Death:  # 뒤로 이동
            self.dir, self.face_dir = 1, 0
            self.state_machine.handle_event(('CHANGE_MOVE', 0))
            return BehaviorTree.RUNNING
        elif self.pattern_check == 2 and self.state_machine.cur_state != Death:  # 공격
            self.face_dir = 0
            self.state_machine.handle_event(('CHANGE_ATTACK', 0))
            return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        c1 = Condition('ch + 220 < ai', self.run_range)
        a1 = Action('달려가는 중', self.run_to_wall)
        SEQ_front_run = Sequence('캐릭터가 멀면 달리기', c1, a1)

        c2 = Condition('ch + 150 < ai < ch + 220', self.move_front_range)
        a2 = Action('앞으로 가기', self.move_to_ch)
        SEQ_front_move = Sequence('캐릭터 앞으로 가기', c2, a2)

        c3 = Condition('ch < ai < ch + 150', self.total_pattern_range)
        a3 = Action('3가지 패턴', self.total_pattern)
        SEQ_three_pattern = Sequence('Idle', c3, a3)
        SEL_basic_pattern = Selector('패턴', SEQ_front_run, SEQ_front_move, SEQ_three_pattern)

        c4 = Condition('ai가 왼쪽에 있는 경우', self.ai_front_character)
        c5 = Condition('ai가 주인공보다 오른쪽에 있는 경우', self.ai_behind_character)

        SEQ_ai_front = Sequence('ai가 캐릭터 왼쪽에 존재', c4, a1)

        SEQ_ai_back = Sequence('ai 오른쪽에 캐릭터 존재', c5, SEL_basic_pattern)

        root = SEL_main = Selector('main', SEQ_ai_back, SEQ_ai_front)

        self.bt = BehaviorTree(root)
