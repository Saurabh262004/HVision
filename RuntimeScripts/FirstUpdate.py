from multiprocessing import Process
import pg_extended as pgx
from UI import Cards
from RuntimeScripts.DBProtocols import DBProtocols
import sharedAssets

# implement error messages in the future
def firstUpdate() -> bool | None:
  configSuccess = DBProtocols.loadConfig()

  if not configSuccess:
    print('failed to load config')
    return False

  dbStructure = DBProtocols.loadDBStructure()

  if dbStructure is None:
    print('failed to load db structure')
    return False

  loadDBSuccess = DBProtocols.loadDB(dbStructure['location'])

  # can't proceed if we don't have the DB. User will have to wait till it's generated
  if not loadDBSuccess:
    print('failed to load db, generating a new one...')
    if not DBProtocols.verifyAndLoadDB(dbStructure):
      print('failed to generate new db')
      return False
  else:
    # if we do have the db, proceed and have a different process varify and update it if needed
    print('varifying db in background')
    dbProcess = Process(target=DBProtocols.verifyAndLoadDB, kwargs={'dbStructure': dbStructure})
    dbProcess.start()

  cards = ['Sangonomiya Kokomi', 'Furina', 'Klee', 'Faruzan']

  for i in range(len(cards)):
    sharedAssets.app.systems['home'].addElements(
        Cards.GenshinCharacter.generate(
        cards[i],
        {
          'x': pgx.DynamicValue('number', 50),
          'y': pgx.DynamicValue('number', (44 * i) + 50),
          'width': pgx.DynamicValue('number', 600),
          'height': pgx.DynamicValue('number', 40)
        },
        'list'
      )
    )

  print('first update finished')
