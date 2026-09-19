import time
from bs4 import BeautifulSoup
from DBManagers.CustomScrapers.Helpers import getFandomPageHTML, removeImageOptions, parsePassive


def getCharacterData(tr: BeautifulSoup) -> tuple[str, dict]:
	data = {}

	rowData = tr.find_all('td')

	name = rowData[0].find('a').get('title')

	try:
		data['Icon'] = removeImageOptions(rowData[0].find('img').get('data-src'))
	except:
		data['Icon'] = 'Unknown'

	data['Rarity'] = int(rowData[2].find('img').get('alt')[0])

	try:
		elementA = rowData[3].find('a')
		data['Element'] = elementA.get('title')
		data['ElementIcon'] = removeImageOptions(elementA.find('img').get('data-src'))
	except:
		data['Element'] = 'Unknown'
		data['ElementIcon'] = 'Unknown'

	try:
		weaponA = rowData[4].find('a')
		data['WeaponClass'] = weaponA.get('title')
		data['WeaponClassIcon'] = removeImageOptions(weaponA.find('img').get('data-src'))
	except:
		data['WeaponClass'] = 'Unknown'
		data['WeaponClassIcon'] = 'Unknown'

	try:
		regionA = rowData[5].find('a')
		data['Region'] = regionA.get('title')
		data['RegionIcon'] = removeImageOptions(regionA.find('img').get('data-src'))
	except:
		data['Region'] = 'Unknown'
		data['RegionIcon'] = 'Unknown'

	data['Model'] = rowData[6].find('a').get_text()

	data['ReleaseDate'] = rowData[7].get('data-release')
	data['ReleaseVersion'] = rowData[8].get('data-version')

	return (name, data)

def getWeaponData(tr: BeautifulSoup) -> tuple[str, dict]:
	data = {}

	rowData = tr.find_all('td')

	name = rowData[0].find('a').get('title')

	try:
		data['Icon'] = removeImageOptions(rowData[0].find('img').get('data-src'))
	except:
		data['Icon'] = 'Unknown'

	data['Rarity'] = int(rowData[2].find('img').get('alt')[0])
	data['BaseATK'] = rowData[3].get_text()
	data['2ndStat'] = rowData[4].get_text()
	data['Passive'] = parsePassive(rowData[5])

	return name, data

def getData() -> tuple[dict, int, int, int]:
	fetchStart = time.time()
	characterHTML = getFandomPageHTML('genshin-impact', 'Character/List')
	time.sleep(2)
	weaponHTML = getFandomPageHTML('genshin-impact', 'Weapon/List/By_Weapon_Type')
	fetchTime = int((time.time() - fetchStart) * 1000) - 2000

	processStart = time.time()

	characterRows = BeautifulSoup(characterHTML, 'html.parser').find('tbody').find_all('tr')
	characterRows.pop(0)

	characters = {}
	for row in characterRows:
		name, cData = getCharacterData(row)
		characters[name] = cData

	weaponTables = BeautifulSoup(weaponHTML, 'html.parser').find_all('tbody')
	WEAPON_CLASSES = ('Sword', 'Claymore', 'Polearm', 'Catalyst', 'Bow')

	weapons = {}
	for i in range(5):
		weaponRows = weaponTables[i].find_all('tr')
		weaponRows.pop(0)

		for row in weaponRows:
			name, wData = getWeaponData(row)
			wData['WeaponClass'] = WEAPON_CLASSES[i]
			weapons[name] = wData

	processTime = int((time.time() - processStart) * 1000)

	data = {
		'Items': {
			'Characters': characters,
			'Weapons': weapons
		}
	}

	return data, fetchTime, processTime, 2000
