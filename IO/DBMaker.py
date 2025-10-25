import os
import json
from Network import scrapeLayouts

def makeDB(layoutSourcesURL: str, dbStructureURL: str):
  with open(layoutSourcesURL, 'r') as layoutSourcesFile:
    layoutSources = json.load(layoutSourcesFile)

  with open(dbStructureURL, 'r') as dbStructureFile:
    dbStructure = json.load(dbStructureFile)

  scrapedData, failedURLs = scrapeLayouts(layoutSources)

  db = {}

  dbLocation = dbStructure['location']
  pages = dbStructure['pages']
  structure = dbStructure['structure']

  if not os.path.exists(dbLocation):
    os.makedirs(dbLocation)

  dbFilePath = os.path.join(dbLocation, 'db.json')
  rawFilePath = os.path.join(dbLocation, 'raw.json')

  def handleStructure(structure):
    nonlocal pages, scrapedData
    parent = {}

    for key in structure:
      if structure[key]['_type_'] == 'object':
        parent[key] = handleStructure(structure[key]['_structure_'])
      elif structure[key]['_type_'] == 'list':
        data = {}

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

          data[requiredDataArrays[itemKey][i]] = item

        parent[key] = data

    return parent

  db = handleStructure(structure)

  with open(dbFilePath, 'w') as dbFile:
    json.dump(db, dbFile, indent=2)

  with open(rawFilePath, 'w') as rawFile:
    json.dump(scrapedData, rawFile)
