import time
import orjson
import socket
from DBManagers.DBProcessors.Scraper import scrapeLayouts

TESTING_CONNECTION_HOSTS = (
  ('8.8.8.8', 53), # Google DNS
  ('1.1.1.1', 53), # Cloudflare DNS
  ('9.9.9.9', 53), # Quad9 DNS
  ('208.67.222.222', 53), # OpenDNS
)

def check_internet_connection(host: str = '8.8.8.8', port: int = 53, timeout: int = 5) -> bool:
  try:
    socket.setdefaulttimeout(timeout)
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
    return True
  except Exception as ex:
    print(f'Internet connection check failed: {host}:{port}')
    print(f'Error: {ex}')
    return False

def ensure_internet_connection(timeout: int = 5) -> bool:
  for host, port in TESTING_CONNECTION_HOSTS:
    if check_internet_connection(host, port, timeout):
      return True
  return False

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

def makeDB(layoutSourcesURL: str, dbStructureURL: str) -> tuple[dict, dict] | bool:
  print(f'Building database.')
  
  if not ensure_internet_connection():
    print('No internet connection available. Cannot proceed with database creation.')
    return False

  startTime = time.time()

  with open(layoutSourcesURL, 'rb') as layoutSourcesFile:
    layoutSources = orjson.loads(layoutSourcesFile.read())

  with open(dbStructureURL, 'rb') as dbStructureFile:
    dbStructure = orjson.loads(dbStructureFile.read())

  scrapedData, failedURLs, stallTime, waitingTime = scrapeLayouts(layoutSources)

  pages = dbStructure['pages']
  structure = dbStructure['structure']

  db = createObject(structure, pages, scrapedData)

  db['_metadata_'] = {
    "creationEpoch": int(time.time()),
    "failedURLs": failedURLs,
    "safe": True
  }

  totalTime = time.time() - startTime
  processingTime = totalTime - (stallTime + waitingTime)

  print(f'Stall time: {stallTime:.2f}')
  print(f'Requests response time: {waitingTime:.2f}')
  print(f'Processing time: {processingTime:.2f}')
  print(f'Total time: {totalTime:.2f}')

  return db, scrapedData
