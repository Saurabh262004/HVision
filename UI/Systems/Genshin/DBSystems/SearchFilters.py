import pygame as pg
import pg_extended as pgx
import SharedAssets

def addSystem() -> bool:
  window: pgx.Window = SharedAssets.app

  if 'GCDBFilters' in window.systems:
    return False

  system = pgx.System(preLoadState=True)

  filtersHeader = pgx.TextBox(
    pgx.Section(
      {
        'x': pgx.DynamicValue(SharedAssets.app, 'screenWidth', percent=68),
        'y': pgx.DynamicValue(window, 'screenHeight', percent=7),
        'width': pgx.DynamicValue(SharedAssets.app, 'screenWidth', percent=29),
        'height': pgx.DynamicValue(window, 'screenHeight', percent=4)
      }, pg.Color(250, 250, 250, 64), 7
    ), 'Filters', 'Arial', pg.Color(200, 200, 200)
  )

  filtersHeader.drawSectionDefault = True

  filterSection = pgx.Section(
    {
      'x': pgx.DynamicValue(SharedAssets.app, 'screenWidth', percent=68),
      'y': pgx.DynamicValue(window, 'screenHeight', percent=14),
      'width': pgx.DynamicValue(SharedAssets.app, 'screenWidth', percent=29),
      'height': pgx.DynamicValue(window, 'screenHeight', percent=83)
    }, pg.Color(250, 250, 250, 64), 7
  )

  system.addElements({
    'filtersHeader': filtersHeader,
    'filterSection': filterSection
  })

  window.addSystem(system, 'GCDBFilters')

  window.setSystemZ('GCDBFilters', 2)

  return True
