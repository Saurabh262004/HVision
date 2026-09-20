def createImageCollectorManifest(db: dict) -> dict:
	imageCollectorManifest = {}

	# genshin characters
	for character, data in db['GenshinImpact']['Items']['Characters'].items():
		if not data['Icon'] == 'Unknown':
			imageCollectorManifest[f'Genshin_Character_{character}'] = data.pop('Icon')

		if not data['ElementIcon'] == 'Unknown':
			imageCollectorManifest[f'Genshin_Element_{data['Element']}'] = data.pop('ElementIcon')

		if not data['WeaponClassIcon'] == 'Unknown':
			imageCollectorManifest[f'Genshin_Weapon_Class_{data['WeaponClass']}'] = data.pop('WeaponClassIcon')

		if not data['RegionIcon'] == 'Unknown':
			imageCollectorManifest[f'Genshin_Region_{data['Region']}'] = data.pop('RegionIcon')

	# genshin weapons
	for weapon, data in db['GenshinImpact']['Items']['Weapons'].items():
		if not data['Icon'] == 'Unknown':
			imageCollectorManifest[f'Genshin_Weapon_{weapon}'] = data.pop('Icon')

	# zzz agents
	for agent, data in db['ZenlessZoneZero']['Items']['Agents'].items():
		if not data['Icon'] == 'Unknown':
			imageCollectorManifest[f'Zenless_Agent_{agent}'] = data.pop('Icon')

		if not data['Rank'] == 'Unknown':
			imageCollectorManifest[f'Zenless_Agent_Rank_{data['Rank']}'] = data.pop('RankIcon')
		
		if not data['Attribute'] == 'Unknown':
			imageCollectorManifest[f'Zenless_Attribute_{data['Attribute']}'] = data.pop('AttributeIcon')

		if not data['Speciality'] == 'Unknown':
			imageCollectorManifest[f'Zenless_Speciality_{data['Speciality']}'] = data.pop('SpecialityIcon')

		for i in range(len(data['AttackType'])):
			atkType = data['AttackType'][i]
			atkTypeIcon = data['AttackTypeIcons'][i]

			if not atkType == 'Unknown':
				imageCollectorManifest[f'Zenless_Attack_Type_{atkType}'] = atkTypeIcon

		data.pop('AttackTypeIcons')

		if not data['Faction'] == 'Unknown':
			imageCollectorManifest[f'Zenless_Faction_{data['Faction']}'] = data.pop('FactionIcon')

	# zzz wengines
	for wengine, data in db['ZenlessZoneZero']['Items']['WEngines'].items():
		if not data['Icon'] == 'Unknown':
			imageCollectorManifest[f'Zenless_WEngine_{wengine}'] = data.pop('Icon')

		if not data['Rank'] == 'Unknown':
			imageCollectorManifest[f'Zenless_WEngine_Rank_{data['Rank']}'] = data.pop('RankIcon')

	db['ImageCollectorManifest'] = imageCollectorManifest

	return db

def processDB(db: dict) -> dict:
	return createImageCollectorManifest(db)
