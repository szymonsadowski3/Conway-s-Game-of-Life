class Cell:
    def __init__(self, i, j):
        """ Create a new point at the origin """
        self.i = i
        self.j = j


class GameOfLifeSimulator(object):
    directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]

    def noOfNeighbors(self, board, i, j):
        no = 0
        for direction in self.directions:
            dx, dy = direction
            if i + dx < 0 or j + dy < 0:
                continue
            try:
                no = no + board[i + dx][j + dy]
            except IndexError:
                continue
        return no

    def toggle(self, board, cells_to_toggle):
        for cell in cells_to_toggle:
            board[cell.i][cell.j] = 1 - board[cell.i][cell.j]

    def simulate(self, board):
        to_toggle = []
        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                alive = True if board[i][j] else False
                no = self.noOfNeighbors(board, i, j)
                if ((no < 2 or no > 3) and alive) or (no == 3 and not alive):
                    to_toggle.append(Cell(i, j))
        self.toggle(board, to_toggle)
