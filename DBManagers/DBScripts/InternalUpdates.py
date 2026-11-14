import SharedAssets
from DBManagers.DBScripts.DBProtocols import DBProtocols

class InternalUpdates:
	@staticmethod
	def updateInternalDB():
		DBProtocols.loadDB()
		DBProtocols.loadOldDB()
		DBProtocols.dbEventClose('DBUpdate')

	@staticmethod
	def updateGCList():
		SharedAssets.app.customData['GCList'].prevSearchMethod(SharedAssets.app.customData['GCList'].prevSearch)
