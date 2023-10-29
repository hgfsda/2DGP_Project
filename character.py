from pico2d import load_image, delay


class Run:

    @staticmethod
    def enter(character, e):
        pass

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 4
        delay(0.07)

    @staticmethod
    def draw(character):
        character.image.clip_draw(character.frame * 45, 90, 45, 45, character.x, 150, 135, 135)


class Move:

    @staticmethod
    def enter(character, e):
        pass

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 4
        delay(0.07)

    @staticmethod
    def draw(character):
        character.image.clip_draw(character.frame * 45, 450 - (135 * character.sword_position), 45, 45, character.x,
                                  150, 135, 135)


class Idle:
    @staticmethod
    def enter(character, e):
        pass

    @staticmethod
    def exit(character, e):
        pass

    @staticmethod
    def do(character):
        character.frame = (character.frame + 1) % 4
        delay(0.07)

    @staticmethod
    def draw(character):
        character.image.clip_draw(character.frame * 45, 495 - (135 * character.sword_position), 45, 45, character.x,
                                  150, 135, 135)


class StateMachine:
    def __init__(self, character):
        self.character = character
        self.cur_state = Run
        self.transitions = {
            Idle: {},
            Move: {},
            Run: {},
        }

    def start(self):
        self.cur_state.enter(self.character, ('START', 0))

    def update(self):
        self.cur_state.do(self.character)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.character, e)
                self.cur_state = next_state
                self.cur_state.enter(self.character, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.character)


class Character:
    def __init__(self):
        self.x = 400
        self.sword_position = 1  # 검의 위치 / 상단 2 , 중단 1, 하단 0
        self.dir = 0             # 캐릭터의 방향
        self.frame = 0
        self.image = load_image('character.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
