import tkinter
import tkinter.messagebox

from fifteen import Fifteen


def number_to_piece(number: int) -> str:
    if number == 0:
        return ""
    return str(number)


class Application(tkinter.Frame):
    game: Fifteen

    def __init__(self, game: Fifteen):
        self.game = game
        tkinter.Frame.__init__(self, None)
        self.grid(column=4, row=5)
        self.create_widgets()

    def with_update(self, f, *args):
        f(*args)
        self.create_widgets()

    def hit(self, x: int, y: int):
        self.game.hit(x, y)
        if self.game.won():
            tkinter.messagebox.showinfo("Congratulations", "You won!")
            self.quit()

    def create_widgets(self):
        tkinter.Button(self, text='New',
                       command=lambda: self.with_update(self.game.reset),
                       width=2, height=2).grid(row=0, column=0)
        tkinter.Button(self, text='Quit',
                       command=self.quit,
                       width=2, height=2).grid(row=0, column=3)
        for x in range(4):
            for y in range(4):
                def hit(x=x, y=y):
                    self.with_update(self.hit, x, y)

                tkinter.Button(self, text=number_to_piece(self.game.state[x][y]),
                               command=hit,
                               width=2, height=2).grid(row=y + 1, column=x)


def main():
    app = Application(Fifteen())
    app.master.title('Game of Fifteen')
    app.mainloop()


if __name__ == '__main__':
    main()
