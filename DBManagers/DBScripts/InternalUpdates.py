import sharedAssets
from DBManagers.DBScripts.DBProtocols import DBProtocols

class InternalUpdates:
  @staticmethod
  def updateInternalDB():
    DBProtocols.loadDB()
    DBProtocols.dbEventClose('DBUpdate')

  @staticmethod
  def updateGCList():
    sharedAssets.app.customData['GCList'].updateCharactersData()
    sharedAssets.app.customData['GCList'].prevSearchMethod(sharedAssets.app.customData['GCList'].prevSearch)
