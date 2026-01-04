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
        '''duration in seconds, callback is function'''
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
            
