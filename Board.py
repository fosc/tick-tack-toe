from enum import Enum

Square = Enum("Square", "Empty X O")


class GameBoard:

    def __init__(self, size):
        self._board = [[Square.Empty]*size for i in range(size)]
        self.size = size
        self.rows = [[(j, i) for j in range(size)] for i in range(size)]
        self.columns = [[(i, j) for j in range(size)] for i in range(size)]
        self.diagonal = [(i, i) for i in range(size)]
        self.off_diagonal = [(i, size - 1 - i) for i in range(size)]

    def __str__(self):
        board = ''
        square_to_string = {
            Square.Empty: " ",
            Square.O: "O",
            Square.X: "X",
                            }
        for row in self.rows:
            for square in row:
                board += '|' + square_to_string[square]
            board += '|\n'
        return board

    def check_for_win(self, player):
        def check_list_of_squares(list_of_squares):
            squares = self.get_squares(list_of_squares)
            if len(squares[Square.Empty]) == 1 and len(squares[player]) == self.size - 1:
                return squares[Square.Empty][0]
            return None
        potential_wins = [check_list_of_squares(self.diagonal)]
        potential_wins += [check_list_of_squares(self.off_diagonal)]
        potential_wins += list(map(check_list_of_squares, self.rows))
        potential_wins += list(map(check_list_of_squares, self.columns))
        return [x for x in potential_wins if x is not None]

    def get_squares(self, list_of_coords):
        d = {x: self.get_square(*x) for x in list_of_coords}
        d2 = {Square.X: [], Square.O: [], Square.Empty: []}
        for key, value in d.items():
            d2[value].append(key)
        return d2

    def get_square(self, x, y):
        return self._board[y][x]

    def set_square(self, x, y, mark):
        self._board[y][x] = mark


class TickTackToeGame:

    def __init__(self, size):
        self.size = size
        self.gameBoard = GameBoard(size)
        self.history = {
            Square.X: [],
            Square.O: []
        }

    def set(self, x, y, mark):
        if self.gameBoard.get_square(x, y) is not Square.Empty:
            raise ValueError(f'square {x} {y} is not empty. Cannot set to {mark}')
        self.gameBoard.set_square(x, y, mark)
        self.history[mark].append((x, y))

    def number_of_moves(self, player):
        return len(self.history[player])

    def next_player(self):
        """X goes first"""
        x_count = self.number_of_moves(Square.X)
        o_count = self.number_of_moves(Square.O)
        return Square.X if x_count <= o_count else Square.O

    def __str__(self):
        return str(self.gameBoard)