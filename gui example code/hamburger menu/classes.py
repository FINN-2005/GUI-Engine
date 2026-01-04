from utility import *



class Button(pygame.sprite.Sprite):
    def __init__(
        self,
        pos=(100, 100),
        size=(160, 50),
        text="Click me",
        font_size=28,
        font_color=(255, 255, 255),
        
        bg_color=(50, 50, 200, 180),
        hover_color=(80, 80, 240, 220),
        pressed_color=(30, 30, 150, 255),
        
        corner_radius=12,
        call_func=None,
        *groups
    ):
        super().__init__(*groups)

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_frect(topleft=pos)

        self.text = text
        self.font = get_Font(font_size)
        self.font_color = font_color

        self.bg_color = bg_color
        self.hover_color = hover_color
        self.pressed_color = pressed_color

        self.corner_radius = corner_radius
        self.call_func = call_func

        self.hovering = False
        self.pushed = False

        self.draw_button()

    def draw_button(self):
        self.image.fill((0, 0, 0, 0))  # Clear with full transparency

        color = self.bg_color
        if self.pushed:
            color = self.pressed_color
        elif self.hovering:
            color = self.hover_color

        pygame.draw.rect(
            self.image,
            color,
            pygame.FRect(0, 0, *self.rect.size),
            border_radius=self.corner_radius
        )

        # Render and center text
        text_surf = self.font.render(self.text, True, self.font_color)
        text_rect = text_surf.get_frect(center=(self.rect.width // 2, self.rect.height // 2))
        self.image.blit(text_surf, text_rect)

    def update(self, *args):
        mpos = pygame.mouse.get_pos()
        mdown = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mpos):
            if mdown:
                if not self.pushed and self.call_func:
                    self.call_func()
                self.pushed = True
                self.hovering = False
            else:
                self.hovering = True
                self.pushed = False
        else:
            self.hovering = False
            self.pushed = False

        self.draw_button()
