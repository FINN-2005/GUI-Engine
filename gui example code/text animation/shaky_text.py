from pygame_template import *



FONT = get_Font()

class Char:
    def __init__(self, char):
        self.image = FONT.render(char, False, Color.white)
        self.rect = self.image.get_frect()

        self.width = self.rect.w
        self.pos = V2()
        self.vibrating_pos = V2()
        self.visible = True

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.vibrating_pos)

    def update(self):
        self.vibrating_pos = self.pos + V2(random.randint(-2,2),random.randint(-2,2))


class String_handler:
    def __init__(self, string: str, pos: V2, reveal_speed=100):
        self.string = string
        self.letters = []
        self.pos = pos
        
        self.reveal_speed = reveal_speed
        self.current_index = 0
        self.last_reveal_time = pygame.time.get_ticks()

        last_width = 0
        for c in self.string:
            char_sprite = Char(c)
            char_sprite.pos = self.pos.copy()
            char_sprite.pos.x += last_width
            last_width += char_sprite.width
            self.letters.append(char_sprite)

        for letter in self.letters:
            letter.visible = False

    def update(self):
        # Time-based reveal
        now = pygame.time.get_ticks()
        if self.current_index < len(self.letters):
            if now - self.last_reveal_time >= self.reveal_speed:
                self.letters[self.current_index].visible = True
                self.current_index += 1
                self.last_reveal_time = now

        # Update visible letters only
        for i in range(self.current_index):
            self.letters[i].update()

    def draw(self, screen):
        for i in range(self.current_index):
            self.letters[i].draw(screen)


class ParagraphHandler:
    def __init__(self, paragraph: str, start_pos: V2, line_spacing=10, reveal_speed=100, max_width=None):
        self.lines = []
        self.start_pos = start_pos
        self.line_spacing = line_spacing
        self.reveal_speed = reveal_speed
        self.max_width = max_width

        self.current_line_index = 0  # Only reveal up to this line
        self._create_lines(paragraph)

    def _create_lines(self, paragraph):
        raw_lines = paragraph.split('\n')
        y_offset = 0
        for line in raw_lines:
            wrapped_lines = self._wrap_line(line) if self.max_width else [line]
            for wrapped_line in wrapped_lines:
                line_pos = self.start_pos.copy()
                line_pos.y += y_offset
                string_handler = String_handler(wrapped_line, line_pos, reveal_speed=self.reveal_speed)
                self.lines.append(string_handler)
                y_offset += FONT.get_height() + self.line_spacing

    def _wrap_line(self, line):
        words = line.split(' ')
        wrapped_lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            width = FONT.size(test_line)[0]
            if width > self.max_width and current_line != "":
                wrapped_lines.append(current_line.strip())
                current_line = word + " "
            else:
                current_line = test_line
        if current_line:
            wrapped_lines.append(current_line.strip())
        return wrapped_lines

    def update(self):
        if self.current_line_index < len(self.lines):
            for line in self.lines[:self.current_line_index + 1]:
                line.update()

    def draw(self, screen):
        for i in range(self.current_line_index + 1):
            if i < len(self.lines):
                self.lines[i].draw(screen)

    def advance_line(self):
        if self.current_line_index < len(self.lines) - 1:
            self.current_line_index += 1


class run(APP):
    def init(self):
        self.WIDTH = 1920
        self.HEIGHT = 1080
        self.FULLSCREEN = True

    def setup(self):
        paragraph = (
            "The air grew colder as you stepped inside.\n"
            "A faint whisper echoed through the empty halls.\n"
            "Something... was watching.\n"
        )
        self.paragraph_handler = ParagraphHandler(paragraph, V2(50, APP.HH), reveal_speed=50, max_width=APP.W - 100)

    def draw(self):
        self.paragraph_handler.draw(self.screen)

    def update(self):
        self.paragraph_handler.update()

    def event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN:
                self.paragraph_handler.advance_line()



run()