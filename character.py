from pico2d import load_image, delay


class Character:
    def __init__(self):
        self.x, self.y = 400, 150
        self.frame = 0
        self.image = load_image('character.png')

    def update(self):
        self.frame = (self.frame + 1) % 4
        delay(0.07)

    def draw(self):
        self.image.clip_draw(self.frame * 45, 495, 45, 45, self.x, self.y, 135, 135)