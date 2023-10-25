from pico2d import load_image


class StartStage:

    @staticmethod
    def enter(stage):
        stage.frame = 0

    @staticmethod
    def exit(stage):
        pass

    @staticmethod
    def do(stage):
        stage.frame = stage.frame - 10
        if stage.frame <= -1300:
            stage.frame = -100

    @staticmethod
    def draw(stage):
        stage.stage_image.clip_draw(0, 0, 2200, 600, 1100 + stage.frame, 300, 2200, 600)
        stage.start_image.clip_draw(0, 150, 500, 100, 465, 450, 800, 200)
        stage.start_image.clip_draw(0, 80, 200, 60, 420, 250, 400, 120)
        stage.start_image.clip_draw(0, 10, 200, 60, 465, 150, 400, 120)
        stage.start_image.clip_draw(200, 10, 30, 60, 165, 260, 60, 120)


class StateMachine:
    def __init__(self, stage):
        self.stage = stage
        self.cur_state = StartStage

    def start(self):
        self.cur_state.enter(self.stage)

    def update(self):
        self.cur_state.do(self.stage)

    def handle_event(self, e):
        pass

    def draw(self):
        self.cur_state.draw(self.stage)


class Stage:
    def __init__(self):
        self.stage_image = load_image('start_stage.png')
        self.start_image = load_image('start.png')
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.draw()