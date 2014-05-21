import random
from judgingyou import deck

randomizer = random.Random()

def makeDeck(deckType,includedDecks,decks):
	"""supported deck types are prompts and answers
	includedDecks is a list of deckCodes"""
	#make list of cards in order
	result = {}
	result['deck'] = []
	result['deckType'] = deckType

	for deckCode in includedDecks:
		thisDeck = decks[deckCode][deckType]
		keyList = thisDeck.keys()
		for key in keyList:
			result['deck'].append(deckCode + '-' + str(key))

	shuffleDeck(result['deck'])
	result['deckLen'] = len(result['deck'])
	result['remainingCardsInDeck'] = len(result['deck'])

	return result

def getCard():
	pass

def dealCard(deckType):
	"""assigns card to user"""
	# TODO: if remainingCardsInDeck == 0, makeDeck with discards, shuffle
	# pop card
	# assign card to player --> hand
	# update remainingCardsInDeck
	pass

def shuffleDeck(deck):
	# TODO: reseed the random function before shuffling
	return randomizer.shuffle(deck)