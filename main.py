from pico2d import open_canvas, close_canvas

import game_framework
# import title_mode as start_mode
# import project as start_mode
# import win_stage as start_mode
import lose_stage as start_mode
# import result as start_mode


open_canvas()
game_framework.run(start_mode)
close_canvas()
