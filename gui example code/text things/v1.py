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



# ============================================================
#   T E X T   F I E L D
# ============================================================

class Text_Field:
    def __init__(self, pos: V2, size: V2, font=None):
        # --- Text state ---
        self.text = ''
        self.ctrl_held = False

        # --- Cursor state ---
        self.cursor_index = 0
        self.cursor_pos = 0     # in pixels
        self.draw_cursor = True
        def blink(): self.draw_cursor = not self.draw_cursor
        self.cursor_blink_timer = Timer(0.5, True, blink)

        # --- Visuals ---
        self.pos = pos
        self.size = size
        self.font = font or get_Font()
        self.base_img = pygame.Surface(size, pygame.SRCALPHA)

        self.keep_center()
        self.cursor_blink_timer.start()



    # --------------------------------------------------------
    #   D R A W I N G
    # --------------------------------------------------------

    def draw(self, screen):
        # Background
        # self.base_img.fill((0, 0, 0, 0))
        self.base_img.fill((0, 0, 0, 30))

        # Render text
        self.text_surf = self.font.render(self.text, True, (255, 255, 255, 255))
        self.text_surf_size = V2(self.text_surf.get_size())

        # Decide how to draw (scrolling or static)
        if self.text_surf_size[0] >= self.size[0]:
            self._draw_scrolling()
        else:
            self._draw_static()

        # Blit to screen
        screen.blit(self.base_img, self.center_pos)


    def _draw_static(self):
        """Draw text centered if it fits in the box."""
        self.base_img.blit(self.text_surf, self.size / 2 - self.text_surf_size / 2)
        if self.draw_cursor:
            self.cursor_pos = max(min(self.size[0] - 1, self.cursor_pos), 0)
            t_h = self.font.get_height()
            pygame.draw.line(self.base_img, (255,255,255,255), V2(self.size[0] / 2 + self.cursor_pos / 2, self.size.y / 2 - t_h / 2), V2(self.size[0]   / 2 + self.cursor_pos / 2, self.size.y / 2 + t_h / 2))


    def _draw_scrolling(self):
        """Draw text with horizontal scrolling (not yet implemented)."""
        ...


    # --------------------------------------------------------
    #   E V E N T   H A N D L I N G
    # --------------------------------------------------------

    def event_call(self, e):
        if e.type == pygame.KEYDOWN:

            if e.key in (pygame.K_LCTRL, pygame.K_RCTRL): 
                self.ctrl_held = True

            elif e.key == pygame.K_LEFT:
                self.cursor_index = max(0, min(len(self.text), self.cursor_index - 1))
                self.cursor_pos = self.font.size(self.text[:self.cursor_index])[0]

            elif e.key == pygame.K_RIGHT:
                self.cursor_index = max(0, min(len(self.text), self.cursor_index + 1))
                self.cursor_pos = self.font.size(self.text[:self.cursor_index])[0]


            # Handle character / buffer updates
            self.update_buffer(e.key)

        elif e.type == pygame.KEYUP:
            if e.key in (pygame.K_LCTRL, pygame.K_RCTRL): self.ctrl_held = False


    # --------------------------------------------------------
    #   T E X T   B U F F E R   L O G I C
    # --------------------------------------------------------

    def update_buffer(self, key):
        """Update internal text buffer based on key input."""
        if key == pygame.K_BACKSPACE:
            self._handle_backspace()
        else:
            self._handle_character_input(key)


    def _handle_backspace(self):
        """Handles deleting characters or words (Ctrl+Backspace)."""
        if not self.text: return

        # Delete last word
        if self.ctrl_held: 
            words = self.text.split(' ')
            self.cursor_pos -= self.font.size(' ' + words[-1])[0]
            self.cursor_index -= len(words[-1]) + 1
            self.text = ' '.join(words[:-1])

        # Delete last character
        else:
            self.cursor_pos -= self.font.size(self.text[-1])[0]
            self.cursor_index -= 1
            self.text = self.text[:-1]

        self.dirty_text = True


    def _handle_character_input(self, key):
        """Handles adding characters to the text buffer."""
        char = pygame.key.name(key)

        if len(char) == 1: 
            self.text += char
            self.cursor_pos += self.font.size(char)[0]
            self.cursor_index += 1
        elif char == 'space': 
            self.text += ' '
            self.cursor_pos += self.font.size(' ')[0]
            self.cursor_index += 1

    # --------------------------------------------------------
    #   U P D A T E
    # --------------------------------------------------------

    def update(self):
        self.cursor_blink_timer.update()

    def keep_center(self):
        """Recalculate the top-left corner for center positioning."""
        self.center_pos = self.pos - self.size / 2



# ============================================================
#   A P P   R U N N E R
# ============================================================

class run(APP):
    def setup(self):
        self.f = Text_Field(V2(APP.HW, APP.HH), V2(300, 150))

    def draw(self):
        self.f.draw(self.screen)

    def update(self):
        self.f.update()
        ...

    def event(self, e):
        self.f.event_call(e)
        ...


# ============================================================
#   M A I N
# ============================================================

run()