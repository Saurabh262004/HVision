import os
import orjson
import time
import sharedAssets
from DBProcessors.ImageCollector import updateImageDB

def processDB(DBLocation: str) -> bool:
  startTime = time.time()

  if not os.path.exists(DBLocation):
    return False

  with open(DBLocation, 'rb') as dbFile:
    db = orjson.loads(dbFile.read())

  # create a proper manifest for image collector
  manifest = {}

  for manifestName in db['ImageCollectorManifestData']:
    manifestPart = db['ImageCollectorManifestData'][manifestName]

    for itemName in manifestPart:
      # remove errored data
      if itemName.startswith('N/A'):
        continue

      # remove query parameters from image URLs
      url: str = manifestPart[itemName]['URL']

      endIndex = url.find('.png') + 4

      url = url[:endIndex]

      manifest[f'{manifestName}_{itemName}'] = url

  del db['ImageCollectorManifestData']

  db['ImageCollectorManifest'] = manifest

  with open(DBLocation, 'wb') as dbFile:
    dbFile.write(orjson.dumps(db, option=orjson.OPT_INDENT_2))

  endTime = time.time()
  processingTime = endTime - startTime

  print(f"Done post-processing DataBase in {processingTime:.2f} seconds.")

  updateImageDB(sharedAssets.config['imageDBLocation'], manifest)

  return True
