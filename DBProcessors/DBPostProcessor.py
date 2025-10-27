import os
import orjson

def processDB(DBLocation: str) -> bool:
  if not os.path.exists(DBLocation):
    return False

  with open(DBLocation, 'rb') as dbFile:
    db = orjson.loads(dbFile.read())

  # remove query parameters from character icon URLs
  for character in db['GenshinImpact']['Items']['Characters'].values():
    iconURL: str = character['IconURL']

    endIndex = iconURL.find('.png') + 4

    iconURL = iconURL[:endIndex]

    character['IconURL'] = iconURL

  with open(DBLocation, 'wb') as dbFile:
    dbFile.write(orjson.dumps(db, option=orjson.OPT_INDENT_2))
  
  return True
