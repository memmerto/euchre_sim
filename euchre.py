from random import shuffle
#import matplotlib.pyplot as plt

class Game:

	def __init__(self, players):
		self.__deck = [val + suit for val in
						[9,10,'J','Q','K','A'] for suit in ['s', 'h', 'd', 'c']]
		self.players = players




class Player:

	def __init__(self, name, position):
		self.position = position
		self.name = name
		self.hand = []

	def action():
		pass

	def call():
		pass