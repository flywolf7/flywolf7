import copy
import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
            self,
            size: tp.Tuple[int, int],
            randomize: bool = True,
            max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0] * self.rows] * self.cols
        if randomize == 1:
            for i in grid:
                for j in range(len(i)):
                    i[j] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        x, y = cell
        x -= 1
        y -= 1

        cells: tp.List[int] = []
        for i in range(x, x + 3):
            for j in range(y, y + 3):
                if cell[0] == i and cell[1] == j:
                    continue
                if 0 <= i < self.rows and 0 <= j < self.cols:
                    value = self.curr_generation[i][j]
                    cells.append(value)

        return cells

    def get_next_generation(self) -> Grid:
        changed_grid = copy.deepcopy(self.curr_generation)

        for i in range(self.rows):
            for j in range(self.cols):
                val = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j] == 1:
                    if val > 3 or val < 2:
                        changed_grid[i][j] = 0
                    else:
                        changed_grid[i][j] = 1
                elif self.curr_generation[i][j] == 0:
                    if val == 3:
                        changed_grid[i][j] = 1
                    else:
                        changed_grid[i][j] = 0
        return changed_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """

        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations > self.max_generations:
            return False
        else:
            return True

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation == self.curr_generation:
            return False
        else:
            return True

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        file = open(str(filename), "r")
        array = file.readlines()
        array = [x[:len(x) - 1] for x in array]  # убрать \n в конце

        grid = []
        for i in array:
            curr = []
            for j in range(len(i)):
                curr.append(int(i[j]))
            grid.append(curr)
        game = GameOfLife((len(grid), len(grid[0])), False, float("inf"))
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file = open(str(filename), "w")

        for i in range(self.rows):
            ans = ""
            for j in range(self.cols):
                ans += self.curr_generation[i][j]
            file.write(ans)
            file.write("\n")
