import pygame as pg
import pg_extended as pgx
import sharedAssets

def addGINav(force: bool = False):
  window: pgx.Window = sharedAssets.app

  if 'GINav' in window.systems and not force:
    return

  system = pgx.System(preLoadState=True)

  container = pgx.Section(
    {
      'x': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=7),
      'y': 0,
      'width': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=93),
      'height': pgx.DynamicValue(sharedAssets.app, 'screenHeight', percent=5),
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
