import utils
from player import Player

class ZachSimPlayer(Player):

	def __init__(self, name):
		super().__init__(name)

	def action(self, trick):
		return super().action(trick)

	def action(self, trick):
		card_to_play = None

		# playing the lead
		if not trick:
			# lead: play highest trump
			card_to_play = self.highest_trump()

			# lead: if no trump, highest non-trump
			if not card_to_play:
				card_to_play = self.highest_non_trump()

		# following the lead
		else:
			# follow suit: highest card, iff you can beat the leader
			card_to_play = self.highest_of_suit_beats_lead(trick[0])

			# follow suit: throw low
			if not card_to_play:
				card_to_play = self.lowest_of_suit(trick[0][1])

		# can't follow the lead
		if not card_to_play:
			card_to_play = self.lowest_overall()

		if not card_to_play:
			# TODO: blow up!
			pass

		return card_to_play

	def call(self, top_card):
		return super().call(top_card)

	def discard(self):
		return super().discard()

	def end_call(self, caller_position, trump):
		return super().end_call(caller_position, trump)

	def end_trick(self):
		return super().end_trick()

	def has_suit(self,suit):
		return super().has_suit(suit)

	def highest_trump(self):
		card_to_play = None
		trumps = []
		rightbower = 'J' + self.game._trump
		leftbower = 'J' + utils.same_color(self.game._trump)

		# get list of trump cards in hand
		for card in self.game.hand_for(self):
			if card[1] == self.game._trump or card == leftbower:
				trumps.append(card)

		# sort trumps highest to lowest
		if (len(trumps) > 0):
			card_order = [ 'J', 'A', 'K', 'Q', 'T', '9' ]
			#suit_order = [ self.game._trump, utils.same_color(self.game._trump) ]
			sorted_trumps = sorted(trumps, key=lambda c: (card_order.index(c[0])))
			#TODO: sort to get the bowers in here
			card_to_play = sorted_trumps[0]

		return card_to_play

	def highest_non_trump(self):
		card_to_play = None
		nontrumps = []
		rightbower = 'J' + self.game._trump
		leftbower = 'J' + utils.same_color(self.game._trump)

		# get list of non-trump cards in hand
		for card in self.game.hand_for(self):
			if card[1] != self.game._trump and card != leftbower:
				nontrumps.append(card)

		# sort non-trumps lowest to highest
		if (len(nontrumps) > 0):
			card_order = [ 'J', 'A', 'K', 'Q', 'T', '9' ]
			sorted_nontrumps = sorted(nontrumps, key=lambda c: (card_order.index(c[0])))
			card_to_play = sorted_nontrumps[0]

		return card_to_play

	def highest_of_suit_beats_lead(self,lead):
		card_to_play = None
		possibles = []
		if lead[1] == self.game._trump:
			leftbower = 'J' + utils.same_color(lead[1]);
		else:
			leftbower = None

		# get list of cards in hand of the same suit (including left bower if suit is trump)
		for card in self.game.hand_for(self):
			if card[1] == lead[1] or card == leftbower:
				possibles.append(card)

		# sort highest to lowest and remove anything that won't beat the lead
		if (len(possibles) > 0):
			card_order = [ 'Jx', 'Jy', 'Ax', 'Kx', 'Qx', 'Tx', '9x' ]
			for n in range(len(card_order)):
				card_order[n] = card_order[n].replace('x', lead[1])
				card_order[n] = card_order[n].replace('y', utils.same_color(lead[1]))

			sorted_possibles = sorted(possibles, key=lambda c: (card_order.index(c)))

			# anything with a smaller index than the lead card will work
			lead_index = card_order.index(lead)
			for card in sorted_possibles:
				if (card_order.index(card) < lead_index):
					card_to_play = card
					break

		return card_to_play

	def lowest_of_suit(self,suit):
		card_to_play = None
		possibles = []
		if suit == self.game._trump:
			leftbower = 'J' + utils.same_color(suit);
		else:
			leftbower = None

		# get list of cards in had of the same suit (including left bower if suit is trump)
		for card in self.game.hand_for(self):
			if card[1] == suit or card == leftbower:
				possibles.append(card);

		# sort lowest to highest
		if (len(possibles) > 0):
			card_order = [ 'Jx', 'Jy', 'Ax', 'Kx', 'Qx', 'Tx', '9x' ]
			for n in range(len(card_order)):
				card_order[n] = card_order[n].replace('x', suit)
				card_order[n] = card_order[n].replace('y', utils.same_color(suit))

			sorted_possibles = sorted(possibles, key=lambda c: (card_order.index(c)), reverse=True)

			card_to_play = sorted_possibles[0]

		return card_to_play

	def lowest_overall(self):
		card_to_play = None
		possibles = self.game.hand_for(self).copy()

		# sort lowest to highest
		if (len(possibles) > 0):
			card_order = [ 'J', 'A', 'K', 'Q', 'T', '9' ]
			sorted_possibles = sorted(possibles, key=lambda c: (card_order.index(c[0])), reverse=True)

			card_to_play = sorted_possibles[0]

		return card_to_play
