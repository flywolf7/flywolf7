import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        for i in range(0, len(self.life.curr_generation)):
            screen.addstr(
                i + 1,
                1,
                "".join(map(str, self.life.curr_generation[i])).replace("0", " ").replace("1", "*"),
            )
        screen.refresh()
        screen.getch()
        self.life.step()

    def run(self) -> None:
        screen = curses.initscr()
        self.draw_borders(screen)
        self.life.create_grid(randomize=True)
        if type(self.life.max_generations) == "<class 'float'>":
            while True:
                self.draw_grid(screen)
        else:
            for i in range(int(self.life.max_generations)):
                self.draw_grid(screen)
        curses.endwin()
