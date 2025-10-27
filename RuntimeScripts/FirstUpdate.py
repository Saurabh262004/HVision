import orjson
import time
import os
from DBProcessors import makeDB, processDB
import sharedAssets

def firstUpdate():
  window = sharedAssets.app

  with open('./Data/App/config.json', 'rb') as f:
    sharedAssets.config = orjson.loads(f.read())

  with open(sharedAssets.config['DBStructureLocation'], 'rb') as f:
    dbStructure = orjson.loads(f.read())

  if not os.path.isdir(dbStructure['location']):
    os.makedirs(dbStructure['location'])
  else:
    print('Database location exists')

  dbLocation = os.path.join(dbStructure['location'], 'DB.json')

  if not os.path.isfile(dbLocation):
    makeDB(sharedAssets.config['layoutSourcesLocation'], sharedAssets.config['DBStructureLocation'])
    processDB(dbLocation)
  else:
    print('DB.json file exists')

  with open(dbLocation, 'rb') as f:
    sharedAssets.db = orjson.loads(f.read())

  dbAge = int(time.time()) - sharedAssets.db['_metadata_']['creationEpoch']

  if dbAge > 3600:
    makeDB(sharedAssets.config['layoutSourcesLocation'], sharedAssets.config['DBStructureLocation'])
    processDB(dbLocation)

    with open(dbLocation, 'rb') as f:
      sharedAssets.db = orjson.loads(f.read())
  else:
    print('DB isn\'t old enough. It won\'t be updated')
