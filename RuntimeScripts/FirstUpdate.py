from multiprocessing import Process
import pygame as pg
import pg_extended as pgx
from RuntimeScripts.DBScripts.DBProtocols import DBProtocols
import sharedAssets

def addCList():
  from UI.Cards.Genshin.CharacterList import CharacterList

  cList = CharacterList(
    {
      'x': pgx.DynamicValue('number', 50),
      'y': pgx.DynamicValue('number', 130),
      'width': pgx.DynamicValue('number', 600),
      'height': pgx.DynamicValue('number', 50)
    }
  )

  for card in cList.listCards:
    sharedAssets.app.systems['home'].addElements(card)

  cList.setActiveCards([0, 1])

  cList.applyCharacterToBase('Furina', 0)
  cList.applyCharacterToBase('Faruzan', 1)

  charInput = pgx.TextInput(
    pgx.Section(
      {
        'x': pgx.DynamicValue('number', 50),
        'y': pgx.DynamicValue('number', 50),
        'width': pgx.DynamicValue('number', 600),
        'height': pgx.DynamicValue('number', 30)
      }, pg.Color(250, 250, 250)
    ), 'Arial', pg.Color(0, 0, 0), placeholder='Character Name',
    onChangeInfo={
      'callable': cList.applyCharacterToBase,
      'params': 0,
      'sendValue': True
    }
  )

  sharedAssets.app.systems['home'].addElement(charInput, 'charInput')

  print('first update finished')

# implement error messages in the future
def firstUpdate() -> bool | None:
  loadDBSuccess = DBProtocols.loadDB()

  # can't proceed if we don't have the DB. User will have to wait till it's generated
  if not loadDBSuccess:
    print('failed to load db, generating a new one...')
    if not DBProtocols.verifyDB():
      return False
  else:
    # if we do have the db, proceed and have a different process varify and update it if needed
    print('varifying db in background')
    DBProtocols.verifyDBBackground()

  addCList()

  return True
