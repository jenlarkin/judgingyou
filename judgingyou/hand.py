import judgingyou.card as card

class Hand(object):

	def __init__(self):
		self.cards = []
		self.handLimit = 7

	def setHandLimit(self,handLimit):
		self.handLimit = handLimit

	def newHand(self,gameDeckSet,referenceDeck):
		cardCodes = []
		for i in range(self.handLimit):
			cardCodes.append(gameDeckSet['answers']['deck'].pop())


		for cardID in cardCodes:
			cardDict = card.getCard(referenceDeck,cardID,'answers')
			self.cards.append(cardDict)
		return self.cards

	def playAnswer():
		pass
