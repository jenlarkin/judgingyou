from uuid import uuid1 as generateuuid
import judgingyou.deck as deck, judgingyou.gameDeck as gameDeck, judgingyou.gameRound as gameRound, judgingyou.hand as hand, judgingyou.card as card

class Game(object):

	def __init__(self, admin):
		#set up default values
		self.game_id = generateuuid()
		self.admin = admin
		self.maxPlayers = 12
		self.maxViewers = 5
		self.hasWaitlist = False
		self.allowSeatholding = False
		self.winningScore = 6
		self.handLimit = 9
		self.roundTimeout = 2
		self.timeoutBeforeKick = 3
		self.hasPassword = False
		self.password = None
		self.includedDecks = {}
		self.allPlayers = []
		self.heldSeats = []
		self.waitlist = []
		self.referenceDeck = {}
		self.gameDeckSet = {}

	def scoreRound():
		pass 

	def startRound(self):
		#TODO: hand should be in the player, who should be in the game
		# also, new hand every round is for testing only
		playerHand = hand.Hand()
		playerHand.handLimit = 9
		result =  playerHand.newHand(self.gameDeckSet,self.referenceDeck)
		return result

	def getPrompt(self):
		promptCode = self.gameDeckSet['prompts']['deck'].pop()
		self.prompt = card.getCard(self.referenceDeck,promptCode,'prompts')
		return self.prompt

	def makeReferenceDeckSet(self,included,availableDecks):
		self.referenceDeck = deck.filterDecks(availableDecks,'included',included)

	def makeGameDeckSet(self,includedDecks,availableDecks):
		self.makeReferenceDeckSet(includedDecks,availableDecks)

		self.gameDeckSet = {}
		self.gameDeckSet['prompts'] = gameDeck.makeDeck('prompts',includedDecks,availableDecks)
		self.gameDeckSet['answers'] = gameDeck.makeDeck('answers',includedDecks,availableDecks)

	def shuffleGameDeckSet(self,gameDeckSet):
		gameDeck.shuffleDeck(self.gameDeckSet['prompts']['deck'])
		gameDeck.shuffleDeck(self.gameDeckSet['answers']['deck'])
	

