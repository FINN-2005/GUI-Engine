from pygame_template import *
from GUI import *


class run(APP):
    def setup(self):
        self.manager = Widget_Manager()     # must initialise this

        Button()        # automatically added to the widget manager

    def draw(self):
        self.manager.draw(self.screen)

    def update(self):
        self.manager.update(self.dt)



run()