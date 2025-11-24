import sharedAssets

def switch(systems: list[str]):
  sharedAssets.app.deactivateSystems('all')

  sharedAssets.app.activateSystems(systems)
