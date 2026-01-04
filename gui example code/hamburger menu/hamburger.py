from classes import *

class Drawer:
    def __init__(
                self,
                size = V2(300, APP.H),
                pos = V2(-300, 0),
                moving_speed = 10,
                items = [
                    Button(size=(300,50), pos=(0,0), bg_color=(30,30,30,255), hover_color=(130,130,130,255), pressed_color=(60,60,100,255), text='b1', call_func=lambda: print("Button 1")), 
                    Button(size=(300,50), pos=(0,0), bg_color=(30,30,30,255), hover_color=(130,130,130,255), pressed_color=(60,60,100,255), text='b2', call_func=lambda: print("Button 2")),
                    ],
                item_spacing = 10,
                ):
        
        # surfaces
        self.drawer_surf = pygame.Surface(size, pygame.SRCALPHA)
        self.drawer_rect = self.drawer_surf.get_frect(topleft=pos)

        # init
        self.drawer_surf.fill((255,255,255,10))
        self.group = Group(screen=self.drawer_surf)

        self.pos = pos
        self.size = size
        self.items = items
        self.moving_speed = moving_speed


        # contents
        gap = 100
        for y, item in enumerate(items):
            gap = y * (item.rect.h + item_spacing) + gap
            item.rect.y = gap
            self.group.add(item)

        # flags
        self.opening = True
        self.changing_state = False


    def draw(self, screen):
        # self.drawer_surf.fill((0, 0, 0, 0))
        screen.blit(self.drawer_surf, self.drawer_rect)
        self.group.draw()

    def update(self, dt):
        key = pygame.key.get_just_pressed()[pygame.K_SPACE]

        if key:
            self.changing_state = True
        self.change_state(dt)
        
        self.group.update()

    def close(self, dt):
        if self.drawer_rect.left > self.pos.x:
            self.drawer_rect.x -= dt * self.moving_speed
        else: 
            self.drawer_rect.x = self.pos.x
            self.opening = True
            self.changing_state = False

    def open(self, dt):
        if self.drawer_rect.left < self.pos.x + self.size.x:
            self.drawer_rect.x += dt * self.moving_speed
        else: 
            self.drawer_rect.x = self.pos.x + self.size.x
            self.opening = False
            self.changing_state = False

    def change_state(self, dt):
        if self.changing_state:
            if self.opening:
                self.open(dt)
            else: 
                self.close(dt)
