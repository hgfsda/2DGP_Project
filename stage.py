from pico2d import load_image


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