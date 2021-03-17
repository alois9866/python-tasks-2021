import tkinter
import tkinter.font

DEFAULT_WIDTH = 7  # For default sized TkFixedFont on my machine.


def _if(cond, body):
    if cond: body()


class InputLabel(tkinter.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, takefocus=True, highlightthickness=1, padx=0, pady=0, **kwargs)
        self.tv = kwargs['textvariable']

        self.cur = InputLabel.Cursor(self, takefocus=True, highlightthickness=0, bg="black", font=kwargs['font'])
        self.cur.place(y=0, x=0, relheight=1, width=1)

        self.prepare()

    def prepare(self):
        self.cur.prepare()
        self.bind("<Left>", self.forward_key("<Left>"))
        self.bind("<Right>", self.forward_key("<Right>"))
        self.bind("<Home>", self.forward_key("<Home>"))
        self.bind("<End>", self.forward_key("<End>"))
        self.bind("<BackSpace>", self.delete, add=False)
        self.bind("<Any-KeyPress>", self.input, add=True)
        self.bind("<Button-1>", self.click, add=False)

    def forward_key(self, key_press):
        def f(_):
            self.cur.focus_set()
            self.event_generate(key_press)
            self.focus_set()

        return f

    def delete(self, _):
        position = self.cur.x() // DEFAULT_WIDTH
        if position > 0:
            self.tv.set(self.tv.get()[:position - 1] + self.tv.get()[position:])
            self.cur.event_generate("<Left>")

    def input(self, arg):
        if arg.char != "":
            position = self.cur.x() // DEFAULT_WIDTH
            self.tv.set(self.tv.get()[:position] + arg.char + self.tv.get()[position:])
            self.update()
            self.cur.event_generate("<Right>")

    def click(self, arg):
        self.cur.place_configure(x=min(arg.x - arg.x % DEFAULT_WIDTH, len(self.tv.get()) * DEFAULT_WIDTH))
        self.focus_set()

    class Cursor(tkinter.Label):
        def __init__(self, master, *args, **kwargs):
            super().__init__(master, *args, **kwargs)

        def x(self):
            return int(self.place_info()['x'])

        def prepare(self):
            self.bind("<Left>", lambda _: _if(self.x() - DEFAULT_WIDTH >= 0,
                                              lambda: self.place_configure(x=self.x() - DEFAULT_WIDTH)))
            self.bind("<Right>", lambda _: _if(self.x() < len(self.master.tv.get()) * DEFAULT_WIDTH,
                                               lambda: _if(self.master.winfo_width() > self.x() + DEFAULT_WIDTH,
                                                           lambda: self.place_configure(x=self.x() + DEFAULT_WIDTH))))
            self.bind("<Home>", lambda _: self.place_configure(x=0))
            self.bind("<End>", lambda _: self.place_configure(x=len(self.master.tv.get()) * DEFAULT_WIDTH))


class App(tkinter.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(None, *args, **kwargs)
        self.master.title("LabelEdit.py")

        for obj in [self.master, self]:
            obj.columnconfigure(0, weight=1)
            obj.rowconfigure(0, weight=1)
            obj.rowconfigure(1, weight=1)
        self.grid(sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)

        label = InputLabel(self, textvariable=tkinter.StringVar(), anchor=tkinter.W, justify='left', font=tkinter.font.Font(font='TkFixedFont'))
        label.grid(column=0, row=0, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)
        label.focus_set()

        tkinter.Button(self, text="Quit", command=self.master.quit) \
            .grid(column=0, row=1, sticky=tkinter.N + tkinter.E + tkinter.W + tkinter.S)


if __name__ == '__main__':
    App().mainloop()
