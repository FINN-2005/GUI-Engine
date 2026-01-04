

class Text:
    def __init__(self, default = 'Default Text'):
        self.data = default
        self.cursor = len(default)

    def move_cursor(self, dir: int):
        '''Move Cursor by Given Amount'''
        self.cursor = max(0, min(len(self.data), self.cursor + dir))

    def set_cursor(self, index: int):
        if not 0 <= index <= len(self.data): raise IndexError('Index out of bounds')
        self.cursor = index

    def __repr__(self):
        return f'{self.data[:self.cursor]}_{self.data[self.cursor:]}'

    def put_text(self, t: str):
        self.data = self.data[:self.cursor] + t + self.data[self.cursor:]
        self.cursor += len(t)

    def set_text(self, t: str):
        self.data = t
        self.cursor = len(t)

    def del_text(self, how_many_chars: int):
        dcrsr = min(how_many_chars, len(self.data[:self.cursor]))
        self.data = self.data[:self.cursor - dcrsr] + self.data[self.cursor:]
        self.cursor -= dcrsr 
        return dcrsr


a = Text()
print(a)

a.set_cursor(5)
a.put_text('this is text')
print(a)

a.set_text('Hello, World!')
print(a)

a.move_cursor(-6)
print(a)

a.del_text(3)
print(a)
