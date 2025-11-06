import os
import time
import orjson
import traceback
from multiprocessing import Process
from DBProcessors import makeDB, processDB
from DBProcessors.ImageCollector import updateImageDB
import sharedAssets

DEFAULT_CONFIG = {
  "DBLocation": "./Resources/Essentials/DataBase/",
  "ImageDBLocation": "./Resources/Assets/GameAssets/",
  "layoutSourcesFileLocation": "./Resources/Essentials/LayoutSources.json",
  "DBFileName": "DB.json",
  "RawDBFileName": "Raw.json",
  "DBStructureFileName": "Structure.json",
  "MaxDBAge": 3600
}

CONFIG_LOCATION = './Data/App/'

CONFIG_FILE_LOCATION = os.path.join(CONFIG_LOCATION, 'config.json')

class DBProtocols:
  @staticmethod
  def dbEventOpen(event: str) -> bool:
    dbDir = sharedAssets.config['DBLocation']

    if not os.path.isdir(dbDir):
      os.makedirs(dbDir)

    eventFileLocation = os.path.join(
      dbDir,
      event
    )

    if os.path.exists(eventFileLocation):
      return False

    open(eventFileLocation, 'a').close()

    return True

  @staticmethod
  def dbEventClose(event: str) -> bool:
    dbDir = sharedAssets.config['DBLocation']

    if not os.path.isdir(dbDir):
      os.makedirs(dbDir)

    eventFileLocation = os.path.join(
      dbDir,
      event
    )

    if os.path.exists(eventFileLocation):
      os.remove(eventFileLocation)

      return True

    return False

  @staticmethod
  def dbEventCheck(event: str) -> bool:
    dbDir = sharedAssets.config['DBLocation']

    if not os.path.isdir(dbDir):
      os.makedirs(dbDir)

    eventFileLocation = os.path.join(
      dbDir,
      event
    )

    if os.path.exists(eventFileLocation):
      return True

    return False

  @staticmethod
  def loadDefaultConfig():
    sharedAssets.config = DEFAULT_CONFIG

  @staticmethod
  def writeDefaultConfig() -> bool:
    if not os.path.isdir(CONFIG_LOCATION):
      os.makedirs(CONFIG_LOCATION)

    try:
      with open(CONFIG_FILE_LOCATION, 'wb') as f:
        f.write(orjson.dumps(DEFAULT_CONFIG, option=orjson.OPT_INDENT_2))
        return True
    except:
      return False

  @staticmethod
  def loadConfig() -> bool:
    try:
      with open(CONFIG_FILE_LOCATION, 'rb') as f:
        sharedAssets.config = orjson.loads(f.read())
        return True
    except:
      return False

  @staticmethod
  def writeConfig(config: dict = None) -> bool:
    if config is None:
      config = sharedAssets.config

    if config is None:
      return False

    if not os.path.isdir(CONFIG_LOCATION):
      os.makedirs(CONFIG_LOCATION)

    try:
      with open(CONFIG_FILE_LOCATION, 'wb') as f:
        f.write(orjson.dumps(config, option=orjson.OPT_INDENT_2))
        return True
    except:
      return False

  @staticmethod
  def verifyConfig() -> bool:
    if (sharedAssets.config is None) and (not DBProtocols.loadConfig()):
      print('Warning: Failed to load config file, loading default config')

      DBProtocols.loadDefaultConfig()

      DBProtocols.writeDefaultConfig()

      return False

    return True

  @staticmethod
  def loadDBStructure() -> bool:
    DBProtocols.verifyConfig()

    dbStructureLocation = os.path.join(
      sharedAssets.config['DBLocation'],
      sharedAssets.config['DBStructureFileName']
    )

    try:
      with open(dbStructureLocation, 'rb') as f:
        sharedAssets.dbStructure = orjson.loads(f.read())
        return True
    except:
      return False

  @staticmethod
  def loadDB() -> bool:
    DBProtocols.verifyConfig()

    dbFileLocation = os.path.join(
      sharedAssets.config['DBLocation'],
      sharedAssets.config['DBFileName']
    )

    try:
      with open(dbFileLocation, 'rb') as f:
        sharedAssets.db = orjson.loads(f.read())
        return True
    except:
      return False

  @staticmethod
  def writeDB(db: dict = None) -> bool:
    DBProtocols.verifyConfig()

    if db is None:
      db = sharedAssets.db

    dbDir = sharedAssets.config['DBLocation']

    dbFileLocation = os.path.join(
      dbDir,
      sharedAssets.config['DBFileName']
    )

    if not os.path.isdir(dbDir):
      os.makedirs(dbDir)

    try:
      with open(dbFileLocation, 'wb') as f:
        f.write(orjson.dumps(db, option=orjson.OPT_INDENT_2))
        return True
    except:
      return False

  @staticmethod
  def writeRaw(raw: dict) -> bool:
    DBProtocols.verifyConfig()

    dbDir = sharedAssets.config['DBLocation']

    rawFileLocation = os.path.join(
      dbDir,
      sharedAssets.config['RawDBFileName']
    )

    if not os.path.isdir(dbDir):
      os.makedirs(dbDir)

    try:
      with open(rawFileLocation, 'wb') as f:
        f.write(orjson.dumps(raw, option=orjson.OPT_INDENT_2))
        return True
    except:
      return False

  @staticmethod
  def generateDB() -> bool:
    DBProtocols.verifyConfig()

    dbStructureLocation = os.path.join(
      sharedAssets.config['DBLocation'],
      sharedAssets.config['DBStructureFileName']
    )

    layoutSourceLocation = sharedAssets.config['layoutSourcesFileLocation']

    try:
      db, raw = makeDB(layoutSourceLocation, dbStructureLocation)

      db = processDB(db)

      DBProtocols.writeDB(db)
      DBProtocols.writeRaw(raw)

      updateImageDB(
        os.path.join(sharedAssets.config['ImageDBLocation'],'specific'),
        db['ImageCollectorManifest']
      )

      return True
    except:
      traceback.print_exc()
      return False

  @staticmethod
  def verifyDB() -> bool:
    DBProtocols.verifyConfig()

    if sharedAssets.dbStructure is None:
      DBProtocols.loadDBStructure()

      if sharedAssets.dbStructure is None:
        DBProtocols.dbEventClose('DBSafe')

        print('Fatal: Couldn\'t load Database structure')

        return False

    dbDir = sharedAssets.config['DBLocation']

    dbFileLocation = os.path.join(
      dbDir,
      sharedAssets.config['DBFileName']
    )

    validDB = True

    if not os.path.isdir(dbDir):
      print('Error: Database location doesn\'t exist')

      os.makedirs(dbDir)

      validDB = False
    else:
      print('Info: Database location exists')

      if not os.path.isfile(dbFileLocation):
        print('Error: Database file doesn\'t exist')

        validDB = False
      else:
        print('Info: Database file exists')

    if not validDB:
      DBProtocols.dbEventClose('DBSafe')

      print('Error: No valid Database exists, generating new Database')

      if not DBProtocols.generateDB():
        print('Fatal: Couldn\'t generate new Database')

        return False

      if not DBProtocols.loadDB():
        print('Fatal: could not load database')
        return False

      DBProtocols.dbEventOpen('DBUpdate')
    else:
      if not DBProtocols.loadDB():
        print('Fatal: could not load database')
        return False

      print('Info: Database loaded successfully')

      dbAge = int(time.time()) - sharedAssets.db['_metadata_']['creationEpoch']

      if dbAge > sharedAssets.config['MaxDBAge']:
        print('Info: Database is old, Generating new Database')

        if not DBProtocols.generateDB():
          DBProtocols.dbEventClose('DBSafe')

          print('Fatal: Couldn\'t generate new Database')

          return False

        DBProtocols.dbEventOpen('DBUpdate')

      else:
        print('DB isn\'t old enough. It won\'t be updated')

    DBProtocols.dbEventOpen('DBSafe')

    return True

  def verifyDBBackground():
    verifyProcess = Process(target=DBProtocols.verifyDB)
    verifyProcess.start()
