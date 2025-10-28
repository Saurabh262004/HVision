import os
import time
import orjson
from DBProcessors import scrapeLayouts

def creatreDictList(itemStructure: dict | list, itemKey: str, pages: list[str], scrapedData: dict) -> dict:
  lst = {}

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
        item[valueKey] = f'N/A : data array length mismatch for key {valueKey}'
      except Exception as e:
        print(f"Error processing {valueKey} at index {i}: {e}")
        item[valueKey] = None

    lst[requiredDataArrays[itemKey][i]] = item

  return lst

def createList(itemStructure: list[int, str], pages: list[str], scrapedData: dict) -> list:
  lst = []

  pageKey = pages[itemStructure[0]]

  layoutKey = itemStructure[1]

  dataArray = scrapedData[pageKey][layoutKey]['data']

  for item in dataArray:
    lst.append(item)

  return lst

def createObject(structure: dict | list, pages: list[str], scrapedData: dict) -> dict:
  parent = {}

  for key in structure:
    structureType = structure[key].get('_type_')
    itemStructure = structure[key].get('_structure_')

    if structureType is None or itemStructure is None:
      continue

    if structureType == 'object':
      parent[key] = createObject(structure[key]['_structure_'], pages, scrapedData)
    elif structureType == 'dictList':
      itemKey = structure[key]['_key_']

      parent[key] = creatreDictList(itemStructure, itemKey, pages, scrapedData)
    elif structureType == 'list':
      parent[key] = createList(itemStructure, pages, scrapedData)

  return parent

def makeDB(layoutSourcesURL: str, dbStructureURL: str):
  startTime = time.time()

  with open(layoutSourcesURL, 'rb') as layoutSourcesFile:
    layoutSources = orjson.loads(layoutSourcesFile.read())

  with open(dbStructureURL, 'rb') as dbStructureFile:
    dbStructure = orjson.loads(dbStructureFile.read())

  print(f'Building database.')

  scrapedData, failedURLs = scrapeLayouts(layoutSources)

  db = {}

  dbLocation = dbStructure['location']
  pages = dbStructure['pages']
  structure = dbStructure['structure']

  if not os.path.exists(dbLocation):
    os.makedirs(dbLocation)

  dbFilePath = os.path.join(dbLocation, 'DB.json')
  rawFilePath = os.path.join(dbLocation, 'Raw.json')

  with open(rawFilePath, 'wb') as rawFile:
    rawFile.write(orjson.dumps(scrapedData, option=orjson.OPT_INDENT_2))

  db = createObject(structure, pages, scrapedData)

  db['_metadata_'] = {
    "creationEpoch": int(time.time()),
    "failedURLs": failedURLs
  }

  with open(dbFilePath, 'wb') as dbFile:
    dbFile.write(orjson.dumps(db, option=orjson.OPT_INDENT_2))

  endTime = time.time()
  stallTime = len(scrapedData) * 2
  processingTime = (endTime - startTime) - stallTime

  print(f"Created DB in {processingTime:.2f} seconds (excluding {stallTime} seconds of stall time).")
