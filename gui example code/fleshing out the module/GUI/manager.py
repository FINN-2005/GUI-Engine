class Widget_Manager:
    layers = []
    def __init__(self, gui='gui.json'):
        import json
        with open(gui, 'r') as F:
            json_data = json.load(F)
        

    def draw(self, screen):
        for layer in self.layers:
            for wdgt in layer:
                wdgt.draw(screen)

    def update(self, dt):
        for layer in self.layers:
            for wdgt in layer:
                wdgt.update(dt)

    