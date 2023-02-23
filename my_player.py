import utils
from player import Player

class MyPlayer(Player):

	def __init__(self, name):
		super().__init__(name)

	def action(self, trick):
		""" Play a card in trick """
		pass

	def call(self, top_card):
		""" Call trump or pass """
		pass

	def discard(self):
		""" Choose card to discard after picking up	"""
		pass

	def end_call(self, caller_position, trump):
		""" Communicate result of calling to player """
		pass

	def end_trick(self):
		""" Communicate result of trick to player """
		pass
