from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(
            self,
            pos = (100, 100),
            size = (100, 40),
            
            draw_text = True,
            text = 'test',
            font_size = 30,
            text_col = (255,255,255,255),
            
            timer_duration = 1,     # in seconds
            call_func = None,
            
            top_col = (200, 100, 200, 255),
            top_col_hovered = (200, 200, 200, 255),
            bottom_col = (150, 50, 150, 255),
            bottom_col_hovered = (150, 150, 150, 255),
            top_col_pushed = (250, 150, 250, 255),
            bottom_col_pushed = (200, 100, 200, 255),
            *groups: tuple[pygame.sprite.Group]):
        
        super().__init__(*groups)

        self.top_col = top_col
        self.top_col_hovered = top_col_hovered
        self.bottom_col = bottom_col
        self.bottom_col_hovered = bottom_col_hovered
        self.top_col_pushed = top_col_pushed
        self.bottom_col_pushed = bottom_col_pushed
        
        self.timer = Timer(timer_duration, None)
        self.call_func = call_func
        
        self.draw_text = draw_text
        self.text = text
        self.text_col = text_col
        self.font_size = font_size
        if self.draw_text:
            self.font = pygame.Font(None, self.font_size)

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_frect(topleft=pos)

        self.pos = pos
        self.size = size        

        self.setup()

    def setup(self):
        self.bottom_rect = pygame.FRect(0, 8, self.size[0], self.size[1] - 8)
        self.top_rect = pygame.FRect(0, 0, self.size[0], self.size[1] - 8)

        # self.top_col = (200, 100, 200, 255)
        # self.top_col_hovered = (200, 200, 200, 255)
        # self.bottom_col = (150, 50, 150, 255)
        # self.bottom_col_hovered = (150, 150, 150, 255)
        # self.top_col_pushed = (250, 150, 250, 255)
        # self.bottom_col_pushed = (200, 100, 200, 255)

        self.hovering = False
        self.pushed = False

        self.draw_button()

    def draw_text_on_top(self):
        if self.draw_text:
            text_surf = self.font.render(self.text, True, self.text_col)
            text_rect = text_surf.get_frect(center = self.top_rect.center)
            self.image.blit(text_surf, text_rect)
    
    def draw_button(self):
        self.image.fill((0, 0, 0, 0))

        if self.pushed:
            self.top_rect.topleft = (0, 8)                
            pygame.draw.rect(self.image, self.bottom_col_pushed, self.bottom_rect, 0, 5)
            pygame.draw.rect(self.image, self.top_col_pushed, self.top_rect, 0, 5)
            self.draw_text_on_top()
            if not self.timer.active:
                self.timer.start()
                if self.call_func is not None: self.call_func()
            
        elif self.hovering:
            self.top_rect.topleft = (0, 0)
            pygame.draw.rect(self.image, self.bottom_col_hovered, self.bottom_rect, 0, 5)
            pygame.draw.rect(self.image, self.top_col_hovered, self.top_rect, 0, 5)
            self.draw_text_on_top()
            
        else:
            self.top_rect.topleft = (0, 0)
            pygame.draw.rect(self.image, self.bottom_col, self.bottom_rect, 0, 5)
            pygame.draw.rect(self.image, self.top_col, self.top_rect, 0, 5)
            self.draw_text_on_top()

    def update(self, *args):
        mpos = pygame.mouse.get_pos()
        mdown = pygame.mouse.get_pressed()[0]

        if self.rect.collidepoint(mpos):
            if mdown:
                self.pushed = True
                self.hovering = False
            else: 
                self.pushed = False
                self.hovering = True
        else:
            self.pushed = False
            self.hovering = False

        self.draw_button()
        self.timer.update()
                      
class TextElement(pygame.sprite.Sprite):
    def __init__(
            self,
            text="Hello World",
            pos=(300,100),
            font_size=30,
            color=(255,255,255,255),
            background_col=(200,100,200,255),
            background_bold_col=(150, 50, 150, 255),
            *groups: tuple[pygame.sprite.Group]):
        
        super().__init__(*groups)
        
        self.text = text
        self.color = color
        self.font_size = font_size
        self.pos = pos
        self.background_col = background_col
        self.background_bold_col = background_bold_col
        self.font = pygame.font.Font(None, self.font_size)
        
        self.update_image()

    def update_image(self):
        self.font_surf = self.font.render(self.text, True, self.color)
        self.image = pygame.Surface(V2(self.font_surf.get_size()) + V2(15, 15), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0)) 
        self.rect = self.image.get_frect(center=self.pos)
        self.background = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(self.background, self.background_col, pygame.Rect((0, 0), self.rect.size), 0, 8)
        pygame.draw.rect(self.background, self.background_bold_col, pygame.Rect((0, 0), self.rect.size), 2, 8)
        self.image.blit(self.background, (0, 0))
        self.image.blit(self.font_surf, (7.5, 7.5))

    def update_text(self, new_text):
        self.text = new_text
        self.update_image()

    def update_color(self, new_color):
        self.color = new_color
        self.update_image()

    def update_position(self, new_pos):
        self.pos = new_pos
        self.rect.topleft = self.pos

    def update(self, *args):
        pass

