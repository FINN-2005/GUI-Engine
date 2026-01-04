from pygame_template import *

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
            self.start_time = pygame.time.get_ticks()

    def update(self):
        if self.is_running:
            current = pygame.time.get_ticks()
            if current - self.start_time >= self.duration:
                if self.function: self.function()
                if self.repeat: self.start_time = current
                else: self.stop()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.start_time = 0


clamp = lambda x, mn, mx: min(max(x, mn), mx)


class Text:
    def __init__(self, default = 'Default Text'):
        self.data = default
        self.cursor = len(default)

    def move_cursor(self, dir: int):
        '''Move Cursor by Given Amount'''
        self.cursor = max(0, min(len(self.data), self.cursor + dir))

    def set_cursor(self, index: int):
        if not 0 <= index <= len(self.data): raise IndexError('Index out of bounds')
        self.cursor = index

    def __repr__(self):
        return f'{self.data[:self.cursor]}_{self.data[self.cursor:]}'

    def put_text(self, t: str):
        self.data = self.data[:self.cursor] + t + self.data[self.cursor:]
        self.cursor += len(t)

    def set_text(self, t: str):
        self.data = t
        self.cursor = len(t)

    def del_text(self, how_many_chars: int):
        dcrsr = min(how_many_chars, len(self.data[:self.cursor]))
        self.data = self.data[:self.cursor - dcrsr] + self.data[self.cursor:]
        self.cursor -= dcrsr 
        return dcrsr


class Text_Field(Text, Sprite):
    def __init__(self, 
                # util
                pos = V2(APP.HW, APP.HH),
                size = V2(300,50),

                # text
                default_text = 'Hello, World!',
                font = None,
                font_size = 32,

                # draws
                draw_bg = True,
                draw_border = True,
                draw_cursor = True,

                # extras
                border_width = 2,
                border_radius = 10,
            
                # colors
                bg_col = (0,0,0,30),
                border_col = (255,255,255,100),
                text_col = (255,255,255,255),

                # pygame
                groups = []
            
            ):
        Text.__init__(self, default_text)
        Sprite.__init__(self, *groups if isinstance(groups, list) else groups)

        # colors and draw
        self.colors = {
            'background' :   bg_col,
            'border'     :   border_col,
            'text'       :   text_col,
            'cursor'     :   (255,255,255,255)
        }
        self.draw_bg = draw_bg
        self.draw_border = draw_border
        self.draw_cursor = draw_cursor

        # utils init
        self.size = size
        self.pos = pos

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_frect(center = pos)

        self.border_width = border_width
        self.border_radius = border_radius
        self.scroll_x = 0

        # Timers
        self.cursor_timer = Timer(0.5, True, self.blink_cursor)

        self.backspace_repeat_timer = Timer(0.04, True, self.butt_backspace)
        self.backspace_start_timer = Timer(0.5, False, lambda: self.backspace_repeat_timer.start())

        self.left_repeat_timer = Timer(0.04, True, self.butt_left)
        self.left_start_timer = Timer(0.5, False, lambda: self.left_repeat_timer.start())
        
        self.right_repeat_timer = Timer(0.04, True, self.butt_right)
        self.right_start_timer = Timer(0.5, False, lambda: self.right_repeat_timer.start())
            
        self.buttons_held = {
            'ctrl'          : False,
            'right_ctrl'    : False,
            'left_ctrl'     : False,

            'shift'         : False,
            'right_shift'   : False,
            'left_shift'    : False,

            'left'          : False,
            'right'         : False,
            
            'backspace'     : False,
        }
        self.shift_map = {'1': '!','2': '@','3': '#','4': '$','5': '%','6': '^','7': '&','8': '*','9': '(','0': ')','-': '_','=': '+','[': '{',']': '}','\\': '|',';': ':',"'": '"',',': '<','.': '>','/': '?','`': '~',}


        # font stuff
        self.font = font or get_Font(font_size)
        self.font_size = font_size

        # setup stuff
        self.image.fill((0,0,0,0))
        self.image.fill(self.colors['background'])
        self.cursor_timer.start()

    def _draw(self):
        # helper stuff
        rel_rect = pygame.Rect((0,0),self.size)
        allowed_text_area = rel_rect.scale_by(0.95, 1)
        allowed_text_area.center = rel_rect.center

        # clear
        self.image.fill((0,0,0,0))
        if self.draw_bg: pygame.draw.rect(self.image, self.colors['background'], rel_rect, 0, self.border_radius)
        if self.draw_border: pygame.draw.rect(self.image, self.colors['border'], rel_rect, self.border_width, self.border_radius)

        # Core for scrolling
        max_visible = allowed_text_area.width
        cursor_px = self.get_cursor_pixel()
        text_px = self.get_text_pixel()

        # cursor is always visible
        if cursor_px - self.scroll_x < 0: self.scroll_x = cursor_px
        elif cursor_px - self.scroll_x > max_visible: self.scroll_x = cursor_px - max_visible

        # Optionally clamp scroll_x (never show empty space)
        max_scroll = max(0, text_px - max_visible)
        self.scroll_x = clamp(self.scroll_x, 0, max_scroll)

        # Render the entire text
        text_surf = self.font.render(self.data, True, self.colors['text'])

        # Blit only the visible part (draw buffer)
        surf_w = text_surf.get_width()
        surf_h = text_surf.get_height()
        left = int(self.scroll_x)
        width = min(int(max_visible), surf_w - left)
        display_rect = pygame.Rect(left, 0, max(width, 0), surf_h)
        visible_text_surf = text_surf.subsurface(display_rect)
        padded_midleft = allowed_text_area.midleft
        padded_midleft = (allowed_text_area.left, allowed_text_area.centery - visible_text_surf.get_height()//2)
        self.image.blit(visible_text_surf, padded_midleft)

        # draw cursor
        if self.draw_cursor:
            cursor_draw_x = allowed_text_area.left + (cursor_px - self.scroll_x)
            cursor_pos = V2(cursor_draw_x, allowed_text_area.centery)
            pygame.draw.line(self.image, self.colors['cursor'], cursor_pos - V2(0, self.font_size/2), cursor_pos + V2(0, self.font_size/2))

    def update(self):
        self.cursor_timer.update()
        self.backspace_start_timer.update()
        self.backspace_repeat_timer.update()
        self.left_start_timer.update()
        self.left_repeat_timer.update()
        self.right_start_timer.update()
        self.right_repeat_timer.update()
        self._draw()

    def event(self, e):
        # KEY DOWN
        if e.type == pygame.KEYDOWN:
            char = pygame.key.name(e.key)
            
            # Put Chars in Text
            if len(char) == 1:
                self.butt_char(char)
            elif char == 'space': 
                self.put_text(' ')
            
            # Del Chars
            elif char == 'backspace' and not self.buttons_held['backspace']:
                self.buttons_held['backspace'] = True
                self.butt_backspace()
                self.backspace_start_timer.start()


            # Ctrl
            elif char == 'left ctrl':
                self.buttons_held['left_ctrl'] = True 
                self.buttons_held['ctrl'] = True 
            elif char == 'right ctrl':
                self.buttons_held['right_ctrl'] = True 
                self.buttons_held['ctrl'] = True 

            # Shift
            elif char == 'left shift':
                self.buttons_held['left_shift'] = True 
                self.buttons_held['shift'] = True 
            elif char == 'right shift':
                self.buttons_held['right_shift'] = True 
                self.buttons_held['shift'] = True 

            # Move Cursor
            elif char == 'left' and not self.buttons_held['left']:
                self.buttons_held['left'] = True
                self.butt_left()
                self.left_start_timer.start()
                
            elif char == 'right' and not self.buttons_held['right']:
                self.buttons_held['right'] = True
                self.butt_right()
                self.right_start_timer.start()
                
            # Extras
            else:
                print(char)
        
        # KEY UP
        elif e.type == pygame.KEYUP:
            char = pygame.key.name(e.key)

            # Backspace
            if char == 'backspace':
                self.buttons_held['backspace'] = False
                self.backspace_start_timer.stop()
                self.backspace_repeat_timer.stop()

            # Move
            elif char == 'left':
                self.buttons_held['left'] = False
                self.left_start_timer.stop()
                self.left_repeat_timer.stop()

            elif char == 'right':
                self.buttons_held['right'] = False
                self.right_start_timer.stop()
                self.right_repeat_timer.stop()

            # Ctrl
            elif char == 'left ctrl':
                self.buttons_held['left_ctrl'] = False
                self.buttons_held['ctrl'] = self.buttons_held['right_ctrl']
            elif char == 'right ctrl':
                self.buttons_held['right_ctrl'] = False
                self.buttons_held['ctrl'] = self.buttons_held['left_ctrl']

            # Shift
            elif char == 'left shift':
                self.buttons_held['left_shift'] = False 
                self.buttons_held['shift'] = self.buttons_held['right_shift'] 
            elif char == 'right shift':
                self.buttons_held['right_shift'] = False 
                self.buttons_held['shift'] = self.buttons_held['left_shift'] 

    # |<============[ U T I L    F U N C T I O N S ]============>|
    
    def butt_char(self, char: str):
        if self.buttons_held['shift']:
            if char.isalpha(): self.put_text(char.upper())
            else: self.put_text(self.shift_map.get(char, char))
        else:
            self.put_text(char)

    def butt_backspace(self):
        if not self.buttons_held['ctrl']:
            self.del_text(1)
        else:
            if self.cursor > 0 and self.data[self.cursor - 1] == ' ':
                while self.cursor > 0 and self.data[self.cursor - 1] == ' ': self.del_text(1)           # del trailing spaces
            else:
                while self.cursor > 0 and self.data[self.cursor - 1] != ' ': self.del_text(1)           # del entire word

    def butt_left(self):
        if self.buttons_held.get('ctrl', False):
            if self.cursor > 0:
                while self.cursor > 0 and self.data[self.cursor - 1] == ' ': self.move_cursor(-1)       # move past trailing spaces
                while self.cursor > 0 and self.data[self.cursor - 1] != ' ': self.move_cursor(-1)       # move past word
        else:
            self.move_cursor(-1)

    def butt_right(self):
        if self.buttons_held.get('ctrl', False):
            if self.cursor < len(self.data):
                while self.cursor < len(self.data) and self.data[self.cursor] == ' ': self.move_cursor(1)   # move past trailing spaces
                while self.cursor < len(self.data) and self.data[self.cursor] != ' ': self.move_cursor(1)   # move past word
        else:
            self.move_cursor(1)

    def get_char_widths(self, char: str):
        if char not in Text_Field.char_widths:
            Text_Field.char_widths[char] = self.font.size(char)[0]
        return Text_Field.char_widths[char]

    def blink_cursor(self):
        self.colors['cursor'] = (255,255,255,255) if self.colors['cursor'] == (255,255,255,40) else (255,255,255,40)

    def get_cursor_pixel(self):
        return self.font.size(self.data[:self.cursor])[0]
    
    def get_text_pixel(self):
        return self.font.size(self.data)[0]

# this is the base class, make a text area out of it (alter draw function and probably use multiple `Text` Objects)
# class Text_Field(Text, Sprite):
#     def __init__(self, 
#                 # util
#                 pos = V2(APP.HW, APP.HH),
#                 size = V2(300,50),


#                 # text
#                 default_text = 'Hello, World!',
#                 font = None,
#                 font_size = 32,


#                 # draws
#                 draw_bg = True,
#                 draw_border = True,
#                 draw_cursor = True,


#                 # extras
#                 border_width = 2,
#                 border_radius = 5,
            
#                 # colors
#                 bg_col = (0,0,0,30),
#                 border_col = (255,255,255,100),
#                 text_col = (255,255,255,255),


#                 # pygame
#                 groups = []
            
#             ):
#         Text.__init__(self, default_text)
#         Sprite.__init__(self, *groups if isinstance(groups, list) else groups)


#         # colors and draw
#         self.colors = {
#             'background' :   bg_col,
#             'border'     :   border_col,
#             'text'       :   text_col,
#             'cursor'     :   (255,255,255,255)
#         }
#         self.draw_bg = draw_bg
#         self.draw_border = draw_border
#         self.draw_cursor = draw_cursor


#         # utils init
#         self.size = size
#         self.pos = pos


#         self.image = pygame.Surface(size, pygame.SRCALPHA)
#         self.rect = self.image.get_frect(center = pos)


#         self.border_width = border_width
#         self.border_radius = border_radius
        
#         # Timers
#         self.cursor_timer = Timer(0.5, True, self.blink_cursor)


#         self.backspace_repeat_timer = Timer(0.04, True, self.butt_backspace)
#         self.backspace_start_timer = Timer(0.5, False, lambda: self.backspace_repeat_timer.start())


#         self.left_repeat_timer = Timer(0.04, True, self.butt_left)
#         self.left_start_timer = Timer(0.5, False, lambda: self.left_repeat_timer.start())
        
#         self.right_repeat_timer = Timer(0.04, True, self.butt_right)
#         self.right_start_timer = Timer(0.5, False, lambda: self.right_repeat_timer.start())
            
#         self.buttons_held = {
#             'ctrl'          : False,
#             'right_ctrl'    : False,
#             'left_ctrl'     : False,


#             'shift'         : False,
#             'right_shift'   : False,
#             'left_shift'    : False,


#             'left'          : False,
#             'right'         : False,
            
#             'backspace'     : False,
#         }
#         self.shift_map = {'1': '!','2': '@','3': '#','4': '$','5': '%','6': '^','7': '&','8': '*','9': '(','0': ')','-': '_','=': '+','[': '{',']': '}','\\': '|',';': ':',"'": '"',',': '<','.': '>','/': '?','`': '~',}



#         # font stuff
#         self.font = font or get_Font(font_size)
#         self.font_size = font_size


#         # setup stuff
#         self.image.fill((0,0,0,0))
#         self.image.fill(self.colors['background'])
#         self.cursor_timer.start()



#     def _draw(self):
#         # helper stuff
#         rel_rect = pygame.Rect((0,0),self.size)
#         allowed_text_area = rel_rect.scale_by(0.95, 1)
#         allowed_text_area.center = rel_rect.center


#         # clear
#         self.image.fill((0,0,0,0))
#         if self.draw_bg: pygame.draw.rect(self.image, self.colors['background'], rel_rect, 0, self.border_radius)
#         if self.draw_border: pygame.draw.rect(self.image, self.colors['border'], rel_rect, self.border_width, self.border_radius)


#         # text stuff
#         text_surf = self.font.render(self.data, True, self.colors['text'])
#         text_rect = text_surf.get_frect(midleft = allowed_text_area.midleft)


#         # draw text on image (clipped)
#         prev_clip = self.image.get_clip()
#         self.image.set_clip(allowed_text_area)
#         self.image.blit(text_surf, text_rect)
#         self.image.set_clip(prev_clip)


#         # cursor
#         if self.draw_cursor:
#             cursor_pos = V2(clamp(allowed_text_area.left + self.font.size(self.data[:self.cursor])[0], mn=allowed_text_area.left, mx=allowed_text_area.right), allowed_text_area.centery)
#             pygame.draw.line(self.image, self.colors['cursor'], cursor_pos - V2(0, self.font_size/2), cursor_pos + V2(0, self.font_size/2))




#     def update(self):
#         self.cursor_timer.update()
#         self.backspace_start_timer.update()
#         self.backspace_repeat_timer.update()
#         self.left_start_timer.update()
#         self.left_repeat_timer.update()
#         self.right_start_timer.update()
#         self.right_repeat_timer.update()
#         self._draw()



#     def event(self, e):
#         # KEY DOWN
#         if e.type == pygame.KEYDOWN:
#             char = pygame.key.name(e.key)
            
#             # Put Chars in Text
#             if len(char) == 1:
#                 self.butt_char(char)
#             elif char == 'space': 
#                 self.put_text(' ')
            
#             # Del Chars
#             elif char == 'backspace' and not self.buttons_held['backspace']:
#                 self.buttons_held['backspace'] = True
#                 self.butt_backspace()
#                 self.backspace_start_timer.start()



#             # Ctrl
#             elif char == 'left ctrl':
#                 self.buttons_held['left_ctrl'] = True 
#                 self.buttons_held['ctrl'] = True 
#             elif char == 'right ctrl':
#                 self.buttons_held['right_ctrl'] = True 
#                 self.buttons_held['ctrl'] = True 


#             # Shift
#             elif char == 'left shift':
#                 self.buttons_held['left_shift'] = True 
#                 self.buttons_held['shift'] = True 
#             elif char == 'right shift':
#                 self.buttons_held['right_shift'] = True 
#                 self.buttons_held['shift'] = True 


#             # Move Cursor
#             elif char == 'left' and not self.buttons_held['left']:
#                 self.buttons_held['left'] = True
#                 self.butt_left()
#                 self.left_start_timer.start()
                
#             elif char == 'right' and not self.buttons_held['right']:
#                 self.buttons_held['right'] = True
#                 self.butt_right()
#                 self.right_start_timer.start()
                
#             # Extras
#             else:
#                 print(char)
        
#         # KEY UP
#         elif e.type == pygame.KEYUP:
#             char = pygame.key.name(e.key)


#             # Backspace
#             if char == 'backspace':
#                 self.buttons_held['backspace'] = False
#                 self.backspace_start_timer.stop()
#                 self.backspace_repeat_timer.stop()


#             # Move
#             elif char == 'left':
#                 self.buttons_held['left'] = False
#                 self.left_start_timer.stop()
#                 self.left_repeat_timer.stop()


#             elif char == 'right':
#                 self.buttons_held['right'] = False
#                 self.right_start_timer.stop()
#                 self.right_repeat_timer.stop()


#             # Ctrl
#             elif char == 'left ctrl':
#                 self.buttons_held['left_ctrl'] = False
#                 self.buttons_held['ctrl'] = self.buttons_held['right_ctrl']
#             elif char == 'right ctrl':
#                 self.buttons_held['right_ctrl'] = False
#                 self.buttons_held['ctrl'] = self.buttons_held['left_ctrl']


#             # Shift
#             elif char == 'left shift':
#                 self.buttons_held['left_shift'] = False 
#                 self.buttons_held['shift'] = self.buttons_held['right_shift'] 
#             elif char == 'right shift':
#                 self.buttons_held['right_shift'] = False 
#                 self.buttons_held['shift'] = self.buttons_held['left_shift'] 





#     # |<============[ U T I L    F U N C T I O N S ]============>|
    
#     def butt_char(self, char: str):
#         if self.buttons_held['shift']:
#             if char.isalpha(): self.put_text(char.upper())
#             else: self.put_text(self.shift_map.get(char, char))
#         else:
#             self.put_text(char)



#     def butt_backspace(self):
#         if not self.buttons_held['ctrl']:
#             self.del_text(1)
#         else:
#             if self.cursor > 0 and self.data[self.cursor - 1] == ' ':
#                 while self.cursor > 0 and self.data[self.cursor - 1] == ' ': self.del_text(1)           # del trailing spaces
#             else:
#                 while self.cursor > 0 and self.data[self.cursor - 1] != ' ': self.del_text(1)           # del entire word



#     def butt_left(self):
#         if self.buttons_held.get('ctrl', False):
#             if self.cursor > 0:
#                 while self.cursor > 0 and self.data[self.cursor - 1] == ' ': self.move_cursor(-1)       # move past trailing spaces
#                 while self.cursor > 0 and self.data[self.cursor - 1] != ' ': self.move_cursor(-1)       # move past word
#         else:
#             self.move_cursor(-1)



#     def butt_right(self):
#         if self.buttons_held.get('ctrl', False):
#             if self.cursor < len(self.data):
#                 while self.cursor < len(self.data) and self.data[self.cursor] == ' ': self.move_cursor(1)   # move past trailing spaces
#                 while self.cursor < len(self.data) and self.data[self.cursor] != ' ': self.move_cursor(1)   # move past word
#         else:
#             self.move_cursor(1)



#     def get_char_widths(self, char: str):
#         if char not in Text_Field.char_widths:
#             Text_Field.char_widths[char] = self.font.size(char)[0]
#         return Text_Field.char_widths[char]



#     def blink_cursor(self):
#         self.colors['cursor'] = (255,255,255,255) if self.colors['cursor'] == (255,255,255,40) else (255,255,255,40)



class run(APP):
    def setup(self):
        self.Text_Group = Group(
            Text_Field(pos=V2(APP.HW, APP.HH - 100), font_size=20),
            Text_Field(pos=V2(APP.HW, APP.HH + 100)),
        )

    def draw(self):
        self.Text_Group.draw()

    def update(self):
        self.Text_Group.update()

    def event(self, e):
        self.Text_Group.event(e)

run()