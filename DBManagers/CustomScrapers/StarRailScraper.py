import time
from collections import Counter
from bs4 import BeautifulSoup
from DBManagers.CustomScrapers.Helpers import getFandomPageHTML, removeImageOptions, getTitleIconPair

def getCharacterData(tr: BeautifulSoup) -> list[str, dict]:
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

def getLightConeStats(td: BeautifulSoup) -> dict:
	stats = {}

	for b in td.find_all("b"):
		stat = b.get_text(strip=True).rstrip(":")
		value = b.next_sibling.strip()

		value = value.replace(",", "")

		min_value, max_value = map(int, value.split("~"))

		stats[stat] = {
			"min": min_value,
			"max": max_value
		}

	return stats

def getLightConePassive(td: BeautifulSoup) -> dict:
	title = td.find("b").get_text(strip=True)

	td.find("b").extract()
	td.find("br").extract()

	return {
		"title": title,
		"description": td.get_text(" ", strip=True)
	}

def getLightConeFeaturedCharacters(td: BeautifulSoup) -> list[str]:
	return [
		li.get_text(strip=True)
		for li in td.find_all("li")
	]

def getLightConeData(tr: BeautifulSoup) -> list[str, dict]:
	data = {}
	rowData = tr.find_all('td')

	name = rowData[0].find('a').get('title')

	try:
		data['Icon'] = removeImageOptions(rowData[0].find('img').get('data-src'))
	except:
		data['Icon'] = 'Unknown'

	data['Rarity'] = int(rowData[1].find('img').get('alt')[0])
	data['Path'] = rowData[2].find('a').get('title')
	data['Stats'] = getLightConeStats(rowData[3])
	data['Passive'] = getLightConePassive(rowData[4])
	data['FeaturedCharacters'] = getLightConeFeaturedCharacters(rowData[5])

	return name, data

def getData():
	fetchStart = time.time()
	charactersHTML = getFandomPageHTML('honkai-star-rail', 'Character/List')
	time.sleep(2)
	lightConeHTML = getFandomPageHTML('honkai-star-rail', 'Light_Cone/List')
	fetchTime = int((time.time() - fetchStart) * 1000) - 2000

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

	lightConeRows = BeautifulSoup(lightConeHTML, 'html.parser').find('tbody').find_all('tr')[1:]
	lightCones = {}
	for row in lightConeRows:
		try:
			name, lData = getLightConeData(row)
			lightCones[name] = lData
		except:
			print('error parsing a light cone row')

	processTime = int((time.time() - processStart) * 1000)

	data = {
		'Items': {
			'Characters': characters,
			'LightCones': lightCones
		}
	}

	return data, fetchTime, processTime, 2000
