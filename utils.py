VALUE_MAP = {'9': 1, 'T': 2, 'J': 3, 'Q': 4, 'K': 5, 'A': 6}

def best_card(cards, trump=None, lead=None):
	""" Calculate winning card from list of cards

	Trump and lead suit must be specified, otherwise normal order is assumed.

	I am displeased with the lack of elegance in this function.

	"""
	val_map = {}
	for c in cards:
		val = VALUE_MAP[c[0]]
		if lead == c[1] and not trump == c[1]:
			val *= 10
		if trump == c[1]:
			val *= 100
			if c[0] == 'J':
				val = val*10 + 5
		if trump == same_color(c[1]) and c[0] == 'J':
			val = val*1000 + 3

		val_map[c] = val

	return sorted(val_map.items(), key=lambda x: x[1], reverse=True)[0][0]

def same_color(suit):
	""" Return other suit of the same same color

	I'm embarrased I had to write this function.

	"""
	if suit == 's':
		return 'c'
	elif suit == 'c':
		return 's'
	elif suit == 'd':
		return 'h'
	elif suit == 'h':
		return 'd'

def follow_suit_priority(card, trump, lead):
	""" Calculate priority order of "follow suit" rule.

	Trump suit and lead card must be specified.

        priority order of "follow suit" rules:
	1) must match suit of lead card
	   - if suit of lead card is trump, then either trump or left bower is acceptable
	2) must match suit of trump
	   - if suit of lead card is trump, then either trump or left bower is acceptable
	3) anything else

	"""

	leftbower = 'J' + same_color(trump)

	# Determine the suit of the lead card.  This considers the left bower as trump.
	suit_to_follow = lead[1]
	if lead == leftbower:
		suit_to_follow = trump

	# Determine the priority of the card that was played.  Note that this
	# is slightly different than the logic in best_card.
	if suit_to_follow == card[1]:
		val = 1
	elif suit_to_follow == trump and card == leftbower:
		val = 1
	elif trump == card[1]:
		val = 2
	elif trump == card[1] and card == leftbower:
		val = 2
	else:
		val = 3

	return val

def did_follow_suit(cards, card, trump, lead):
	""" Calculate if card followed suit given the cards in the hand

	Trump suit and lead card must be specified.

	"""

	# Determine the priority of the card played
	card_pri = follow_suit_priority(card, trump, lead)

	# Determine the priorities of all other cards in the hand
	cards_pri = {}
	for c in cards:
		cards_pri[c] = follow_suit_priority(c, trump, lead)

	best_pri = sorted(cards_pri.items(), key=lambda x: x[1])[0][1]

	# If the card played has the same priority as the best priority,
	# then the follow suit rules were followed.  (Otherwise, there
	# was a card that had higher priority ==> should have been played.)
	if card_pri == best_pri:
		return True

	return False

# Should be unit tests
# print best_card(['Qs', 'As'])                        # As
# print best_card(['As', 'Jh'], 'h')                   # Jh
# print best_card(['Jc', 'Js'], 'h', 's')              # Js
# print best_card(['Jc', 'Js', 'Jh'], 'h', 's')        # Js
# print best_card(['Jc', 'Js', 'Jh', 'Jd'], 'h', 's')  # Js
# print best_card(['Jc', 'Js', 'Ah', 'Jd'], 'h', 's')  # Js

# print did_follow_suit(['Jc', 'Js', Kc'], 'Jc', 's', 's') # false, 'Js'
# print did_follow_suit(['Jc', 'As', Kc'], 'Jc', 's', 's') # false, 'Jc'
# print did_follow_suit(['Jc', 'Js', Kc'], 'Jc', 's', 'c') # true, 'Jc'
# print did_follow_suit(['Jc', 'As', Kc'], 'Jc', 's', 'c') # true, 'Jc'
# print did_follow_suit(['Td', '9s', 'Ts', '9c', 'Ah'], 'Ah', 'h', 'h') # true, 'Ah'

