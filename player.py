import util

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

		trick -- list of cards played in order, trick[0] is lead card

		"""
		card_to_play = None
		for card in self.hand:
			if not trick:
				card_to_play = self.hand[0]
			elif trick[0][1] == card[1]:
				card_to_play = card
		if not card_to_play:
			card_to_play = self.hand[0]
		return card_to_play

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
		return True

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
		""" Receive card into player's hand """
		self.hand.append(card)

	def has_suit(self, suit):
		""" Return True if player has specified suit in hand, otherwise false """
		return suit in [card[1] for card in self.hand]


