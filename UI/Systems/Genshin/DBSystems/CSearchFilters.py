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

  filterList = pgx.List(
    {
      'x': pgx.DynamicValue(lambda: filterSection.x + (filterSection.width / 20)),
      'y': pgx.DynamicValue(lambda: filterSection.y + (filterSection.height / 40))
    },
    pgx.Section(
      {
        'x': pgx.DynamicValue(lambda: filterSection.x + (filterSection.width / 20)),
        'y': pgx.DynamicValue(lambda: filterSection.y + (filterSection.height / 40)),
        'width': pgx.DynamicValue(filterSection, 'width', percent=90),
        'height': pgx.DynamicValue(filterSection, 'height', percent=20)
      }, pg.Color(255, 255, 255, 128)
    ), 4,
    pgx.DynamicValue(filterSection, 'height', percent=3)
  )

  filterList.elements[0].dimensions['height'] = pgx.DynamicValue(filterSection, 'height', percent=10)

  system.addElements({
    'filtersHeader': filtersHeader,
    'filterSection': filterSection,
    'raritySection': filterList.elements[0],
    'elementsSection': filterList.elements[1],
    'weaponsSection': filterList.elements[2],
    'regionSection': filterList.elements[3],
  })

  window.addSystem(system, 'GCDBFilters')

  window.setSystemZ('GCDBFilters', 2)

  return True
