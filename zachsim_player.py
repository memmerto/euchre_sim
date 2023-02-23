import utils
from player import Player

class ZachSimPlayer(Player):

	def __init__(self, name):
		super().__init__(name)

	def action(self, trick):
		""" Play a card in trick """
		return super().action(trick)

	def call(self, top_card):
		""" Call trump or pass """
		return super().call(top_card)

	def discard(self):
		""" Choose card to discard after picking up """
		return super().discard()

	def end_call(self, caller_position, trump):
		""" Communicate result of calling to player """
		return super().end_call(caller_position, trump)

	def end_trick(self):
		""" Communicate result of trick to player """
		return super().end_trick()

	def has_suit(self,suit):
		""" Return True if player has specified suit in hand, otherwise false """
		return super().has_suit(suit)
