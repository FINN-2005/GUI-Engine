from pygame_template import *

class rect(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface(size=(random.randint(50,300),random.randint(50,300)))
        self.rect = self.image.get_frect()
        self.size = V2(self.image.size)
        pygame.draw.rect(self.image, Color.random(), self.rect)
        pygame.draw.rect(self.image, 'black', self.rect, 5)
        pygame.draw.rect(self.image, (200,200,200,100), self.rect, 3)
        pygame.draw.rect(self.image, 'black', self.rect, 2)


class COL:
    def __init__(self):
        self.children = []
        self.pos = V2(APP.HW, APP.HH)
        self.size = V2()

        self.padding = V2(20, 20)
        self.spacing = 15

    def __add__(self, r: rect):
        self.children.append(r)
        self.relayout()

    def relayout(self):
        size = V2()
        size.y += self.padding.y
        width = 0

        for i, child in enumerate(self.children): 
            if i != 0:
                size.y += self.spacing
            size.y += child.size.y
            width = max(width, child.size.x)
        size.x = width + self.padding.x * 2
        size.y += self.padding.y
        self.size = size

        # Align all children
        start_y = self.pos.y - self.size.y // 2 + self.padding.y
        for child in self.children:
            x = self.pos.x - child.size.x // 2  # center horizontally
            child.rect.topleft = (x, start_y)
            start_y += child.size.y + self.spacing



class ROW:
    def __init__(self):
        self.children = []
        self.pos = V2(APP.HW, APP.HH)
        self.size = V2()

        self.padding = V2(20, 20)
        self.spacing = 15

    def __add__(self, r: rect):
        self.children.append(r)
        self.relayout()

    def relayout(self):
        size = V2()
        size.x += self.padding.x
        height = 0

        for i, child in enumerate(self.children): 
            if i != 0:
                size.x += self.spacing
            size.x += child.size.x
            height = max(height, child.size.y)
        size.y = height + self.padding.y * 2
        size.x += self.padding.x
        self.size = size

        # Align all children
        start_x = self.pos.x - self.size.x // 2 + self.padding.x
        for child in self.children:
            y = self.pos.y - child.size.y // 2  # center vertically
            child.rect.topleft = (start_x, y)
            start_x += child.size.x + self.spacing



class run(APP):
    def setup(self):
        self.drawables = Group()
        self.col = COL()

        self.col + rect(self.drawables)
        self.col + rect(self.drawables)

    def draw(self):
        self.drawables.draw()

    def update(self):
        self.drawables.update()

run()