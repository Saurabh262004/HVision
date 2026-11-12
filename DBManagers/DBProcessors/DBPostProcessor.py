def isKnown(icon: dict | None) -> bool:
	return icon is not None and icon.get('url') != 'Unknown'

def collect(manifest: dict, prefix: str, name: str, icon: dict | None) -> None:
	if isKnown(icon):
		manifest[f'{prefix}_{name}'] = icon

def createImageCollectorManifest(db: dict) -> dict:
	manifest = {}

	# Genshin Characters
	for character, data in db['GenshinImpact']['Items']['Characters'].items():
		collect(manifest, 'Genshin_Character', character, data.pop('Icon', None))
		collect(manifest, 'Genshin_Element', data['Element'], data.pop('ElementIcon', None))
		collect(manifest, 'Genshin_Weapon_Class', data['WeaponClass'], data.pop('WeaponClassIcon', None))
		collect(manifest, 'Genshin_Region', data['Region'], data.pop('RegionIcon', None))

	# Genshin Weapons
	for weapon, data in db['GenshinImpact']['Items']['Weapons'].items():
		collect(manifest, 'Genshin_Weapon', weapon, data.pop('Icon', None))

	# ZZZ Agents
	for agent, data in db['ZenlessZoneZero']['Items']['Agents'].items():
		collect(manifest, 'Zenless_Agent', agent, data.pop('Icon', None))
		collect(manifest, 'Zenless_Agent_Rank', data['Rank'], data.pop('RankIcon', None))
		collect(manifest, 'Zenless_Attribute', data['Attribute'], data.pop('AttributeIcon', None))
		collect(manifest, 'Zenless_Speciality', data['Speciality'], data.pop('SpecialityIcon', None))
		collect(manifest, 'Zenless_Faction', data['Faction'], data.pop('FactionIcon', None))

		for atkType, icon in zip(data['AttackType'], data.pop('AttackTypeIcons')):
			collect(manifest, 'Zenless_Attack_Type', atkType, icon)

	# ZZZ WEngines
	for wengine, data in db['ZenlessZoneZero']['Items']['WEngines'].items():
		collect(manifest, 'Zenless_WEngine', wengine, data.pop('Icon', None))
		collect(manifest, 'Zenless_WEngine_Rank', data['Rank'], data.pop('RankIcon', None))

	# HSR Characters
	for character, data in db['HonkaiStarRail']['Items']['Characters'].items():
		collect(manifest, 'StarRail_Character', character, data.pop('Icon', None))
		collect(manifest, 'StarRail_Path', data['Path'], data.pop('PathIcon', None))
		collect(manifest, 'StarRail_CombatType', data['CombatType'], data.pop('CombatTypeIcon', None))

	# HSR Light Cones
	for lightCone, data in db['HonkaiStarRail']['Items']['LightCones'].items():
		collect(manifest, 'StarRail_LightCone', lightCone, data.pop('Icon', None))

	db['ImageCollectorManifest'] = manifest
	return db

def createCacheBusterDict(db: dict) -> dict:
	manifest = db['ImageCollectorManifest']
	cacheBusters = {}

	for key, icon in list(manifest.items()):
		cacheBusters[key] = icon['cb']
		manifest[key] = icon['url']

	db['CacheBusters'] = cacheBusters
	return db

def processDB(db: dict) -> dict:
	db = createImageCollectorManifest(db)
	return createCacheBusterDict(db)
