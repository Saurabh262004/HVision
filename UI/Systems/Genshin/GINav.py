import pygame as pg
import pg_extended as pgx
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

  system.addElements(
    {
      'navContainer': container,
    }
  )

  window.addSystem(system, 'GINav')

  window.setSystemZ('GINav', 1000)
