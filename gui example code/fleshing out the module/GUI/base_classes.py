from .util_classes import InputState, V4
from pygame import Vector2 as V2


'''
Widget:
  -> Container      # row col grids
  -> Interactive   # button slider toggles
  -> Static         # div image text
'''


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
