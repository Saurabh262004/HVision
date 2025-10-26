import os
import time
import orjson
from Network import scrapeLayouts

def createObject(structure, pages, scrapedData):
  parent = {}

  for key in structure:
    if structure[key]['_type_'] == 'object':
      parent[key] = createObject(structure[key]['_structure_'], pages, scrapedData)
    elif structure[key]['_type_'] == 'list':
      lst = {}

      itemStructure = structure[key]['_structure_']

      itemKey = structure[key]['_key_']

      requiredDataArrays = {}

      for valueKey in itemStructure:
        valueLoc = itemStructure[valueKey]

        pageKey = pages[valueLoc[0]]

        layoutKey = valueLoc[1]

        requiredDataArrays[valueKey] = scrapedData[pageKey][layoutKey]['data']

      maxItemsPossible = 0

      for dataArray in requiredDataArrays.values():
        if len(dataArray) > maxItemsPossible:
          maxItemsPossible = len(dataArray)

      for i in range(maxItemsPossible):
        item = {}

        for valueKey in itemStructure:
          if valueKey == itemKey:
            continue

          try:
            item[valueKey] = requiredDataArrays[valueKey][i]
          except IndexError:
            item[valueKey] = None
          except Exception as e:
            print(f"Error processing {valueKey} at index {i}: {e}")
            item[valueKey] = None

        lst[requiredDataArrays[itemKey][i]] = item

      parent[key] = lst

  return parent

def makeDB(layoutSourcesURL: str, dbStructureURL: str):
  startTime = time.time()

  with open(layoutSourcesURL, 'rb') as layoutSourcesFile:
    layoutSources = orjson.loads(layoutSourcesFile.read())

  with open(dbStructureURL, 'rb') as dbStructureFile:
    dbStructure = orjson.loads(dbStructureFile.read())

  scrapedData, failedURLs = scrapeLayouts(layoutSources)

  db = {}

  dbLocation = dbStructure['location']
  pages = dbStructure['pages']
  structure = dbStructure['structure']

  if not os.path.exists(dbLocation):
    os.makedirs(dbLocation)

  dbFilePath = os.path.join(dbLocation, 'db.json')
  rawFilePath = os.path.join(dbLocation, 'raw.json')

  db = createObject(structure, pages, scrapedData)

  db['_metadata_'] = {
    "creationEpoch": int(time.time()),
    "failedURLs": failedURLs
  }

  with open(dbFilePath, 'wb') as dbFile:
    dbFile.write(orjson.dumps(db, option=orjson.OPT_INDENT_2))

  with open(rawFilePath, 'wb') as rawFile:
    rawFile.write(orjson.dumps(scrapedData, option=orjson.OPT_INDENT_2))

  endTime = time.time()
  stallTime = len(scrapedData) * 2
  processingTime = (endTime - startTime) - stallTime

  print(f"Created DB in {processingTime:.2f} seconds (excluding {stallTime} seconds of stall time).")
