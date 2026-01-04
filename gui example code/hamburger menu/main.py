from hamburger import *

# press spacebar

class run(APP):
    def setup(self):
        self.d = Drawer()

    def update(self):
        self.d.update(self.dt)

    def draw(self):
        self.d.draw(self.screen)

run()