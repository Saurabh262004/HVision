from UI.Systems.Nav import Sidebar
from UI.Systems.Home import addHome
from UI.Systems.DBUpdateIndicator import addIndicator
from UI.Systems.Genshin.DBSystems import CDBList as GCDBList
from UI.Systems.Genshin.DBSystems import CSearchFilters as GCDBFilters
from UI.Systems.Genshin.DBSystems import WDBList as GWDBList
from UI.Systems.Genshin.DBSystems import WSearchFilters as GWDBFilters
from UI.Systems.Genshin import GINav as GINav
import SharedAssets

def setupSystems():
  addHome()

  Sidebar.addSystem()

  addIndicator()

  GINav.addGINav()

  GCDBList.addSystem()

  GCDBFilters.addSystem()

  GWDBList.addSystem()

  GWDBFilters.addSystem()

  SharedAssets.app.activateSystems(['Nav', 'Home'])
