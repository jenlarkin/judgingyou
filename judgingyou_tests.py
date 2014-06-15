from nose.tools import *
import unittest
from judgingyou import app
import judgingyou
import judgingyou.deck as deck


class JudgingYouTestCase(unittest.TestCase):
	def setUp(self):
		judgingyou.app.config['TESTING'] = True
		self.app = judgingyou.app.test_client()
		self.app.CSVPath = '../../judgingyou-decks/judgingyou-decks/testDecks/'
		self.app.activeDeckList = ['NCABD','CABD','NCAE','CAE','ADPROMPT','ADANSWER']
		print "SETUP!"

	def tearDown(self):
		print "TEAR DOWN!"

	def test_basic(self):
		print "I RAN!"

	def test_deckMetadataSetup(self):
		self.deckDefinitions = deck.getAvailableDecks(self.app.CSVPath)
		print "Deck Metadata set up did not throw exception."

	def test_deckSetSetup(self):
		self.availableDecks = deck.loadActiveDecks(deck.getAvailableDecks(self.app.CSVPath), self.app.CSVPath)
		print "Deck Set set up did not throw exception."

if __name__ == '__main__':
	unittest.main()