import tkinter
from typing import List


class Ellipse:
    x0: int
    y0: int
    width: int = 0
    height: int = 0
    color: str = '#000'
    border_width: int = '0'
    border_color: str = '#000'

    def __init__(self, x0: int, y0: int):
        self.x0 = x0
        self.y0 = y0

    def resize(self, x: int, y: int):
        self.width = x - self.x0
        self.height = y - self.y0

    def contains(self, x: int, y: int):
        return (x - self.x0) ** 2 / self.width ** 2 + (y - self.y0) ** 2 / self.height ** 2

    def __str__(self) -> str:
        return f'{self.x0} {self.y0} {self.width} {self.height} {self.color} {self.border_width} {self.border_color}'

    def __repr__(self):
        return self.__str__()


class Editor(tkinter.Canvas):
    ellipses: List[Ellipse] = []
    button_down: bool = False

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
            print(arg)
            self.button_down = True
            self.ellipses.append(Ellipse(arg.x, arg.y))

        def motion(arg):
            if self.button_down:
                self.ellipses[-1].resize(arg.x, arg.y)
                self.draw()

        def release(arg):
            print(arg)
            self.button_down = False
            self.ellipses[-1].resize(arg.x, arg.y)
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
        self.draw()

    def draw(self):
        self.delete(1.0, tkinter.END)
        self.insert(tkinter.END, '\n'.join(map(str, self.ellipses)))

    def send_to(self, editor: Editor):
        def f():
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

        text = Text(self)
        text.grid(column=0, row=0, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)

        editor = Editor(self)
        editor.grid(column=1, row=0, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)

        tkinter.Button(self, text="Send to editor", command=text.send_to(editor)) \
            .grid(column=0, row=1, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)

        tkinter.Button(self, text="Send to text", command=editor.send_to(text)) \
            .grid(column=1, row=1, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)


if __name__ == '__main__':
    App().mainloop()
