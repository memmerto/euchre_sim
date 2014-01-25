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
		self.trump = None


	def deal_hand(self):
		self.__deck = [val + suit for val in
						['9','T','J','Q','K','A'] for suit in ['s', 'h', 'd', 'c']]
		shuffle(self.__deck)
		self.trump = None

		# euchre style dealing, for true authenticity
		for p in self.__players:
			for _ in xrange(randrange(1,5)):
				p.receive_card(self.__deck.pop())

		for p in self.__players:
			for _ in xrange(5-len(p.hand)):
				p.receive_card(self.__deck.pop())

		self.top_card = self.__deck.pop()

	def play_hand(self):
		team_one_tricks = 0
		team_two_tricks = 0

		# order players based on position values (3 for dealer)
		self.__players = sorted(self.__players, key=lambda x: x.position)
		dealer = self.__players[3]

		# deal
		self.deal_hand()
		self.print_hand()
		print "top card", self.top_card

		# call trump
		for p in self.__players:
			call_result = p.call(self.top_card)
			if call_result != False:
				dealer.hand.remove(dealer.exchange_card(self.top_card))
				dealer.receive_card(self.top_card)
				if call_result == "alone":
					self.teammate_for(p).active = False
				break

		self.print_hand()

		for p in self.__players:
			pass


		# play tricks

		# score

		# rotate dealer (rotate positions)
		for p in self.__players:
			if p.position == 0:
				p.position = 3
			else:
				p.position -= 1


	def play_game(self):
		while (self.team_one_score < 10 and self.team_two_score < 10):
			play_hand()

		print "GAME OVER!"

	def print_hand(self):
		""" Print hand for each player"""
		print "----------------------------------------------"
		for p in self.__players:
			if p.active:
				print p.position, p.name, p.hand
			else:
				print p.position, p.name, "*** asleep ***"

	def teammate_for(self, player):
		return filter(lambda teammate: teammate.team_num == player.team_num and
									   teammate.position != player.position,
									   self.__players)[0]

class Player:

	def __init__(self, name):
		self.name = name
		self.team_num = None
		self.hand = []
		self.position = None
		self.active = True # set to False to "go it alone"/"put partner to sleep"

	def action(self):
		""" Play a card in trick

		"""
		return False

	def call(self, top_card):
		""" Call trump

		"""
		return 'alone'

	def exchange_card(self, top_card):
		""" Choose card

		"""
		return self.hand[0]

	def receive_card(self, card):
		self.hand.append(card)



p1 = Player("Henry")
p2 = Player("Alex")
p3 = Player("Paul")
p4 = Player("Erica/Sarah")

g = Game([p1, p2, p3, p4])
g.play_hand()