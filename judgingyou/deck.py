import csv

def getAvailableDecks(CSVPath):
	""" creates decks dict from metadata in decks/decks.csv """
	result = {}

	# TODO: should be with open like the load prompts code, try consolidate with other functions
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
			# TODO: add exception for if both decks are empty. empty prompts or answers is ok, but not both

	return decks

def loadDeckFromFile(deck):
	""" sets up deck from file. Used to add decks, reload decks	"""
	# TODO: could be a single function used twice. May not be worth refactoring
	isMissingDecks = 0
	try:
		deck['prompts'] = {}
		deck['prompts'] = loadDeckCards(deck['promptsCSV'],'prompts')	
		deck['numPrompts'] = len(deck['prompts'])
	except:
		isMissingDecks = 1

	try:
		deck['answers'] = {}
		deck['answers'] = loadDeckCards(deck['answersCSV'], 'answers')
		deck['numAnswers'] = len(deck['answers'])
	except:
		isMissingDecks = isMissingDecks + 1

	if isMissingDecks > 1:
		raise Exception('Deck set as active has no cards.')

	return deck

def loadDeckCards(csvFilePath,deckType):
	with open(csvFilePath, 'rb') as fileContents:
		results = csv.DictReader(fileContents, delimiter=',')
		if deckType == 'prompts':
			results = setPrompts(results)
		elif deckType == 'answers':
			results = setAnswers(results)
		else:
			raise Exception('invalid deckType sent to loadDeckCards. Value was: ' + deckType)
	return results

def setPrompts(prompts):
	""" adds prompt cards from CSV to the deck """
	# if database functions are added, need to split at line outside of function instead of looping on line
	# TODO: consolidate with setAnswers, evaluate if setting up file metadata would allow decks to be consolidated too
	result = {}
	i = 0

	for line in prompts:
		result[i] = {}
		# TODO: add in watermark and iscustom
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
		# TODO: add in watermark and iscustom
		result[i]['cardText'] = line['card_text']
		i = i + 1
	
	return result	

def filterDecks(availableDecks,filterType,filterList):
	result = {}

	for deck in availableDecks:
		# TODO: add code to validate filter criteria, deck not found
		if filterType == 'active':
			if availableDecks[deck]['isActive']:
				result[deck] = availableDecks[deck]
		elif filterType == 'included' and filterList != '':
			# TODO: add exception if filterList is empty
			if deck in filterList:
				if availableDecks[deck]['isActive']:
					result[deck] = availableDecks[deck]
				else:
					raise Exception('selected deck is not currently available: ' + deck)

	return result