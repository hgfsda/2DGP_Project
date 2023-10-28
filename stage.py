from pico2d import load_image, SDL_KEYDOWN, SDLK_UP, SDLK_DOWN, SDLK_RETURN

import game_world
from character import Character

def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def enter_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RETURN


class StartStage:
    @staticmethod
    def enter(stage, e):
        if up_down(e) or down_down(e):
            stage.check_y = 1 - stage.check_y

    @staticmethod
    def exit(stage, e):
        if enter_down(e) and stage.check_y == 1:
            stage.running = False

    @staticmethod
    def do(stage):
        stage.frame = stage.frame - 10
        if stage.frame <= -1300:
            stage.frame = -100

    @staticmethod
    def draw(stage):
        stage.stage_image.clip_draw(0, 0, 2200, 600, 1100 + stage.frame, 300, 2200, 600)   # 배경
        stage.start_image.clip_draw(0, 150, 500, 100, 465, 450, 800, 200)                  # 펜싱 게임 제목
        stage.start_image.clip_draw(0, 80, 200, 60, 420, 250, 400, 120)                    # start
        stage.start_image.clip_draw(0, 10, 200, 60, 465, 150, 400, 120)                    # exit
        stage.start_image.clip_draw(200, 10, 30, 60, 165, 260 - (110 * stage.check_y), 60, 120)  # 화살표 위치


class PlayStage:
    @staticmethod
    def enter(stage, e):
        stage.character_create()

    @staticmethod
    def exit(stage, e):
        pass

    @staticmethod
    def do(stage):
        pass

    @staticmethod
    def draw(stage):
        stage.play_stage_image.clip_draw(0, 1360 - (660*abs(stage.character_stage - stage.ai_stage)//2), 1190, 600, stage.x, 300, 1800, 600)


class WinStage:
    @staticmethod
    def enter(stage, e):
        pass

    @staticmethod
    def exit(stage, e):
        pass

    @staticmethod
    def do(stage):
        pass

    @staticmethod
    def draw(stage):
        stage.final_image.clip_draw(0, 0, 1200, 600, 400, 300, 800, 600)


class LoseStage:
    @staticmethod
    def enter(stage, e):
        pass

    @staticmethod
    def exit(stage, e):
        pass

    @staticmethod
    def do(stage):
        pass

    @staticmethod
    def draw(stage):
        stage.final_image.clip_draw(0, 0, 1200, 600, 400, 300, 800, 600)

class StateMachine:
    def __init__(self, stage):
        self.stage = stage
        self.cur_state = StartStage
        self.transitions = {
            StartStage: {up_down: StartStage, down_down: StartStage, enter_down: PlayStage},
            PlayStage: {enter_down: PlayStage},
            WinStage: {},
            LoseStage: {},
        }

    def start(self):
        self.cur_state.enter(self.stage, ('START', 0))

    def update(self):
        self.cur_state.do(self.stage)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.stage, e)
                self.cur_state = next_state
                self.cur_state.enter(self.stage, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.stage)


class Stage:
    def __init__(self):
        self.stage_image = load_image('start_stage.png')
        self.start_image = load_image('start.png')
        self.play_stage_image = load_image('stage.png')
        self.final_image = load_image('final_stage.png')
        self.frame = 0
        self.check_y = 0    # 시작 화면에서 start exit 표시해주는 화살표 위치
        self.x = 400        # 배경 위치
        self.character_stage = 3          # 주인공 스테이지 위치
        self.ai_stage = 3                 # ai 스테이지 위치      / 스테이지 위치는 |주인공 - ai| / 2로 계산
        self.running = True
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def character_create(self):
        character = Character()
        game_world.add_object(character, 1)