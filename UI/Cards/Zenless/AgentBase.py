import pygame as pg
import pg_extended as pgx

class CharacterBase:
  @staticmethod
  def getCardBase(cardDim, prefix: str = '') -> dict[str, pgx.UIElement]:
    cardBase = {}

    cardButton = pgx.Button(
      pgx.TextBox(
        pgx.Section(
          cardDim,
          pg.Color(255, 255, 255, 64),
          7,
          'squish',
          'center_right'
        ), '', 'arial', pg.Color(0, 0, 0)
      )
    )

    iconSection = pgx.Section(
      {
        'x': pgx.DynamicValue(lambda: cardDim['x'].value + (cardDim['width'].value / 100)),
        'y': cardDim['y'],
        'width': cardDim['height'],
        'height': cardDim['height']
      }, pg.Color(255, 255, 255, 64)
    )

    nameSection = pgx.Section(
      {
        'x': pgx.DynamicValue(lambda: iconSection.x + iconSection.width),
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
