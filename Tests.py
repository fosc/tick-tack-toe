import unittest
from Board import GameBoard, Square


class TestBoard(unittest.TestCase):

    def setUp(self) -> None:
        self.board1 = GameBoard(3)
        self.board1.set_square(1, 1, Square.X)
        self.board1.set_square(2, 2, Square.X)
        self.board1.set_square(0, 2, Square.O)
        self.board1.set_square(0, 1, Square.O)

    def test_check_for_win_board1(self):
        X_win = self.board1.check_for_win(Square.X)
        O_win = self.board1.check_for_win(Square.O)
        self.assertEqual((0, 0), X_win)
        self.assertEqual((0, 0), O_win)



if __name__ == '__main__':
    unittest.main()
