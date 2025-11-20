from UI.Systems.Home import addHome
from UI.Systems.DBUpdateIndicator import addIndicator
from UI.Systems.Genshin.DBSystems import DBList as GCDBList
from UI.Systems.Genshin.DBSystems import SearchFilters as GCDBFilters
import sharedAssets

def setupSystems():
  addHome()

  addIndicator()

  GCDBList.addSystem()

  GCDBFilters.addSystem()

  sharedAssets.app.activateSystems(['GCDBList', 'GCDBFilters'])
