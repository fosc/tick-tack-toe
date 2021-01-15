import Opponents
from Board import TickTackToeGame, Square


class Game:

    def __init__(self, difficulty, size):
        self.opponent = Opponents.opponentFactory.get_opponent('hard',3)
        self.this_game = TickTackToeGame(3)

    def start_game(self):
        for i in range(8):
            move_x, move_y = self.opponent.play(self.this_game)
            self.this_game.set(move_x, move_y, Square.X)
            print(self.this_game)
            print("top left is 0,0")
            x = int(input("enter x:"))
            y = int(input("enter y:"))
            self.this_game.set(x,y, Square.O)
            print(self.this_game.gameBoard.columns)
            print(self.this_game.gameBoard.diagonals)


game = Game('hard', 3)
game.start_game()