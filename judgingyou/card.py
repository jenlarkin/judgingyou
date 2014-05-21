

def getCard(availableDecks,cardID,cardType):
	card = cardID.split('-')
	result = {}
	result['cardID'] = cardID
	result['deckName'] = availableDecks[card[0]]['name']
	result['watermark'] = availableDecks[card[0]]['watermark']
	result['isCustomDeck'] = availableDecks[card[0]]['isCustomDeck']
	if cardType == 'answers':
		result['cardText'] = availableDecks[card[0]]['answers'][int(card[1])]['cardText']
	elif cardType == 'prompts':
		result['cardText'] = replaceBlanksWithUnderscores(availableDecks[card[0]]['prompts'][int(card[1])]['cardText'])

	return result

def replaceBlanksWithUnderscores(cardText):
	""" replace text [blank] with ____ """
	return cardText.replace('[blank]', '____')