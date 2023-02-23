from game import Game
from player import Player
from my_player import MyPlayer

if __name__ == "__main__":
	p1 = Player("Alma")
	p2 = Player("Brad")
	p3 = Player("Carl")
	p4 = Player("Dave")

	g = Game([p1, p2, p3, p4])
	g.play_game()
