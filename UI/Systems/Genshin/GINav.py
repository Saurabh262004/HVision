import pygame as pg
import pg_extended as pgx
from UI import SystemSwitch
import SharedAssets

def addGINav(force: bool = False):
  window: pgx.Window = SharedAssets.app

  if 'GINav' in window.systems and not force:
    return

  system = pgx.System(preLoadState=True)

  container = pgx.Section(
    {
      'x': pgx.DynamicValue(SharedAssets.app, 'screenWidth', percent=7),
      'y': 0,
      'width': pgx.DynamicValue(SharedAssets.app, 'screenWidth', percent=93),
      'height': pgx.DynamicValue(SharedAssets.app, 'screenHeight', percent=5),
    },
    pgx.ImgManipulation.getGradient(
      [
        (255, 255, 255, 32),
        (0, 0, 0)
      ],
      [20, 1],
      'down'
    ),
    backgroundSizeType='squish'
  )

  chrListSelector = pgx.Button(
    pgx.TextBox(
      pgx.Section(
        {
          'x': pgx.DynamicValue(container, 'x'),
          'y': pgx.DynamicValue(container, 'y'),
          'width': pgx.DynamicValue(container, 'width', percent=10),
          'height': pgx.DynamicValue(container, 'height')
        }, pg.Color(255, 255, 255, 64)
      ),
      'Characters', 'Arial',
      pg.Color(200, 200, 200),
      pgx.DynamicValue(container, 'height', percent=50)
    ),
    pgx.CallbackSet(
      (
        pgx.Callback(
          ('mouseUp',),
          SystemSwitch.switch,
          {'systems': ['Nav', 'GCDBList', 'GCDBFilters', 'GINav']}
        ),
      )
    ),
    pressedBG=pg.Color(255, 255, 255, 16)
  )

  wpnListSelector = pgx.Button(
    pgx.TextBox(
      pgx.Section(
        {
          'x': pgx.DynamicValue(lambda: container.x + (container.width / 10)),
          'y': pgx.DynamicValue(container, 'y'),
          'width': pgx.DynamicValue(container, 'width', percent=10),
          'height': pgx.DynamicValue(container, 'height')
        }, pg.Color(255, 255, 255, 64)
      ),
      'Weapons', 'Arial',
      pg.Color(200, 200, 200),
      pgx.DynamicValue(container, 'height', percent=50)
    ),
    pgx.CallbackSet(
      (
        pgx.Callback(
          ('mouseUp',),
          SystemSwitch.switch,
          {'systems': ['Nav', 'GWDBList', 'GWDBFilters', 'GINav']}
        ),
      )
    ),
    pressedBG=pg.Color(255, 255, 255, 16)
  )

  system.addElements({
    'navContainer': container,
    'chrListSelector': chrListSelector,
    'wpnListSelector': wpnListSelector
  })

  window.addSystem(system, 'GINav')

  window.setSystemZ('GINav', 999)
