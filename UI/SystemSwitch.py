import SharedAssets

def switch(systems: list[str]):
  SharedAssets.app.deactivateSystems('all')

  SharedAssets.app.activateSystems(systems)
