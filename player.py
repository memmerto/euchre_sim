import utils

class Player:

	def __init__(self, name):
		self.name = name
		self.game = None

	def action(self, trick):
		""" Play a card in trick

		trick -- list of cards played in order, trick[0] is lead card

		"""
		card_to_play = None
		for card in self.game.hand_for(self):
			if not trick:
				card_to_play = self.game.hand_for(self)[0]
			elif trick[0][1] == card[1]:
				card_to_play = card
		if not card_to_play:
			card_to_play = self.game.hand_for(self)[0]
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

		Return the string (like 'As' or 'Th'), it will automatically be removed from hand

		"""
		return self.game.hand_for(self)[0]

	def end_call(self, caller_position, trump):
		""" Communicate result of calling to player

		caller_postion -- current position of player who called, so if your position is 0, your
			teammate would be 2
		trump -- the trump that was called.  can also be accessed via self.game.trump

		"""
		pass

	def end_trick(self, winner_position, lead_position, trick):
		""" Communicate result of trick to player

		winner_position - position of winner of trick
		lead_position - position of player who led trick, used to tell who played what

		"""
		pass

	def has_suit(self, suit):
		""" Return True if player has specified suit in hand, otherwise false """
		return suit in [card[1] for card in self.game.hand_for(self)]
