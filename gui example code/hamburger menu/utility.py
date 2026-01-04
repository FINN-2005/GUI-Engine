from pygame_template import *




class Timer:
    def __init__(self, duration, callback):
        self.duration = duration * 1000  # Duration in seconds
        self.callback = callback         # Function to call after duration
        self.start_time = None           # Start time in milliseconds
        self.active = False              # Timer status

    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.active = True

    def update(self):
        if self.active:
            elapsed_time = pygame.time.get_ticks() - self.start_time
            if elapsed_time >= self.duration:
                if self.callback is not None:
                    self.callback()  
                self.active = False  # Stop the timer

    def reset(self):
        self.start_time = None
        self.active = False
