import SharedAssets
import pg_extended as pgx

def addSystem():
  window = SharedAssets.app

  system: pgx.System = pgx.System()

  window.addSystem(system, 'GWDBList')

  window.setSystemZ('GWDBList', 3)
