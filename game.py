from random import shuffle, randrange
from functools import reduce
import utils

SUITS = ['s', 'h', 'd', 'c']
VALUES = ['9','T','J','Q','K','A']
MAX_SCORE = 10

class Game:

	def __init__(self, players):
		if len(players) != 4:
			raise IllegalPlayException("Game only supports 5 players")
		self._players = players

		# set positions and teams
		self._positions = {}
		self._teams = {}
		self._hands = {p: [] for p in self._players}
		self._inactives = [] # current inactive player for the hand ("alone")
		position = 0
		for p in self._players:
			p.game = self

			# set both player attr and position dict for security
			self._positions[p] = position
			p.position = position
			if p.position % 2 == 0:
				p.team_num = 1
				self._teams[p] = 1
			else:
				p.team_num = 2
				self._teams[p] = 2
			position += 1

		self._game_score = {1: 0, 2: 0}
		self._tricks_score = {1: 0, 2: 0}
		self.__deck = None
		self._top_card = None
		self._trump = None
		self._caller = None
		self._dealer = None

	def play_game(self):
		while (self._game_score[1] < MAX_SCORE and self._game_score[2] < MAX_SCORE):
			self.play_hand()
			print("--------------------")
			print("Score:", self._game_score)
			print("--------------------")

		print("GAME OVER!")

	def play_hand(self):
		# dealer is the "last" player in order
		self._dealer = self._players[3]

		# deal
		self.deal_hand()

		# call trump
		self.call_trump()

		# display trump, top card and hands
		print("====================")
		self.print_hand()

		# play tricks
		print("Tricks:")
		for _ in range(5):
			trick = []

			for p in self._players:
				card = p.action(trick)
				if p not in self._inactives:
					if len(trick) > 0 and p.has_suit(trick[0][1]) and card[1] != trick[0][1]:
						raise IllegalPlayException("Must play the lead suit if you've got it")
					if card not in self._hands[p]:
						raise IllegalPlayException("Player doesn't have that card to play")
					trick.append(card)
					self._hands[p].remove(card) # Game

			winning_card = utils.best_card(trick, self._trump, trick[0])
			winning_player = self._players[trick.index(winning_card)]
			self._tricks_score[self._teams[winning_player]] += 1
			self._rotate_until(winning_player)
			print(winning_player.name, winning_card, trick)

		# score
		self.score_hand()

		# reset
		self._trump = None
		self._top_card = None
		self._inactives = []
		for team_num in range(1, 3):
			self._tricks_score[team_num] = 0

		for p in self._players:
			self._hands[p] = [] # Game
			p.active = True

		# rotate dealer (rotate positions)
		self._rotate_until(self._dealer)
		self._rotate()

	def deal_hand(self):
		self.__deck = [val + suit for val in VALUES for suit in SUITS]
		shuffle(self.__deck)

		# euchre style dealing, for true authenticity
		for p in self._players:
			for _ in range(randrange(1,5)):
				card = self.__deck.pop()
				self._hands[p].append(card) # Game

		for p in self._players:
			for _ in range(5-len(self._hands[p])):
				card = self.__deck.pop()
				self._hands[p].append(card) # Game

		self._top_card = self.__deck.pop()

	def call_trump(self):
		for p in self._players:
			call_result = p.call(self._top_card)
			if call_result != False:
				self._hands[self._dealer].append(self._top_card) # Game
				discard = self._dealer.discard()

				if discard not in self._hands[self._dealer]:
					raise IllegalPlayException("Dealer must discard card that was in hand")
				self._hands[self._dealer].remove(discard) # Game
				
				self._trump = self._top_card[1]

				if call_result == "alone":
					self._inactives.append(self._teammate_for(p))
					self._teammate_for(p).active = False

				# tell players and game who called
				self._caller = p
				for pl in self._players:
					pl.end_call(self._positions[p], self._trump)
				return
			print(p.name, ":", self._trump)

		self.print_hand()

		for p in self._players:
			call_result = p.call(None)

			if call_result not in SUITS and p == self._dealer:
				raise IllegalPlayException("The dealer got screwed - You have to call something!")
			if call_result == self._top_card[1]:
				raise IllegalPlayException("Can't call the face up card after it's flipped")
			if call_result in SUITS:
				self._trump = call_result

				# tell players and game who called
				self._caller = p
				for pl in self._players:
					pl.end_call(self._positions[p], self._trump)
				return

	def score_hand(self):
		calling_team = self._teams[self._caller]
		non_calling_team = (calling_team % 2) + 1
		if self._tricks_score[calling_team] > self._tricks_score[non_calling_team]:
			if self._tricks_score[calling_team] == 5:
				team_players = [p for p in self._players if self._teams[p] == calling_team]
				went_alone = reduce(lambda x, y: x not in self._inactives or y not in self._inactives, team_players)
				if went_alone:
					self._game_score[calling_team] += 4
				else:
					self._game_score[calling_team] += 2
			else:
				self._game_score[calling_team] += 1
		else:
			self._game_score[non_calling_team] += 2

	def print_hand(self):
		""" Print hand for each player """
		print("--------------------")
		print("Trump:    ", self._trump)
		print("Top Card: ", self._top_card)
		print("--------------------")
		print("Hands:")
		for p in self._players:
			if p not in self._inactives:
				print(self._positions[p], p.name, self._hands[p])
			else:
				print(self._positions[p], p.name, "*** asleep ***")
		print("--------------------")

	def _teammate_for(self, player):
		""" Return teammate of player """
		return self._players[self._positions[(player.num + 2) % 4]]

	def _rotate(self):
		""" Rotate players in self._players so that player after dealer becomes dealer """
		self._players = self._players[1:] + self._players[:1]

	def _rotate_until(self, player_at_front):
		""" Rotate players in self._players until player_at_front is as such """
		while self._players[0] != player_at_front:
			self._rotate()

	def hand_for(self, player):
		""" Return hand of specified player """
		return self._hands[player]

	def position_for(self, player):
		""" Return position of specified player """
		return self._positions[player]

	def team_num_for(self, player):
		""" Return team_num of specified player """
		if player in self._teams[1]:
			return 1
		elif player in self._teams[2]:
			return 2
		else:
			raise Exception("You don't appear to be on either team :/")

	def is_player_active(self, player):
		""" Return True if player is active this hand """
		return player not in self._inactives

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
