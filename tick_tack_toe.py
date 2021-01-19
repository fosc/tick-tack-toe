"""This module contains class Game which can orchestrate tick tack toe and print to stdout"""
from enum import Enum
from copy import deepcopy
SQUARE = Enum("SQUARE", "Empty X O")


class Board:
    """Two dimensional board implemented on top of List of Lists. Gets and sets squares."""
    def __init__(self, size, def_val):
        self._board = [[def_val]*size for i in range(size)]
        self.size = size

    def get_square(self, coord):
        return self._board[coord[1]][coord[0]]

    def set_square(self, coord, mark):
        self._board[coord[1]][coord[0]] = mark


class GameBoard(Board):
    """A Board that can also check for wins and return possible moves for the next player"""
    def __init__(self, size):
        super().__init__(size, SQUARE.Empty)
        self._rows = [[(j, i) for j in range(size)] for i in range(size)]
        self._columns = [[(i, j) for j in range(size)] for i in range(size)]
        self._diagonal = [(i, i) for i in range(size)]
        self._off_diagonal = [(i, size - 1 - i) for i in range(size)]

    def __str__(self):
        def row_to_string(this_row):
            return ''.join([f"|{square_to_string[x]}" for x in this_row]) + '|\n'

        def get_squares(row):
            return list(map(self.get_square, row))

        square_to_string = {SQUARE.Empty: " ", SQUARE.O: "O", SQUARE.X: "X"}
        rows = list(map(get_squares, self._rows))
        return ''.join(list(map(row_to_string, reversed(rows))))

    def get_empty_squares(self):
        """Return a single list of the coordinates of all squares containing SQUARE.Empty"""
        def get_empty_squares(list_of_coords):
            return self._get_squares(list_of_coords)[SQUARE.Empty]
        coords_of_empty = list(map(get_empty_squares, self._rows))
        return [item for sublist in coords_of_empty for item in sublist]

    def are_there_n_in_a_row(self, player):
        """Return True if a row/column/diagonal spans the board. Otherwise False."""
        for row in [self._diagonal, self._off_diagonal] + self._rows + self._columns:
            if len(self._get_squares(row)[player]) == self.size:
                return True
        return False

    def find_winning_move(self, player):
        """Return a list containing the coordinates of winning moves, if any exist."""
        def check_list_of_squares(list_of_squares):
            squares = self._get_squares(list_of_squares)
            if len(squares[SQUARE.Empty]) == 1 and len(squares[player]) == self.size - 1:
                return squares[SQUARE.Empty][0]
            return None
        potential_wins = [check_list_of_squares(self._diagonal)]
        potential_wins += [check_list_of_squares(self._off_diagonal)]
        potential_wins += list(map(check_list_of_squares, self._rows))
        potential_wins += list(map(check_list_of_squares, self._columns))
        return [x for x in potential_wins if x is not None]

    def _get_squares(self, list_of_coords):
        """Return a dictionary mapping each SQUARE type to a list of corresponding coordinates."""
        square_values = {x: self.get_square(x) for x in list_of_coords}
        square_map = {SQUARE.X: [], SQUARE.O: [], SQUARE.Empty: []}
        for key, value in square_values.items():
            square_map[value].append(key)
        return square_map


class RuleManager:
    """
    RuleManager has a GameBoard. It handles interactions with that GameBoard.

    Rule Manager implements the Game State interface by providing the following methods:
    1. is_game_over() --> Boolean
    2. get_moves() --> list of tuples
    3. is_winnable() --> Boolean
    4. + tuple --> new Game State
    """
    def __init__(self, size):
        self._game_board = GameBoard(size)
        self.history = {SQUARE.X: [], SQUARE.O: []}

    def __add__(self, other):
        if isinstance(other, tuple):
            game_copy = deepcopy(self)
            game_copy.set(*other, self.next_player())
            return game_copy
        raise ValueError('Only Tuples can be added to this class with the + operator.')

    def get_moves(self):
        """Return all playable moves remaining in the game"""
        return self._game_board.get_empty_squares()

    def set(self, x, y, mark):
        """Write and X or and O on gameBord. Check to make sure its and empty square."""
        if self._game_board.get_square((x, y)) is not SQUARE.Empty:
            raise ValueError(f'square {x} {y} is not empty. Cannot set to {mark}')
        self._game_board.set_square((x, y), mark)
        self.history[mark].append((x, y))

    def number_of_moves(self, player):
        """Return how many moves player has made"""
        return len(self.history[player])

    def next_player(self):
        """Return who goes next. Remember, X goes first"""
        x_count = self.number_of_moves(SQUARE.X)
        o_count = self.number_of_moves(SQUARE.O)
        return SQUARE.X if x_count <= o_count else SQUARE.O

    def is_winnable(self):
        """Return true if the active player can win."""
        return len(self._game_board.find_winning_move(self.next_player())) > 0

    def is_game_over(self):
        """Return True if someone has won or a draw has been reached"""
        if self._game_board.are_there_n_in_a_row(SQUARE.X):
            return True
        if self._game_board.are_there_n_in_a_row(SQUARE.O):
            return True
        if not self._game_board.get_empty_squares():
            return True
        return False

    def get_winner(self):
        """Return the winner if there is one, else return None"""
        if self._game_board.are_there_n_in_a_row(SQUARE.X):
            return SQUARE.X
        if self._game_board.are_there_n_in_a_row(SQUARE.O):
            return SQUARE.O
        return None

    def __str__(self):
        return str(self._game_board)


class Game:
    """
    Orchestrate a game between team_x and team_o on board of size 'size'

    Initializes as Game(Player, Player, int)
    The Player interface provides the following method:
    1. play(Game State) --> tuple
    """
    def __init__(self, team_x, team_o, size):
        self._game_manager = RuleManager(size)
        self._this_turn = SQUARE.X
        self._team = {SQUARE.X: team_x, SQUARE.O: team_o}

    def _do_turn(self):
        """Get next move, apply it to the board, switch self._this_turn"""
        x, y = self._team[self._this_turn].play(self._game_manager)
        self._game_manager.set(x, y, self._this_turn)
        self._this_turn = SQUARE.X if self._this_turn is SQUARE.O else SQUARE.O

    def _is_win_or_tie(self):
        """Return True if the game is over, otherwise False."""
        is_over = self._game_manager.is_game_over()
        winner = self._game_manager.get_winner()
        if is_over and winner is not None:
            print(self._game_manager)
            print(f"{winner} the winner")
            return True
        elif is_over:
            print(self._game_manager)
            print(f"Tie Game")
            return True
        return False

    def start_game(self):
        """Start the game and don't stop until its over"""
        while not self._is_win_or_tie():
            self._do_turn()
