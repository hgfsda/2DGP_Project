from pico2d import load_image, SDL_KEYDOWN, SDLK_UP, SDLK_DOWN


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


class StartStage:
    @staticmethod
    def enter(stage, e):
        if up_down(e) or down_down(e):
            stage.check_y = 1 - stage.check_y

    @staticmethod
    def exit(stage, e):
        pass

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


class StateMachine:
    def __init__(self, stage):
        self.stage = stage
        self.cur_state = StartStage
        self.transitions = {
            StartStage: {up_down: StartStage, down_down: StartStage}
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
        self.frame = 0
        self.check_y = 0    # 시작 화면에서 start exit 표시해주는 화살표 위치
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

