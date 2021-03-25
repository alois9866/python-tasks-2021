import re
import tkinter
from typing import List

color_re = re.compile(r'^#[0-9a-f]{3}$')


class Ellipse:
    x0: int
    y0: int
    width: int
    height: int
    color: str
    border_width: int
    border_color: str

    def __init__(self, x0: int, y0: int, width: int = 0, height: int = 0, color: str = '#000', border_width: int = 0, border_color: str = '#000'):
        self.x0 = x0
        self.y0 = y0
        self.width = width
        self.height = height
        self.color = color
        self.border_width = border_width
        self.border_color = border_color

    def resize(self, x: int, y: int):
        self.width = abs(x - self.x0)
        self.height = abs(y - self.y0)

    def move(self, x: int, y: int):
        self.x0 = x
        self.y0 = y

    def contains(self, x: int, y: int):
        return ((x - self.x0) ** 2 / self.width ** 2 + (y - self.y0) ** 2 / self.height ** 2) <= 1

    def __str__(self) -> str:
        return f'{self.x0} {self.y0} {self.width} {self.height} {self.color} {self.border_width} {self.border_color}'

    def __repr__(self):
        return self.__str__()


class Editor(tkinter.Canvas):
    ellipses: List[Ellipse] = []
    button_down: bool = False
    move_target: Ellipse = None

    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)
        self.prepare()
        self.draw()

    def send_to(self, text: 'Text'):
        def f():
            text.ellipses = self.ellipses.copy()
            print('text', text.ellipses)
            text.draw()

        return f

    def prepare(self):
        def press(arg):
            self.button_down = True
            for e in self.ellipses[::-1]:
                if e.contains(arg.x, arg.y):
                    self.move_target = e
                    break
            if self.move_target is None:
                self.ellipses.append(Ellipse(arg.x, arg.y))
            self.draw()

        def motion(arg):
            if self.button_down:
                if self.move_target is None:
                    self.ellipses[-1].resize(arg.x, arg.y)
                else:
                    self.move_target.move(arg.x, arg.y)
                self.draw()

        def release(arg):
            self.button_down = False
            if self.move_target is None:
                self.ellipses[-1].resize(arg.x, arg.y)
            else:
                self.move_target = None
            self.draw()

        self.bind("<ButtonPress>", press, add=False)
        self.bind("<Motion>", motion, add=False)
        self.bind("<ButtonRelease>", release, add=False)

    def draw(self):
        self.delete(tkinter.ALL)
        width, height = self.winfo_width(), self.winfo_height()
        self.create_polygon(0, 0, width, 0, width, height, 0, height, fill='#fff')
        for e in self.ellipses:
            self.create_oval(e.x0 - e.width, e.y0 - e.height, e.x0 + e.width, e.y0 + e.height, fill=e.color, outline=e.border_color, width=e.border_width)

    def __repr__(self):
        return self.__str__()


class Text(tkinter.Text):
    ellipses: List[Ellipse] = []

    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)
        self.tag_config('error', background="#faa")
        self.draw()

    def correct_text(self):
        correct = True
        txt: str = self.get(1.0, tkinter.END)
        self.delete(1.0, tkinter.END)
        for line in txt.split('\n'):
            line = line.strip()
            if line == '':
                continue
            params = line.split(' ')
            if len(params) != 7:
                correct = False
                self.insert(tkinter.END, line + '\n', 'error')
                continue
            try:
                int(params[0])
                int(params[1])
                assert int(params[2]) >= 0
                assert int(params[3]) >= 0
                assert color_re.match(params[4])
                assert int(params[5]) >= 0
                assert color_re.match(params[6])
            except:
                correct = False
                self.insert(tkinter.END, line + '\n', 'error')
                continue
            self.insert(tkinter.END, line + '\n')

        return correct

    def convert_text(self):
        ellipses = []
        txt: str = self.get(1.0, tkinter.END)
        for line in txt.split('\n'):
            line = line.strip()
            if line == '':
                continue
            (x0, y0, width, height, color, border_width, border_color) = line.split(' ')
            ellipses.append(Ellipse(int(x0), int(y0), int(width), int(height), color, int(border_width), border_color))
        return ellipses

    def draw(self):
        self.delete(1.0, tkinter.END)
        self.insert(tkinter.END, '\n'.join(map(str, self.ellipses)))

    def send_to(self, editor: Editor):
        def f():
            if self.correct_text():
                self.ellipses = self.convert_text()
            editor.ellipses = self.ellipses.copy()
            print('editor', editor.ellipses)
            editor.draw()

        return f


class App(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)
        self.master.title("Ellipse Editor")

        for obj in [self.master, self]:
            obj.columnconfigure(0, weight=1)
            obj.rowconfigure(0, weight=1)
            obj.rowconfigure(1, weight=1)
        self.grid(sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)

        text = Text(self, width=40)
        text.grid(column=0, row=0, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)

        editor = Editor(self)
        editor.grid(column=1, row=0, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)

        tkinter.Button(self, text="Send to editor", command=text.send_to(editor)) \
            .grid(column=0, row=1, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)

        tkinter.Button(self, text="Send to text", command=editor.send_to(text)) \
            .grid(column=1, row=1, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)


if __name__ == '__main__':
    App().mainloop()
