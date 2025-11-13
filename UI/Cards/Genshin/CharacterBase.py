import pygame as pg
import pg_extended as pgx

class CharacterBase:
  @staticmethod
  def getCardBase(cardDim, prefix: str = '') -> dict[str, pgx.UIElement]:
    cardBase = {}

    cardButton = pgx.Button(
      pgx.Section(
        cardDim,
        pg.Color(255, 255, 255, 64),
        7,
        'squish',
        'center_right'
      ),
      onClickActuation='buttonUp'
    )

    iconSection = pgx.Section(
      {
        'x': cardDim['x'],
        'y': cardDim['y'],
        'width': cardDim['height'],
        'height': cardDim['height']
      }, pg.Color(255, 255, 255, 64)
    )

    nameSection = pgx.Section(
      {
        'x': pgx.DynamicValue(lambda: cardButton.section.x + iconSection.width),
        'y': cardDim['y'],
        'width': pgx.DynamicValue(lambda: cardButton.section.width - iconSection.width),
        'height': cardDim['height']
      }, pg.Color(255, 255, 255, 64)
    )

    nameTextBox = pgx.TextBox(
      nameSection,
      'characterName',
      'Arial',
      pg.Color(250, 255, 255),
      pgx.DynamicValue(lambda: nameSection.height * .4)
    )

    nameTextBox.alignTextHorizontal = 'left'
    nameTextBox.paddingLeft = 2

    nameTextBox.update()

    raritySection = pgx.Section(
      {
        'x': pgx.DynamicValue(lambda: cardButton.section.x + (cardButton.section.width - (cardButton.section.height * 5))),
        'y': cardDim['y'],
        'width': pgx.DynamicValue(lambda: cardButton.section.height * 2),
        'height': cardDim['height']
      }, pg.Color(255, 255, 255, 64), backgroundPosition='center_right'
    )

    weaponTypeSection = pgx.Section(
      {
        'x': pgx.DynamicValue(lambda: cardButton.section.x + (cardButton.section.width - (cardButton.section.height * 3))),
        'y': cardDim['y'],
        'width': cardDim['height'],
        'height': cardDim['height']
      }, pg.Color(255, 255, 255, 64), backgroundSizePercent=65
    )

    nationSection = pgx.Section(
      {
        'x': pgx.DynamicValue(lambda: cardButton.section.x + (cardButton.section.width - (cardButton.section.height * 2))),
        'y': cardDim['y'],
        'width': cardDim['height'],
        'height': cardDim['height']
      }, pg.Color(255, 255, 255, 64), backgroundSizePercent=75
    )

    elementSection = pgx.Section(
      {
        'x': pgx.DynamicValue(lambda: cardButton.section.x + (cardButton.section.width - cardButton.section.height)),
        'y': cardDim['y'],
        'width': cardDim['height'],
        'height': cardDim['height']
      }, pg.Color(255, 255, 255, 64), backgroundSizePercent=55
    )

    cardBase[f'{prefix}cardSection'] = cardButton
    cardBase[f'{prefix}iconSection'] = iconSection
    cardBase[f'{prefix}nameTextBox'] = nameTextBox
    cardBase[f'{prefix}elementSection'] = elementSection
    cardBase[f'{prefix}weaponTypeSection'] = weaponTypeSection
    cardBase[f'{prefix}nationSection'] = nationSection
    cardBase[f'{prefix}raritySection'] = raritySection

    return cardBase
