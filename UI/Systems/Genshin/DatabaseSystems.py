import pygame as pg
import pg_extended as pgx
from UI.Cards.Genshin.CharacterList import CharacterList
import sharedAssets

class GenshinDBSystems:
  @staticmethod
  def addGenshinCharacters() -> bool:
    if 'genshinCharacters' in sharedAssets.app.systems:
      return False

    system = pgx.System()

    cList = CharacterList(
      {
        'x': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=5),
        'y': pgx.DynamicValue(100),
        'width': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=90),
        'height': pgx.DynamicValue(50)
      }, maxListLength=10, padding=10
    )

    for card in cList.listCards:
      system.addElements(card)

    listScroller = None

    def updateCListAfterSearch(searchVal: str):
      nonlocal listScroller, cList

      cList.updateListPosition(0)

      listScroller.value = 0

      cList.displaySearchAll(searchVal)

      listScroller.valueRange = (0, len(cList.activeList) - 1)

    charInput = pgx.TextInput(
      pgx.Section(
        {
          'x': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=5),
          'y': pgx.DynamicValue(50),
          'width': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=90),
          'height': pgx.DynamicValue(30)
        }, pg.Color(250, 250, 250, 64), 7
      ),
      'Arial', pg.Color(250, 250, 250),
      placeholder='Search...',
      placeholderTextColor=pg.Color(128, 128, 128),
      onChangeInfo={
        'callable': updateCListAfterSearch,
        'params': None,
        'sendValue': True
      }
    )

    listScroller = pgx.Slider(
      'vertical',
      pgx.Section(
        {
          'x': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=99),
          'y': pgx.DynamicValue(0),
          'width': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=1),
          'height': pgx.DynamicValue(sharedAssets.app, 'screenHeight')
        }, pg.Color(0, 0, 0, 0)
      ),
      pgx.Section(
        {
          'x': pgx.DynamicValue(0),
          'y': pgx.DynamicValue(0),
          'width': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=1),
          'height': pgx.DynamicValue(sharedAssets.app, 'screenHeight', percent=4)
        }, pg.Color(255, 255, 255, 128)
      ), (0, len(cList.characters) - 1), -2, pg.Color(0, 0, 0, 0),
      {
        'callable': cList.updateListPosition,
        'params': None,
        'sendValue': True
      }, False
    )

    listScroller.lazyUpdate = False

    system.addElement(charInput, 'charInput')

    system.addElement(listScroller, 'listScroller')

    sharedAssets.app.addSystem(system, 'genshinCharacters')

    sharedAssets.app.setSystemZ('genshinCharacters', 1)

    cList.displaySearchName('')

    return True

  @staticmethod
  def addGenshinWeapons():
    pass
