from random import shuffle, randrange
from functools import reduce
from game import Game
import utils

SUITS = ['s', 'h', 'd', 'c']
VALUES = ['9','T','J','Q','K','A']

MAX_SCORE = 100

class ZachSimGame(Game):

	# override so that we can set MAX_SCORE
	def play_game(self):
		while (self._game_score[1] < MAX_SCORE and self._game_score[2] < MAX_SCORE):
			self.play_hand()
			print("--------------------")
			print("Score:", self._game_score)
			print("--------------------")

		print("GAME OVER!")

	# override so that we fix the dealer (doesn't change each hand)
	# override so that we always play highest lead suit / lowest non-trump
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

		# play starts with the "first" player in order
		leader = 0

		# number of players
		numplayers = len(self._players)

		# play tricks
		print("Tricks:")
		for _ in range(5):
			# cards played in order from [leader..leader+numplayers-1]%numplayers
			trick = []

			# loop through players, starting with the leader
			for n in range(numplayers):
				p = self._players[(leader+n)%numplayers]

				card = p.action(trick)
				if p not in self._inactives:
					# must follow suit
					if len(trick) > 0 and not utils.did_follow_suit(self._hands[p], card, self._trump, trick[0]):
						print("DEBUG: lead card: ", trick[0], " card: ", card, "hand: ", self._hands[p])
						raise IllegalPlayException("Must follow suit")
					# internal logic error
					if card not in self._hands[p]:
						raise IllegalPlayException("Player doesn't have that card to play")
					trick.append(card)
					self._hands[p].remove(card) # Game

			winning_card = utils.best_card(trick, self._trump, trick[0][1])
			winning_player_index = (trick.index(winning_card) + leader) % numplayers
			winning_player = self._players[winning_player_index]
			self._tricks_score[self._teams[winning_player]] += 1
			print(winning_player.name, winning_card, trick)

			# move leader to winning player
			leader = winning_player_index

		# score
		self.score_hand()

		# reset
		self._trump = None
		self._leftbower = None
		self._top_card = None
		self._inactives = []
		for team_num in range(1, 3):
			self._tricks_score[team_num] = 0

		for p in self._players:
			self._hands[p] = [] # Game
			p.active = True

		# don't change dealer each hand

	# override so that we can rig the deal
	def deal_hand(self):
		self.__deck = [val + suit for val in VALUES for suit in SUITS]
		shuffle(self.__deck)

		# rig the game!

		# 0) set trump (before we "deal")
		self.call_trump()

		# 1) give the first player some trump
                #    A) Jh, Kh, Th, 9h
                #    B) Jd, Kh, Th, 9h
		self.__deck.remove("Jh")
		self._hands[self._players[0]].append("Jh")
		self.__deck.remove("Kh")
		self._hands[self._players[0]].append("Kh")
		self.__deck.remove("Th")
		self._hands[self._players[0]].append("Th")
		self.__deck.remove("9h")
		self._hands[self._players[0]].append("9h")

		# 2) give the dealer (4th player) one trump
		#    Either Qh or Ah or Jh, but never Jd, since that would force trump to be diamons
		self.__deck.remove("Qh")
		self._hands[self._players[3]].append("Qh")

		# 3) deal the rest
		count = 0
		while (len(self.__deck) > 4):
			for p in self._players:
				if (len(self._hands[p]) < 5):
					card = self.__deck.pop(0)
					# p0 cannot pick up any more trump
					if (p == self._players[0]):
						while (card[1] == 'h' or card == 'Jd'):
							count=count+1
							self.__deck.append(card)
							card = self.__deck.pop(0)
							if (count>10):
								print(card)
								print(self.__deck)
		
					self._hands[p].append(card)

		self._top_card = self.__deck.pop()

	# override so that we can force trump, called by dealer
	def call_trump(self):
		# dealer always chooses trump to be hearts
		self._trump = 'h'
		self._caller = self._players[3]

		# set up left bower
		self._leftbower = 'J' + utils.same_color(self._trump)

class IllegalPlayException(Exception):
        pass
