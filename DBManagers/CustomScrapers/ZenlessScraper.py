import time
from bs4 import BeautifulSoup
from DBManagers.CustomScrapers.Helpers import getFandomPageHTML, removeImageOptions, parsePassive, getTitleIconPair, getStatLines

def getAgentData(tr: BeautifulSoup) -> tuple[str, dict]:
	data = {}
	rowData = tr.find_all('td')

	name = rowData[1].find('a').get_text(strip=True)

	try:
		data['Icon'] = removeImageOptions(rowData[0].find('img').get('data-src'))
	except:
		data['Icon'] = 'Unknown'

	try:
		rankSpan = rowData[2].find('span', class_='zzw-icon')
		data['Rank'] = rankSpan.get('title').split(' ')[-1]
		data['RankIcon'] = removeImageOptions(rowData[2].find('img').get('data-src'))
	except:
		data['Rank'] = 'N/A'
		data['RankIcon'] = 'Unknown'

	data['Attribute'], data['AttributeIcon'] = getTitleIconPair(rowData[3])
	data['Speciality'], data['SpecialityIcon'] = getTitleIconPair(rowData[4])

	attackTypeSpans = rowData[5].find_all('span', recursive=False)
	attackTypePairs = [getTitleIconPair(span) for span in attackTypeSpans]
	data['AttackType'] = [pair[0] for pair in attackTypePairs]
	data['AttackTypeIcons'] = [pair[1] for pair in attackTypePairs]

	data['Faction'], data['FactionIcon'] = getTitleIconPair(rowData[6])

	versionLink = rowData[7].find('a')
	data['ReleaseVersion'] = versionLink.get_text(strip=True).replace('Version ', '') if versionLink else 'Unreleased'

	return name, data

def getWEngineData(tr: BeautifulSoup) -> tuple[str, dict]:
	data = {}
	rowData = tr.find_all('td')

	name = rowData[1].find('a').get_text(strip=True)

	try:
		data['Icon'] = removeImageOptions(rowData[0].find('img').get('data-src'))
	except:
		data['Icon'] = 'Unknown'

	try:
		rankSpan = rowData[2].find('span', class_='zzw-icon')
		data['Rank'] = rankSpan.get('title').split(' ')[-1]
		data['RankIcon'] = removeImageOptions(rowData[2].find('img').get('data-src'))
	except:
		data['Rank'] = 'N/A'
		data['RankIcon'] = 'Unknown'

	data['Speciality'] = rowData[3].find('a').get('title')

	attributeSpans = rowData[4].find_all('span', recursive=False)
	data['Attributes'] = [span.find('a').get('title') for span in attributeSpans]

	try:
		data['Exclusive'] = rowData[5].find('a').get('title')
	except:
		data['Exclusive'] = 'N/A'

	baseStat = getStatLines(rowData[6])
	data['BaseStatName'] = baseStat[0] if baseStat else 'N/A'
	data['BaseStatValue'] = baseStat[1] if len(baseStat) > 1 else 'N/A'

	advStat = getStatLines(rowData[7])
	data['AdvancedStatName'] = advStat[0].rstrip(':') if advStat else 'N/A'
	data['AdvancedStatValue'] = advStat[1] if len(advStat) > 1 else 'N/A'

	data['Passive'] = parsePassive(rowData[8])

	try:
		data['Version'] = rowData[9].find('a').get_text(strip=True)
	except:
		data['Version'] = 'N/A'

	return name, data

def getData() -> tuple[dict, int, int, int]:
	fetchStart = time.time()
	agentsHTML = getFandomPageHTML('zenless-zone-zero', 'Agent/List')
	time.sleep(2)
	wEngineHTML = getFandomPageHTML('zenless-zone-zero', 'W-Engine/List')

	fetchTime = int((time.time() - fetchStart) * 1000) - 2000

	processStart = time.time()

	agentTables = BeautifulSoup(agentsHTML, 'html.parser').find_all('table', class_='article-table')
	agents = {}
	for table in agentTables:
		rows = table.find('tbody').find_all('tr')[1:]
		for row in rows:
			name, aData = getAgentData(row)
			agents[name] = aData

	wEngineRows = BeautifulSoup(wEngineHTML, 'html.parser').find('tbody').find_all('tr')[1:]
	wEngines = {}
	for row in wEngineRows:
		name, wData = getWEngineData(row)
		wEngines[name] = wData

	processTime = int((time.time() - processStart) * 1000)

	data = {
		'Items': {
			'Agents': agents,
			'WEngines': wEngines
		}
	}

	return data, fetchTime, processTime, 2000
