import os
from flask import Flask, request, session, g, redirect, url_for, render_template

# Jinja fix for answers deck
# app should be set for UTF-8 anyway, for translation decks
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# end Jinja fix for answers deck

# create application
app = Flask('judgingyou')

app.config.from_object('judgingyou')
# TODO: move this to file
app.config.update(dict(
	DEBUG=True,
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default',
	CSVPATH='../../judgingyou-decks/judgingyou-decks/rawDataExports/',
	ALPHA1DECKS=['ANTISOCIAL','CAHMAIN1','RIDICSTUP'],
	ACTIVEDECKLIST=['ANTISOCIAL','CAHMAIN1','RIDICSTUP']
))
app.config.from_envvar('JUDGINGYOU_SETTINGS', silent=True)

import judgingyou.deck as deck
import judgingyou.game as game
#import views

# TODO: look into making these global variables
CSVPath = app.config['CSVPATH']
alpha1Decks = app.config['ALPHA1DECKS']

# test decks
CSVPath = '../../judgingyou-decks/judgingyou-decks/testDecks/'
alpha1Decks = ['NCABD','CABD','NCAE','CAE','ADPROMPT','ADANSWER']

""" TODO: bootstrap-- code will move by Alpha 2 """
availableDecks = deck.loadActiveDecks(deck.getAvailableDecks(CSVPath), CSVPath)
activeDecks = deck.filterDecks(availableDecks,'active','')
filteredDecks = deck.filterDecks(availableDecks,'included',alpha1Decks)

# TODO: game admin is irrelevant before alpha 2, since no game admin functions exist
thisGame = game.Game('gameAdmin')
thisGameDeckSet = thisGame.makeGameDeckSet(alpha1Decks,activeDecks)

hand = thisGame.startRound()

@app.route('/', methods=['GET','POST'])
def testingNavigation():
	return render_template('testingNav.html')

@app.route('/dumpdecks', methods=['GET','POST'])
def dumpDecks():
	return render_template('dumpDecks.html', decks=availableDecks)

@app.route('/activedecks', methods=['GET','POST'])
def dumpActiveDecks():
	return render_template('dumpDecks.html', decks=activeDecks)

@app.route('/showhand', methods=['GET','POST'])
def showHand():
	#TODO: for now, pull ne prompt and deal new hand. Later, it should come from round
	prompt = thisGame.getPrompt()
	hand = thisGame.startRound()
	return render_template('showHand.html', prompt=prompt, hand=hand)

@app.route('/showgamedeck', methods=['GET','POST'])
def showGameDeckSet():
	# does not create a new game deck set
	return render_template('showGameDeck.html', gameDeck=thisGame.gameDeckSet)

@app.route('/reshufflegamedeck', methods=['GET','POST'])
def reshuffleGameDeckSet():
	# takes the existing game deck set and shuffles it.
	thisGame.shuffleGameDeckSet(thisGame.gameDeckSet)
	return render_template('showGameDeck.html', gameDeck=thisGame.gameDeckSet)

# starts the web app	
if __name__ == '__main__':
	try:
		app.run()
	except KeyboardInterrupt:
		sys.exit(1)