'''./main.py'''
'''
from pygame_template import *
from GUI import *


class run(APP):
    def setup(self):
        self.manager = Widget_Manager()     # must initialise this

        Button()        # automatically added to the widget manager

    def draw(self):
        self.manager.draw(self.screen)

    def update(self):
        self.manager.update(self.dt)



run()
'''

'''./ideas.md'''
'''
# UI Widgets Documentation

## Widget (Root)
**Purpose:** Fundamental building block for all UI elements.  
Provides geometry, hierarchy, visibility, and update/draw control.  

### Key Attributes
- `pos: V2` → Widget’s center position.  
- `size: V2` → Widget’s width & height.  
- `padding: V4` → Space inside widget boundary `[left, top, right, bottom]`.  
- `margin: V4` → Space outside widget boundary `[left, top, right, bottom]`.  
- `children: list[Widget]` → Optional child widgets (for recursive updates/draws).  
- `parent: Widget | None` → Parent widget reference.  
- `visible: bool` → Whether the widget should be drawn.  
- `enabled: bool` → Whether the widget can interact with events.  
- `is_dirty: bool` → Flag indicating widget needs update/redraw.  
- `is_child: bool` → Whether this widget is a child (affects recursive update/draw).  
- `flex_grow: int` → CSS's Flex Grow.  


---
## Container
**Purpose:** Layout and organize children widgets.

### Types
- **Row**: Horizontally arranges children.  
- **Col**: Vertically arranges children.  
- **Div**: Generic container for arbitrary grouping with no strict layout.  
- **Grid**: Arranges children in a 2D grid with rows and columns.  

### Key Parameters
- `grid_size` (V2: for grid, row, col)  
- `spacing` (V2: for grid, row, col)  
- `alignment` (start, center, end)  

### Alignments Options for Both Axes
- `start` — Align items to the start (left/top) of the container.  
- `center` — Align items centered in the container.  
- `end` — Align items to the end (right/bottom) of the container.  
- `stretch` — Expand items to fill the available space.  
- `space-between` — Distribute items evenly, first at start and last at end.  
- `space-around` — Distribute items evenly with equal space around each item.  
- `space-evenly` — Distribute items with equal space between all items and container edge  

---

## Static
**Purpose:** Display-only, non-interactive visuals.

### Types
- **Canvas**: Blank drawable surface for custom rendering.  
- **Image**: Shows image content from source.  
- **Video**: Embeds video playback.  

---

## Interactive
**Purpose:** User input and interactive elements.

### Types
- **Button**: Clickable button.  
- **Slider**: Adjustable value slider.  
- **Toggle**: Switch or checkbox.  
- **Text**: Editable single-line text input.  
- **Input Field**: Editable multi-line text input.  
- **Paragraph Field**: Larger multi-line text blocks.  
- **Menus**: Dropdown or popup menus.  

### Key Parameters
- `hovered`, `pressed`, `focused` states (bool)  
- `event callbacks` (`on_click`, `on_hover`, `on_keydown`, etc.)  
- `value/state` storage depending on widget  

---

## Future Extras
Examples of potential extended UI features:
- Tables  
- Joysticks  
- Vector graphics  
- Animations  


---
# Interactive
## Button
a class for buttons
'''


'''./GUI/__init__.py'''
'''
from .util_classes import InputState, Timer, V4
from .base_classes import Widget, Interactive, Container, Static
from .interactive import Button
from .manager import Widget_Manager

from .interactive import *
'''


'''./GUI/base_classes.py'''
'''
from .util_classes import InputState, V4
from pygame import Vector2 as V2


# Widget:
#   -> Container      # row col grids
#   -> Interactive   # button slider toggles
#   -> Static         # div image text



class Widget:
    def __init__(self):
        self.pos = V2()                      # center pos
        self.size = V2()                     # total size

        self.padding = V4()                  # padding: [left, top, right, bottom]
        self.margin = V4()                   # margin: [left, top, right, bottom]
        
        self.children: list["Widget"] = []   # list of children widgets
        self.parent: Widget = None           # parent widget

        self.visible = True                  # draw or not
        self.enabled = True                  # interact or not

        self.is_dirty = True                 # flag to update logic
        self.is_child = False                # flag for recursive update logic in containers

        self.flex_grow = 1                   # CSS's Flex Grow

    @property
    def top(self): return self.pos.y - self.size.y / 2
    @top.setter
    def top(self, amount): self.pos.y = amount + self.size.y / 2

    @property
    def right(self): return self.pos.x + self.size.x / 2
    @right.setter
    def right(self, amount): self.pos.x = amount - self.size.x / 2

    @property
    def bottom(self): return self.pos.y + self.size.y / 2
    @bottom.setter
    def bottom(self, amount): self.pos.y = amount - self.size.y / 2

    @property
    def left(self): return self.pos.x - self.size.x / 2
    @left.setter
    def left(self, amount): self.pos.x = amount + self.size.x / 2

    @property
    def centerx(self): return self.pos.x
    @centerx.setter
    def centerx(self, amount): self.pos.x = amount

    @property
    def centery(self): return self.pos.y
    @centery.setter
    def centery(self, amount): self.pos.y = amount

    @property
    def center(self): return self.pos
    @center.setter
    def center(self, amount: V2|tuple[float]): self.pos = V2(amount)

    @property
    def topleft(self): return self.pos - self.size / 2
    @topleft.setter
    def topleft(self, amount: V2|tuple[float]): self.pos = V2(amount) + self.size / 2
    
    @property
    def midtop(self): return V2(self.pos.x, self.pos.y - self.size.y / 2)
    @midtop.setter
    def midtop(self, amount: V2|tuple[float]): self.pos = V2(amount[0], amount[1] + self.size.y / 2)
    
    @property
    def topright(self): return V2(self.pos.x + self.size.x / 2, self.pos.y - self.size.y / 2)
    @topright.setter
    def topright(self, amount: V2|tuple[float]): self.pos = V2(amount[0] - self.size.x / 2, amount[1] + self.size.y / 2)
    
    @property
    def midright(self): return V2(self.pos.x + self.size.x / 2, self.pos.y)
    @midright.setter
    def midright(self, amount: V2|tuple[float]): self.pos = V2(amount[0] - self.size.x / 2, amount[1])
    
    @property
    def bottomright(self): return self.pos + self.size / 2
    @bottomright.setter
    def bottomright(self, amount: V2|tuple[float]): self.pos = V2(amount) - self.size / 2

    @property
    def midbottom(self): return V2(self.pos.x, self.pos.y + self.size.y / 2)
    @midbottom.setter
    def midbottom(self, amount: V2|tuple[float]): self.pos = V2(amount[0], amount[1] - self.size.y / 2)
    
    @property
    def bottomleft(self): return V2(self.pos.x - self.size.x / 2, self.pos.y + self.size.y / 2)
    @bottomleft.setter
    def bottomleft(self, amount: V2|tuple[float]): self.pos = V2(amount[0] + self.size.x / 2, amount[1] - self.size.y / 2)

    @property
    def midleft(self): return V2(self.pos.x - self.size.x / 2, self.pos.y)
    @midleft.setter
    def midleft(self, amount: V2|tuple[float]): self.pos = V2(amount[0] + self.size.x / 2, amount[1])


class Interactive(Widget):
    def __init__(self):
        super().__init__()

        self.hovered = False
        self.pressed = False
        self.focused = False
        
        self.last_clicked_time = 0     # in mili seconds, for double click detection

    def _on_hover(self, state: InputState) -> None : ...
    def _on_click(self, state: InputState) -> None : ...
    def _on_hold(self, state: InputState) -> None : ...
    def _on_double_click(self, state: InputState) -> None : ...
    def _on_focus(self, state: InputState) -> None : ...
    def _on_blur(self, state: InputState) -> None : ...
    def _on_keydown(self, state: InputState) -> None : ...
    def _on_keyup(self, state: InputState) -> None : ...



class Container(Widget):
    possible_alignments = ['start', 'center', 'end', 'stretch', 'space-between', 'space-around', 'space-evenly']
    def __init__(self):
        super().__init__()

        self.grid_size = V2()           # xy -> grid, x -> row, y -> col
        self.spacing = V2(5, 5)         # in pixels, xy -> grid, x -> row, y -> col
        
        self.alignment = {              # default is center on both
            'main-axis'  : 'center',
            'cross-axis' : 'center'
        }



class Static(Widget):
    def __init__(self):
        super().__init__()

'''


'''./GUI/manager.py'''
'''
class Widget_Manager:
    layers = []
    def __init__(self, gui='gui.json'):
        import json
        with open(gui, 'r') as F:
            json_data = json.load(F)
        

    def draw(self, screen):
        for layer in self.layers:
            for wdgt in layer:
                wdgt.draw(screen)

    def update(self, dt):
        for layer in self.layers:
            for wdgt in layer:
                wdgt.update(dt)

    
'''


'''./GUI/util_classes.py'''
'''
from pygame.mouse import get_pressed as m_prsd
from pygame.mouse import get_just_pressed as m_jst_prsd
from pygame.mouse import get_pos as m_ps
from pygame.mouse import get_rel as m_rl

from pygame.key import get_pressed as k_prsd
from pygame.key import get_just_pressed as k_jst_prsd
from pygame.key import get_just_released as k_jst_rlsd

from pygame.time import get_ticks


class V4:
    def __init__(self, left=0., top=0., right=0., bottom=0.):
        self._data = [left, top, right, bottom]

    @property
    def left(self) -> float: return self._data[0]
    @left.setter
    def left(self, data: float): self._data[0] = data

    @property
    def top(self) -> float: return self._data[1]
    @top.setter
    def top(self, data: float): self._data[1] = data

    @property
    def right(self) -> float: return self._data[2]
    @right.setter
    def right(self, data: float): self._data[2] = data

    @property
    def bottom(self) -> float: return self._data[3]
    @bottom.setter
    def bottom(self, data: float): self._data[3] = data


class InputState:
    def __init__(self):
        self.mkeys_just_pressed = m_jst_prsd()        # mouse button: [left, middle, right]
        self.mkeys = m_prsd()                         # mouse button: [left, middle, right]
        self.mpos = m_ps()                            # mouse pos
        self.mpos_rel = m_rl()                        # mouse pos

        self.key_pressed = k_prsd()                   # keyboard pressed
        self.key_just_pressed = k_jst_prsd()          # keyboard just pressed
        self.key_just_released = k_jst_rlsd()         # keyboard just released


class Timer:
    def __init__(self, duration: float = 1, repeat: bool = False, callback = None):
        # duration in seconds, callback is function
        self.duration = duration * 1000
        self.repeat = repeat
        self.function = callback

        self.start_time = 0
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = get_ticks()

    def update(self):
        if self.is_running:
            current = get_ticks()
            if current - self.start_time >= self.duration:
                if self.function: self.function()
                if self.repeat: self.start_time = current
                else: self.stop()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.start_time = 0
            
'''


'''./GUI/interactive/__init__.py'''
'''
from .button import Button
'''


'''./GUI/interactive/button.py'''
'''
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

        
'''