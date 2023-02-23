from random import shuffle, randrange
from functools import reduce
from game import Game
import utils

class ZachSimGame(Game):

	def __init__(self, players):
		super().__init__(players)

	def play_game(self):
		super().play_game()

	def play_hand(self):
		super().play_hand()

	def deal_hand(self):
		super().deal_hand()

	def call_trump(self):
		return super().call_trump()

	def score_hand(self):
		super().score_hand()

	def print_hand(self):
		super().print_hand()

	def _teammate_for(self, player):
		return super()._teammate_for(player)

	def _rotate(self):
		return super()._rotate()

	def _rotate_until(self, player_at_front):
		super()._rotate_until(player_at_front)

	def hand_for(self, player):
		return super().hand_for(player)

	def position_for(self, player):
		return super().position_for(player)

	def team_num_for(self, player):
		return super().team_num_for(player)

	def is_player_active(self, player):
		return super().is_player_active(player)

"""
	@property
	def top_card(self):
		return self._top_card

	@property
	def trump(self):
		return self._trump

	@property
	def caller_pos(self):
		return self._positions[self._caller]

	@property
	def dealer_pos(self):
		return self._positions[self._dealer]

	@property
	def tricks_score(self):
		return self._tricks_score

	@property
	def game_score(self):
		return self._game_score

class IllegalPlayException(Exception):
	pass

"""
