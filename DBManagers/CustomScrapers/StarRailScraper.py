import time
from collections import Counter
from bs4 import BeautifulSoup
from DBManagers.CustomScrapers.Helpers import getFandomPageHTML, removeImageOptions, getTitleIconPair

def getCharacterData(tr: BeautifulSoup) -> tuple[str, dict]:
	data = {}
	rowData = tr.find_all('td')

	name = rowData[0].find('a').get('title')

	try:
		data['Icon'] = removeImageOptions(rowData[0].find('img').get('data-src'))
	except:
		data['Icon'] = 'Unknown'

	data['Rarity'] = int(rowData[1].find('img').get('alt')[0])
	data['Path'], data['PathIcon'] = getTitleIconPair(rowData[2])
	data['CombatType'], data['CombatTypeIcon'] = getTitleIconPair(rowData[3])
	data['ReleaseVersion'] = rowData[4].get_text(strip=True)

	return name, data

def getData():
	fetchStart = time.time()
	charactersHTML = getFandomPageHTML('honkai-star-rail', 'Character/List')
	fetchTime = int((time.time() - fetchStart) * 1000)

	processStart = time.time()

	characterRows = BeautifulSoup(charactersHTML, 'html.parser').find('tbody').find_all('tr')[1:]
	namesList = []
	cDataList = []
	for row in characterRows:
		name, cData = getCharacterData(row)
		namesList.append(name)
		cDataList.append(cData)

	characters = {}
	namesCounter = Counter(namesList)
	currentCounts = Counter()

	for name, cData in zip(namesList, cDataList):
		if namesCounter[name] > 1:
			currentCounts[name] += 1
			key = f"{name}_{currentCounts[name]}"
		else:
			key = name

		characters[key] = cData

	processTime = time.time() - processStart

	data = {
		'Items': {
			'Characters': characters
		}
	}

	return data, fetchTime, processTime, 0
