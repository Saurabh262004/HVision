from UI.Systems.Home import addHome
from UI.Systems.DBUpdateIndicator import addIndicator
from UI.Systems.Genshin.DBSystems import GenshinCharacters
import sharedAssets

def setupSystems():
  addHome()

  addIndicator()

  GenshinCharacters.addSystem()

  sharedAssets.app.activateSystems(['genshinCharacters'])
