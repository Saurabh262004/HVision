import pygame as pg
import pg_extended as pgx
import sharedAssets

def addSystem() -> bool:
  window: pgx.Window = sharedAssets.app

  if 'GCDBFilters' in window.systems:
    return False

  system = pgx.System(preLoadState=True)

  filtersHeader = pgx.TextBox(
    pgx.Section(
      {
        'x': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=68),
        'y': pgx.DynamicValue(window, 'screenHeight', percent=3),
        'width': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=29),
        'height': pgx.DynamicValue(window, 'screenHeight', percent=4)
      }, pg.Color(250, 250, 250, 64), 7
    ), 'Filters', 'Arial', pg.Color(200, 200, 200)
  )

  filtersHeader.drawSectionDefault = True

  filterSection = pgx.Section(
    {
      'x': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=68),
      'y': pgx.DynamicValue(window, 'screenHeight', percent=10),
      'width': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=29),
      'height': pgx.DynamicValue(window, 'screenHeight', percent=80)
    }, pg.Color(250, 250, 250, 64), 7
  )

  system.addElements({
    'filtersHeader': filtersHeader,
    'filterSection': filterSection
  })

  window.addSystem(system, 'GCDBFilters')

  window.setSystemZ('GCDBFilters', 2)

  return True
