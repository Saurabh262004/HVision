import pygame as pg
import pg_extended as pgx
from UI.Cards.Genshin.CharacterList import CharacterList
import sharedAssets

class DatabaseSystems:
  @staticmethod
  def addGenshinCharacters() -> bool:
    if 'genshinCharacters' in sharedAssets.app.systems:
      return False

    system = pgx.System()

    cList = CharacterList(
      {
        'x': pgx.DynamicValue('classPer', sharedAssets.app, classAttribute='screenWidth', percent=5),
        'y': pgx.DynamicValue('number', 100),
        'width': pgx.DynamicValue('classPer', sharedAssets.app, classAttribute='screenWidth', percent=90),
        'height': pgx.DynamicValue('number', 50)
      }, maxListLength=10, padding=10
    )

    for card in cList.listCards:
      system.addElements(card)

    charInput = pgx.TextInput(
      pgx.Section(
        {
          'x': pgx.DynamicValue('classPer', sharedAssets.app, classAttribute='screenWidth', percent=5),
          'y': pgx.DynamicValue('number', 50),
          'width': pgx.DynamicValue('classPer', sharedAssets.app, classAttribute='screenWidth', percent=90),
          'height': pgx.DynamicValue('number', 30)
        }, pg.Color(250, 250, 250, 64), 7
      ),
      'Arial', pg.Color(250, 250, 250),
      placeholder='Search...',
      placeholderTextColor=pg.Color(128, 128, 128),
      onChangeInfo={
        'callable': cList.displaySearchAll,
        'params': None,
        'sendValue': True
      }
    )

    system.addElement(charInput, 'charInput')

    sharedAssets.app.addSystem(system, 'genshinCharacters')

    sharedAssets.app.setSystemZ('genshinCharacters', 1)

    cList.displaySearchName('')

    return True

  @staticmethod
  def addGenshinWeapons():
    pass

  @staticmethod
  def addZenlessAgents():
    pass

  @staticmethod
  def addZenlessWEngines():
    pass
