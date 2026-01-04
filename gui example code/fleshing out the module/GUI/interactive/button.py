from ..base_classes import Interactive
from ..util_classes import V4

from pygame import Vector2 as V2

class Button(Interactive):
    def __init__(
            self,
            center_pos = V2(100,100),
            total_size = V2(200,100),
            padding = V4(5,5,5,5),
            margin = V4(),

            draw_text = True,
            text = '_default text_',
            text_size = 30,
            text_color = (255,255,255,255),
            text_draw_outline = False,
            text_col_outline = (0,0,0,255),

            allow_hold_repeat = True,
            hold_repeat_interval = 0.5,
            hold_repeat_start_delay = 0.5,
            allow_double_click = True,
            double_click_interval = 0.5,

            on_hover_callback = None,
            on_click_callback = None,
            on_hold_callback = None,
            on_double_click_callback = None,
            on_focus_callback = None,
            on_blur_callback = None,
            on_keydown_callback = None,
            on_keyup_callback = None,

            visible = True,
            enabled = True,
            flex_grow = 1,

            tooltip = 'This is Default Text!',
            tooltip_size = 30,

            top_outline_width = 1,
            bottom_outline_width = 1,

            top_color = (200, 100, 200, 255),
            bottom_color = (150, 50, 150, 255),
            top_outline_color = (0,0,0,0),
            bottom_outline_color = (0,0,0,0),
            
            top_hover_color = (200, 200, 200, 255),
            bottom_hover_color = (150, 150, 150, 255),
            top_outline_hover_color = (0,0,0,0),
            bottom_outline_hover_color = (0,0,0,0),

            top_active_color = (250, 150, 250, 255),
            bottom_active_color = (200, 100, 200, 255),
            top_outline_active_color = (0,0,0,0),
            bottom_outline_active_color = (0,0,0,0),
            

    ):
        super().__init__()

        