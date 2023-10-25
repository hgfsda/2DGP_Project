from pico2d import load_image


class StartStage:
    def __init__(self):
        self.stage_image = load_image('start_stage.png')
        self.start_image = load_image('start.png')
        self.frame = 0

    def draw(self):
        self.stage_image.clip_draw(0, 0, 2200, 600, 1100 + self.frame, 300, 2200, 600)
        self.start_image.clip_draw(0, 150, 500, 100, 465, 450, 800, 200)
        self.start_image.clip_draw(0, 80, 200, 60, 420, 250, 400, 120)
        self.start_image.clip_draw(0, 10, 200, 60, 465, 150, 400, 120)
        self.start_image.clip_draw(200, 10, 30, 60, 165, 260, 60, 120)

    def update(self):
        self.frame = self.frame - 10
        if self.frame <= -1300:
            self.frame = -100