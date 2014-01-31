from game import Game
from player import Player

if __name__ == "__main__":
	p1 = Player("Henry")
	p2 = Player("Alex")
	p3 = Player("Paul")
	p4 = Player("Erica/Sarah")

	g = Game([p1, p2, p3, p4])
	g.play_game()

