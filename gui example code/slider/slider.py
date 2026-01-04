from pygame_template import *

class slider(Sprite):
    def __init__(self, y=APP.H, *groups):
        super().__init__(*groups)

        self.size_A = V2(50, 30)
        self.size_B = V2(200, 3)

        self.no_of_steps = 10

        self.A = pygame.Rect(APP.HW - self.size_A.x/2, y - self.size_A.y * 3, self.size_A.x, self.size_A.y)
        self.B = pygame.Rect(APP.HW - self.size_B.x/2, y - self.size_A.y * 2.5 - self.size_B.y/2, self.size_B.x, self.size_B.y)

        self.dragging = False
        self.value = 0

    def draw(self, screen):
        pygame.draw.rect(screen, 'gray40', self.B, 0, 5)
        pygame.draw.rect(screen, 'gray', self.A, 0, 5)

    
    def get_snapped_value(self, x, n):
        t = (x - self.B.x) / (self.B.w)
        t = max(0, min(1, t))
        step_index = round(t * (n - 1))
        return step_index / (n - 1)
    
    def update(self, dt):
        mouse = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()[0]
        if pressed and self.A.collidepoint(mouse): self.dragging = True
        elif not pressed: self.dragging = False
        if self.dragging:
            mouse_x = mouse[0]
            self.value = self.get_snapped_value(mouse_x, self.no_of_steps)
        snapped_x = self.B.x + self.value * self.B.w
        self.A.centerx = snapped_x

    def set_value(self, value):
        self.value = max(0, min(1, value))
        self.A.centerx = self.B.x + self.value * self.B.w


class run(APP):
    def setup(self):
        self.grp = Group(slider(), slider(APP.HW))
        self.font = get_Font()

    def update(self):
        self.grp.update(self.dt)

        s1, s2 = self.grp.sprites()
        s1.no_of_steps = 1000

        if s1.dragging:
            s2.set_value(s1.value)
        elif s2.dragging:
            s1.set_value(s2.value)

        self.step_count_1 = self.font.render(f'Slider 1: {s1.value}', True, 'white')
        self.step_count_2 = self.font.render(f'Slider 2: {s2.value}', True, 'white')

    def draw(self):
        self.screen.blit(self.step_count_1, (100,100,100,100))
        self.screen.blit(self.step_count_2, (100,200,100,100))
        self.grp.draw()


if __name__ == '__main__':
    run()