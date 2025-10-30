import os
import time
import orjson
from DBProcessors import makeDB, processDB
import sharedAssets

class DBProtocols:
  @staticmethod
  def loadConfig() -> bool:
    try:
      with open('./Data/App/config.json', 'rb') as f:
        sharedAssets.config = orjson.loads(f.read())
        return True
    except:
      return False

  @staticmethod
  def loadDBStructure() -> object | None:
    try:
      with open(sharedAssets.config['DBStructureLocation'], 'rb') as f:
        return orjson.loads(f.read())
    except:
      return None

  @staticmethod
  def loadDB(location: str) -> bool:
    try:
      with open(os.path.join(location, 'DB.json'), 'rb') as f:
        sharedAssets.db = orjson.loads(f.read())
        return True
    except:
      return False

  @staticmethod
  def generateDB(dbLocation: str) -> bool:
    try:
      makeDB(sharedAssets.config['layoutSourcesLocation'], sharedAssets.config['DBStructureLocation'])
      processDB(dbLocation)
      return True
    except:
      return False

  @staticmethod
  def verifyAndLoadDB(dbStructure: dict) -> bool:
    dbLocation = os.path.join(dbStructure['location'], 'DB.json')

    validDB = True

    if not os.path.isdir(dbStructure['location']):
      os.makedirs(dbStructure['location'])
      validDB = False
    else:
      print('Database location exists')

    if not os.path.isfile(dbLocation):
      validDB = False
    else:
      print('DB.json file exists')

    if (not validDB) and (not DBProtocols.generateDB(dbStructure['location'])):
      return False

    if not DBProtocols.loadDB(dbStructure['location']):
      return False

    dbAge = int(time.time()) - sharedAssets.db['_metadata_']['creationEpoch']

    if dbAge > 3600:
      if not DBProtocols.generateDB(dbStructure['location']):
        return False

      if not DBProtocols.loadDB(dbStructure['location']):
        return False
    else:
      print('DB isn\'t old enough. It won\'t be updated')

    return True
