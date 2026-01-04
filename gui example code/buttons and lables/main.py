from classes import *

class GUI:
    def __init__(self):
        self.screen = pygame.display.set_mode(RES, pygame.SRCALPHA)
        self.clock = pygame.Clock()
        
        self.group = pygame.sprite.Group((
            TextElement(text='close',pos=(HW,HH)),                                                           # background_col=(0,0,0,0), background_bold_col=(0,0,0,0) for no background
            Button(call_func=self.exit, timer_duration= 0.5, text='X', pos=(W-5-30,5), size=(30,34)),        # close button top-right
        ))
        self.run()

    def exit(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick()/1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.exit()
                                        
            self.screen.fill('gray16')
            self.group.update()
            self.group.draw(self.screen)
            pygame.display.flip()
            pygame.display.set_caption(str(self.clock.get_fps()))

if __name__ == '__main__':
    GUI()
    pygame.quit()
    sys.exit()
