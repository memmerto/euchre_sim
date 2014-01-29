from random import shuffle, randrange
import util

SUITS = ['s', 'h', 'd', 'c']
VALUES = ['9','T','J','Q','K','A']

VALUE_MAP = {'9': 0, 'T': 1, 'J': 2, 'Q': 3, 'K': 4, 'A': 5}

class Game:

	def __init__(self, players):
		if len(players) != 4:
			raise Exception("Game only supports 5 players")
		self._players = players

		position = 0
		for p in self._players:
			p.game = self
			p.position = position
			if p.position % 2 == 0:
				p.team_num = 1
			else:
				p.team_num = 2
			position += 1

		self._team_one_score = 0
		self._team_two_score = 0
		self._team_one_tricks = 0
		self._team_two_tricks = 0
		self.__deck = None
		self._top_card = None
		self._trump = None

	def play_game(self):
		while (self.team_one_score < 10 and self.team_two_score < 10):
			play_hand()

		print "GAME OVER!"

	def play_hand(self):
		# order players based on position values (3 for dealer)
		self._players = sorted(self._players, key=lambda x: x.position)

		# deal
		self.deal_hand()
		self.print_hand()
		print "top card", self._top_card

		# call trump
		self.call_trump()
		self.print_hand()

		# play tricks
		start_pos = 0
		for _ in xrange(5):
			action_pos = start_pos
			trick = []
			for _ in xrange(4):
				player = self._players[action_pos % 4]
				if player.active:
					player.action(trick)
				
				action_pos += 1
			start_pos = 0


		# score
		# TODO
		self._team_one_tricks = 0
		self._team_two_tricks = 0
		self._team_one_score = 999
		self._team_two_score = 999

		# rotate dealer (rotate positions)
		for p in self._players:
			if p.position == 0:
				p.position = 3
			else:
				p.position -= 1

	def deal_hand(self):
		self.__deck = [val + suit for val in VALUES for suit in SUITS]
		shuffle(self.__deck)
		self._trump = None

		# euchre style dealing, for true authenticity
		for p in self._players:
			for _ in xrange(randrange(1,5)):
				p.receive_card(self.__deck.pop())

		for p in self._players:
			for _ in xrange(5-len(p.hand)):
				p.receive_card(self.__deck.pop())

		self._top_card = self.__deck.pop()

	def call_trump(self):
		dealer = self._players[3]

		for p in self._players:
			call_result = p.call(self._top_card)
			if call_result != False:
				dealer.receive_card(self._top_card)
				discard = dealer.discard()

				# TODO: check that an appropriate card is discarded
				dealer.hand.remove(discard)
				
				self._trump = self._top_card[1]
				if call_result == "alone":
					self._teammate_for(p).active = False

				# tell players who called
				for pl in self._players:
					pl.end_call(p.position, self._trump)
				return
			print p.name, ":", self._trump

		self.print_hand()

		for p in self._players:
			call_result = p.call(None)

			if call_result not in SUITS and p.position == 3:
				raise Exception("The dealer got screwed - You have to call something!")
			if call_result == self._top_card[1]:
				raise Exception("Can't call the face up card after it's flipped")
			if call_result in SUITS:
				self._trump = call_result
				for pl in self._players:
					pl.end_call(p.position, self._trump)
				return

	def print_hand(self):
		""" Print hand for each player """
		print "------------------- Trump:", self._trump, "---------------"
		for p in self._players:
			if p.active:
				print p.position, p.name, p.hand
			else:
				print p.position, p.name, "*** asleep ***"

	def _teammate_for(self, player):
		return filter(lambda teammate: teammate.team_num == player.team_num and
									   teammate.position != player.position,
									   self._players)[0]

	# Properties
	@property
	def top_card(self):
		return self._top_card

	@property
	def trump(self):
		return self._trump

	@property
	def team_one_tricks(self):
		return self._team_one_tricks

	@property
	def team_two_tricks(self):
		return self._team_two_tricks

	@property
	def team_one_score(self):
		return self._team_one_score

	@property
	def team_two_score(self):
		return self._team_two_score


class Player:

	def __init__(self, name):
		self.name = name
		self.team_num = None
		self.hand = []
		self.position = None
		self.active = True # set to False to "go it alone"/"put partner to sleep"
		self.game = None

	def action(self, trick):
		""" Play a card in trick

		trick -- list of cards played in order

		"""
		return False

	def call(self, top_card):
		""" Call trump or pass

		If top_card is specified return:
			True - call the top_card suit as trump
			"alone" - call that suit trump, and put partner to sleep / go alone
			False - pass

		If top_card is None, return:
			's', 'c', 'h', 'd' - call specified suit as trump
			False - pass
			*** note if player is dealer (position == 3), player can't pass

		"""
		if top_card:
			return False
		else:
			if self.position == 2:
				return 's'

	def discard(self):
		""" Choose card to discard after picking up

		"""
		return self.hand[0]

	def end_call(self, caller_position, trump):
		""" Communicate result of calling to player

		"""
		return

	def end_trick(self):
		""" Communicate result of trick to player

		"""
		return

	def receive_card(self, card):
		self.hand.append(card)



p1 = Player("Henry")
p2 = Player("Alex")
p3 = Player("Paul")
p4 = Player("Erica/Sarah")

g = Game([p1, p2, p3, p4])
g.play_hand()

