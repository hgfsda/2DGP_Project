from pico2d import load_image, load_music

character_stage = 3  # 주인공 스테이지 위치
ai_stage = 3  # ai 스테이지 위치      / 스테이지 위치는 |주인공 - ai| / 2로 계산

class Stage:
    def __init__(self):
        global character_stage
        global ai_stage
        self.stage_image = load_image('image\\stage.png')
        self.frame = 0
        self.x = 400  # 배경 위치
        character_stage = 3
        ai_stage = 3
        self.bgm = load_music('sound\\background.mp3')
        self.bgm.set_volume(5)
        self.bgm.repeat_play()

    def update(self):
        pass

    def draw(self):
        self.stage_image.clip_draw(0, 1360 - (660 * abs(character_stage - ai_stage) // 2), 1190, 600, self.x,
                                   300, 1800, 600)
