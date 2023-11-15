from pico2d import load_image, get_time


class System:
    def __init__(self):
        self.num_image = load_image('image\\Num.png')
        self.set_image = load_image('image\\set_check.png')
        self.play_time = 90
        self.start_time = get_time()

    def update(self):
        if self.play_time > 0:
            self.play_time = 90 - get_time()

    def draw(self):
        self.num_image.clip_draw(100 * (int)(self.play_time % 100 // 10), 0, 100, 100, 360, 530, 80, 100)
        self.num_image.clip_draw(100 * (int)(self.play_time % 10), 0, 100, 100, 440, 530, 80, 100)
