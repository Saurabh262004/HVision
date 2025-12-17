import SharedAssets
import pg_extended as pgx

def addSystem():
  window = SharedAssets.app

  system: pgx.System = pgx.System()

  window.addSystem(system, 'GWDBFilters')

  window.setSystemZ('GWDBFilters', 4)
