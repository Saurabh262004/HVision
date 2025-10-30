import os
import pygame as pg
import pg_extended as pgx
import sharedAssets

def generate(characterName: str, cardDim: dict[str, pgx.DynamicValue], cardType: str, selectionCallback: callable = None) -> dict[str, pgx.UIElement]:
  if cardType == 'list':
    return listCard(characterName, cardDim, selectionCallback)

  return None

def getIcon(path: str) -> pg.Surface | pg.Color:
  try:
    icon = pg.image.load(path).convert_alpha()
  except:
    icon = pg.Surface((64, 64), pg.SRCALPHA)
    icon.fill((255, 0, 64, 128))

  return icon

def listCard(characterName: str, cardDim: dict[str, pgx.DynamicValue], selectionCallback: callable = None) -> dict[str, pgx.UIElement]:
  card = {}

  characterDetails = sharedAssets.db['GenshinImpact']['Items']['Characters'][characterName]

  characterRarity = int(characterDetails['Rarity'][0])

  cardButton = pgx.Button(
    pgx.Section(cardDim, pg.Color(143, 50, 148), 5),
    onClick=selectionCallback,
    onClickActuation='buttonUp'
  )

  imageDBPath = sharedAssets.config['imageDBLocation']

  characterIcon = getIcon(
    os.path.join(
      imageDBPath,
      f'GenshinCharacters_{characterName}'
    )
  )

  rarityIcon = getIcon(
    os.path.join(
      imageDBPath,
      'Genshin_RarityStar'
    )
  )

  elementIcon = getIcon(
    os.path.join(
      imageDBPath,
      f'Genshin_Element_{characterDetails['Element']}'
    )
  )

  weaponTypeIcon = getIcon(
    os.path.join(
      imageDBPath,
      f'Genshin_WeaponClass_{characterDetails['WeaponType']}'
    )
  )

  iconSection = pgx.Section(
    {
      'x': cardDim['x'],
      'y': cardDim['y'],
      'width': cardDim['height'],
      'height': cardDim['height']
    }, characterIcon
  )

  nameSection = pgx.Section(
    {
      'x': pgx.DynamicValue('callable', lambda: cardButton.section.x + iconSection.width),
      'y': cardDim['y'],
      'width': pgx.DynamicValue('callable', lambda: cardButton.section.width - iconSection.width),
      'height': cardDim['height']
    }, pg.Color(255, 255, 255, 64)
  )

  nameTextBox = pgx.TextBox(
    nameSection,
    characterName,
    'Arial',
    pg.Color(250, 255, 255),
    pgx.DynamicValue('callable', lambda: nameSection.height * .4)
  )

  nameTextBox.alignTextHorizontal = 'left'
  nameTextBox.paddingLeft = 2

  nameTextBox.update()

  rarityIconWidth, rarityIconHeight = rarityIcon.get_size()

  raritySurface = pg.Surface(
    (characterRarity * rarityIconWidth, rarityIconHeight),
    pg.SRCALPHA
  )

  for i in range(characterRarity):
    raritySurface.blit(rarityIcon, (i * rarityIconWidth, 0))

  elementSection = pgx.Section(
    {
      'x': pgx.DynamicValue('callable', lambda: cardButton.section.x + (cardButton.section.width - cardButton.section.height)),
      'y': cardDim['y'],
      'width': cardDim['height'],
      'height': cardDim['height']
    }, elementIcon, backgroundSizePercent=55
  )

  weaponTypeSection = pgx.Section(
    {
      'x': pgx.DynamicValue('callable', lambda: cardButton.section.x + (cardButton.section.width - (cardButton.section.height * 2))),
      'y': cardDim['y'],
      'width': cardDim['height'],
      'height': cardDim['height']
    }, weaponTypeIcon, backgroundSizePercent=55
  )

  rarityWidth = pgx.DynamicValue('callable', lambda: cardButton.section.height * 0.4 * characterRarity)

  raritySection = pgx.Section(
    {
      'x': pgx.DynamicValue('callable', lambda: cardButton.section.x + cardButton.section.width - rarityWidth.value - (cardButton.section.height * 2)),
      'y': cardDim['y'],
      'width': rarityWidth,
      'height': cardDim['height']
    }, raritySurface
  )

  card[f'{characterName}_listCard_cardSection'] = cardButton
  card[f'{characterName}_listCard_iconSection'] = iconSection
  card[f'{characterName}_listCard_nameTextBox'] = nameTextBox
  card[f'{characterName}_listCard_elementSection'] = elementSection
  card[f'{characterName}_listCard_weaponTypeSection'] = weaponTypeSection
  card[f'{characterName}_listCard_raritySection'] = raritySection

  return card
