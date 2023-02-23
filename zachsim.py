from game import Game
from zachsim_player import ZachSimPlayer

if __name__ == "__main__":
	p1 = ZachSimPlayer("Alma")
	p2 = ZachSimPlayer("Brad")
	p3 = ZachSimPlayer("Carl")
	p4 = ZachSimPlayer("Dave")

	g = Game([p1, p2, p3, p4])
	g.play_game()
