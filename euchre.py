from random import shuffle, randrange
#import matplotlib.pyplot as plt

class Game:

	def __init__(self, players):
		self.__players = players
		position = 0
		for p in self.__players:
			p.position = position
			if p.position % 2 == 0:
				p.team_num = 1
			else:
				p.team_num = 2
			position += 1

		self.team_one_score = 0
		self.team_two_score = 0
		self.__deck = None
		self.top_card = None


	def deal_hand(self):
		self.__deck = [val + suit for val in
						['9','T','J','Q','K','A'] for suit in ['s', 'h', 'd', 'c']]
		shuffle(self.__deck)

		# order players based on position values (0 for dealer)
		self.__players = sorted(self.__players, key=lambda x: x.position)

		# euchre style dealing, for true authenticity
		for p in self.__players:
			for _ in xrange(randrange(1,5)):
				p.receive_card(self.__deck.pop())

		for p in self.__players:
			for _ in xrange(5-len(p.hand)):
				p.receive_card(self.__deck.pop())

#		for p in self.__players:
#			print p.name, p.hand

		self.top_card = self.__deck.pop()

#		print "top card", self.top_card

	def play_hand(self):
		# deal
		deal_hand()

		# call

		# play tricks

		# score

		# rotate dealer (rotate positions)
		for p in self.


	def play_game(self):
		while (self.team_one_score < 10 and self.team_two_score < 10):
			play_hand()

		print "GAME OVER!"



class Player:

	def __init__(self, name):
		self.name = name
		self.team_num = None
		self.hand = []
		self.position = None
		self.active = True # set to False to "go it alone"/"put partner to sleep"

	def action(self):
		pass

	def call(self):
		pass

	def receive_card(self, card):
		self.hand.append(card)



p1 = Player("Henry")
p2 = Player("Alex")
p3 = Player("Paul")
p4 = Player("Erica/Sarah")

g = Game([p1, p2, p3, p4])
g.deal_hand()