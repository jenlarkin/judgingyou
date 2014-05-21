import csv

def getAvailableDecks(CSVPath):
	""" creates decks dict from metadata in decks/decks.csv """
	result = {}

	rawFile = open(CSVPath + 'decks.csv', 'rb')
	fileContents = csv.DictReader(rawFile, delimiter=',')

	for line in fileContents:
		result[line['deck_code']] = {}
		result[line['deck_code']]['name'] = line['deck_name']
		result[line['deck_code']]['description'] = line['description']
		result[line['deck_code']]['watermark'] = line['watermark']
		if line['is_active'] == 't':
			result[line['deck_code']]['isActive'] = True
		else:
			result[line['deck_code']]['isActive'] = False

		if line['is_base_deck'] == 't':
			result[line['deck_code']]['isBaseDeck'] = True
		else:
			result[line['deck_code']]['isBaseDeck'] = False

		if line['is_custom_deck'] == 't':
			result[line['deck_code']]['isCustomDeck'] = True
		else:
			result[line['deck_code']]['isCustomDeck'] = False

		result[line['deck_code']]['numPrompts'] = 0
		result[line['deck_code']]['numAnswers'] = 0
		result[line['deck_code']]['prompts'] = {}
		result[line['deck_code']]['answers'] = {}
		result[line['deck_code']]['promptsCSV'] = CSVPath + line['deck_code'] + '-prompts.csv'
		result[line['deck_code']]['answersCSV'] = CSVPath + line['deck_code'] + '-answers.csv'
	rawFile.close()

	return result

def loadActiveDecks(decks, CSVPath):
	""" attempts to load active prompt and answer decks from CSVs, marks deck inactive on failure """
	# ensure that the availableDecks have been loaded
	if len(decks) < 1:
		decks = getAvailableDecks(CSVPath)

	for deck in decks:
		if decks[deck]['isActive']:
			try:
				loadDeckFromFile(decks[deck])
			except:
				decks[deck]['isActive'] = False

	return decks

def setPrompts(prompts):
	""" adds prompt cards from CSV to the deck """
	# if database functions are added, need to split at line outside of function instead of looping on line
	result = {}
	i = 0

	for line in prompts:
		result[i] = {}
		result[i]['cardText'] = line['card_text']
		result[i]['numberToPlay'] = int(line['number_to_play'])
		result[i]['drawBefore'] = int(line['draw_before'])
		i = i + 1
	
	return result

def setAnswers(answers):
	""" adds answer cards from CSV to the deck """
	# if database functions are added, need to split at line outside of function instead of looping on line
	result = {}
	i = 0

	for line in answers:
		result[i] = {}
		result[i]['cardText'] = line['card_text']
		i = i + 1
	
	return result

def loadPrompts(csvFilePath):
	""" opens prompts csv file and returns prompts deck"""
	with open(csvFilePath, 'rb') as fileContents:
		results = csv.DictReader(fileContents, delimiter=',')
		results = setPrompts(results)
	return results

def loadAnswers(csvFilePath):
	""" opens answers csv file and returns answers deck"""
	with open(csvFilePath, 'rb') as fileContents:
		results = csv.DictReader(fileContents, delimiter=',')
		results = setAnswers(results)
	return results

def loadDeckFromFile(deck):
	""" sets up deck from file. Used to add decks, reload decks	"""

	deck['prompts'] = {}
	deck['prompts'] = loadPrompts(deck['promptsCSV'])	
	deck['numPrompts'] = len(deck['prompts'])

	deck['answers'] = {}
	deck['answers'] = loadAnswers(deck['answersCSV'])
	deck['numAnswers'] = len(deck['answers'])

	return deck

def filterDecks(availableDecks,filterType,filterList):
	result = {}

	for deck in availableDecks:
		if filterType == 'active':
			if availableDecks[deck]['isActive']:
				result[deck] = availableDecks[deck]
		elif filterType == 'included' and filterList != '':
			if deck in filterList:
				if availableDecks[deck]['isActive']:
					result[deck] = availableDecks[deck]
				else:
					raise Exception('selected deck is not currently available: ' + deck)

	return result