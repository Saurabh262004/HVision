import pygame as pg
import pg_extended as pgx
from UI.Cards.Genshin.CharacterList import CharacterList
import sharedAssets

def addSystem() -> bool:
  window: pgx.Window = sharedAssets.app

  if 'GCDBList' in window.systems:
    return False

  system = pgx.System(preLoadState=True)

  cList = CharacterList(
    {
      'x': pgx.DynamicValue(window, 'screenWidth', percent=5),
      'y': pgx.DynamicValue(100),
      'width': pgx.DynamicValue(window, 'screenWidth', percent=60),
      'height': pgx.DynamicValue(50)
    }, maxListLength=10, padding=10
  )

  for card in cList.listCards:
    system.addElements(card)

  listScroller = None

  def updateCListAfterSearch(value: str):
    nonlocal listScroller, cList

    cList.updateListPosition(0)

    listScroller.value = 0

    cList.displaySearchAll(value)

    listScroller.valueRange = (0, len(cList.activeList) - 1)

  charInput = pgx.TextInput(
    pgx.Section(
      {
        'x': pgx.DynamicValue(window, 'screenWidth', percent=5),
        'y': pgx.DynamicValue(50),
        'width': pgx.DynamicValue(window, 'screenWidth', percent=60),
        'height': pgx.DynamicValue(30)
      }, pg.Color(250, 250, 250, 64), 7
    ),
    'Arial', pg.Color(250, 250, 250),
    placeholder='Search...',
    placeholderTextColor=pg.Color(128, 128, 128),
    callback=pgx.Callback(
      ('None',),
      updateCListAfterSearch,
      extraArgKeys={'value': 'value'}
    )
  )

  listScroller = pgx.Slider(
    'vertical',
    pgx.Section(
      {
        'x': pgx.DynamicValue(window, 'screenWidth', percent=99),
        'y': pgx.DynamicValue(0),
        'width': pgx.DynamicValue(window, 'screenWidth', percent=1),
        'height': pgx.DynamicValue(window, 'screenHeight')
      }, pg.Color(0, 0, 0, 0)
    ),
    pgx.Section(
      {
        'x': pgx.DynamicValue(0),
        'y': pgx.DynamicValue(0),
        'width': pgx.DynamicValue(window, 'screenWidth', percent=1),
        'height': pgx.DynamicValue(window, 'screenHeight', percent=4)
      }, pg.Color(255, 255, 255, 128)
    ), (0, len(cList.characters) - 1), -2, pg.Color(0, 0, 0, 0),
    pgx.CallbackSet((
      pgx.Callback(
        ('scroll', 'mouseDrag', 'mouseDown', 'mouseUp'),
        cList.updateListPosition,
        extraArgKeys={'value': 'listPosition'}
      ),
    )), False
  )

  listScroller.lazyUpdate = False

  system.addElement(charInput, 'charInput')

  system.addElement(listScroller, 'listScroller')

  window.addSystem(system, 'GCDBList')

  window.setSystemZ('GCDBList', 1)

  cList.displaySearchName('')

  return True
