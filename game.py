from random import shuffle, randrange
import utils

SUITS = ['s', 'h', 'd', 'c']
VALUES = ['9','T','J','Q','K','A']

class Game:

	def __init__(self, players):
		if len(players) != 4:
			raise IllegalPlayException("Game only supports 5 players")
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

		self._game_score = {1: 0, 2: 0}
		self._tricks_score = {1: 0, 2: 0}
		self.__deck = None
		self._top_card = None
		self._trump = None
		self._caller = None

	def play_game(self):
		while (self._game_score[1] < 10 and self._game_score[2] < 10):
			self.play_hand()
			print "===============> SCORE:", self._game_score

		print "GAME OVER!"

	def play_hand(self):
		# order players based on position values (3 for dealer)
		self._players = sorted(self._players, key=lambda x: x.position)

		# deal
		self.deal_hand()

		# call trump
		self.call_trump()
		self.print_hand()
		print "top card", self._top_card


		# play tricks
		start_pos = 0
		for _ in xrange(5):
			action_pos = start_pos
			trick = []

			for _ in xrange(4):
				player = self._players[action_pos % 4]
				if _ == 0:
					print "**********"
					print player.name, "is leading"
				if player.active:
					card = player.action(trick)
					if len(trick) > 0 and player.has_suit(trick[0][1]) and card[1] != trick[0][1]:
						raise IllegalPlayException("Must play the lead suit if you've got it")
					trick.append(card)
					player.hand.remove(card)
				action_pos += 1

			winning_card = utils.best_card(trick, self._trump, trick[0])
			winning_player = self._players[(trick.index(winning_card) + start_pos) % 4]
			start_pos = winning_player.position
			self._tricks_score[winning_player.team_num] += 1

			print winning_player.name, winning_card, trick

		# score
		self.score_hand()

		# reset
		self._trump = None
		self._top_card = None
		for team_num in xrange(1, 3):
			self._tricks_score[team_num] = 0

		for p in self._players:
			p.hand = []
			p.active = True

			# rotate dealer (rotate positions)
			if p.position == 0:
				p.position = 3
			else:
				p.position -= 1

	def deal_hand(self):
		self.__deck = [val + suit for val in VALUES for suit in SUITS]
		shuffle(self.__deck)

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

				# tell players and game who called
				self._caller = p
				for pl in self._players:
					pl.end_call(p.position, self._trump)
				return
			print p.name, ":", self._trump

		self.print_hand()

		for p in self._players:
			call_result = p.call(None)

			if call_result not in SUITS and p.position == 3:
				raise IllegalPlayException("The dealer got screwed - You have to call something!")
			if call_result == self._top_card[1]:
				raise IllegalPlayException("Can't call the face up card after it's flipped")
			if call_result in SUITS:
				self._trump = call_result

				# tell players and game who called
				self._caller = p
				for pl in self._players:
					pl.end_call(p.position, self._trump)
				return

	def score_hand(self):
		calling_team = self._caller.team_num
		non_calling_team = (calling_team % 2) + 1
		if self._tricks_score[calling_team] > self._tricks_score[non_calling_team]:
			if self._tricks_score[calling_team] == 5:
				team_players = [p for p in self._players if p.team_num == calling_team]
				went_alone = reduce(lambda x, y: not x.active or not y.active, team_players)
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
		print "------------------- Trump:", self._trump, "---------------"
		for p in self._players:
			if p.active:
				print p.position, p.name, p.hand
			else:
				print p.position, p.name, "*** asleep ***"

	def _teammate_for(self, player):
		""" Return teammate of player """
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
	def caller(self):
		return self._caller

	@property
	def tricks_score(self):
		return self._tricks_score

	@property
	def game_score(self):
		return self._game_score

class IllegalPlayException(Exception):
	pass