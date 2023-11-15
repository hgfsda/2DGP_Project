from pico2d import load_image, get_time


class System:
    def __init__(self):
        self.num_image = load_image('image\\Num.png')
        self.set_image = load_image('image\\set_check.png')
        self.play_time = 90
        self.start_time = get_time()
        self.character_kill = 0
        self.ai_kill = 0

    def update(self):
        if self.play_time > 0:
            self.play_time = 90 - get_time()

    def draw(self):
        # 타이머
        self.num_image.clip_draw(100 * (int)(self.play_time % 100 // 10), 0, 100, 100, 360, 530, 80, 100)
        self.num_image.clip_draw(100 * (int)(self.play_time % 10), 0, 100, 100, 440, 530, 80, 100)

        # 주인공 세트 확인
        self.set_image.clip_draw(0, 300, 300, 300, 290, 550, 40, 40)
        self.set_image.clip_draw(0, 300, 300, 300, 240, 550, 40, 40)

        # 적 세트 확인
        self.set_image.clip_draw(0, 300, 300, 300, 510, 550, 40, 40)
        self.set_image.clip_draw(0, 300, 300, 300, 560, 550, 40, 40)

        # 주인공 킬 수 확인
        self.num_image.clip_draw(100 * (self.character_kill % 100 // 10), 0, 100, 100, 270, 500, 30, 30)
        self.num_image.clip_draw(100 * (self.character_kill % 10), 0, 100, 100, 300, 500, 30, 30)

        # 적 킬 수 확인
        self.num_image.clip_draw(100 * (self.ai_kill % 100 // 10), 0, 100, 100, 500, 500, 30, 30)
        self.num_image.clip_draw(100 * (self.ai_kill % 10), 0, 100, 100, 530, 500, 30, 30)