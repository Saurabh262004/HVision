import time

def deleteKeyRecursive(obj, targetKey):
  if isinstance(obj, dict):
    keys_to_delete = [key for key in obj if key.startswith(targetKey)]

    for key in keys_to_delete:
      del obj[key]

    for value in list(obj.values()):
      deleteKeyRecursive(value, targetKey)

  elif isinstance(obj, list):
    for item in obj:
      deleteKeyRecursive(item, targetKey)

def processDB(db: dict) -> dict:
  startTime = time.time()

  # remove all the N/A data
  deleteKeyRecursive(db, 'N/A')

  # create a proper manifest for image collector
  manifest = {}

  for manifestName in db['ImageCollectorManifestData']:
    manifestPart = db['ImageCollectorManifestData'][manifestName]

    for itemName in manifestPart:
      # remove query parameters from image URLs
      url: str = manifestPart[itemName]['URL']

      endIndex = url.find('.png') + 4

      url = url[:endIndex]

      manifest[f'{manifestName}_{itemName}'] = url

  del db['ImageCollectorManifestData']

  db['ImageCollectorManifest'] = manifest

  endTime = time.time()
  processingTime = endTime - startTime

  print(f"Done post-processing DataBase in {processingTime:.2f} seconds.")

  return db
