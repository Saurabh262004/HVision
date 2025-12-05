from UI.Systems.Nav import Sidebar
from UI.Systems.Home import addHome
from UI.Systems.DBUpdateIndicator import addIndicator
from UI.Systems.Genshin.DBSystems import DBList as GCDBList
from UI.Systems.Genshin.DBSystems import SearchFilters as GCDBFilters
from UI.Systems.Genshin import GINav as GINav
import SharedAssets

def setupSystems():
  addHome()

  Sidebar.addSystem()

  addIndicator()

  GCDBList.addSystem()

  GCDBFilters.addSystem()

  GINav.addGINav()

  SharedAssets.app.activateSystems(['Nav', 'Home'])
