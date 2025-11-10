import pygame as pg
import pg_extended as pgx
import sharedAssets

def addIndicator():
  system = pgx.System()

  tetWidth = pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=2)
  tetX = pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=97.5)

  # default colour fill looks like it was drawn by a baby. I can literally see the pixels
  tetBack1 = pg.Surface((256, 256), pg.SRCALPHA)

  pg.draw.aacircle(tetBack1, pg.Color(111, 171, 121), (128, 128), 127, 0)

  tet = pgx.Section(
    {
      'x': tetX,
      'y': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=.5),
      'width': tetWidth,
      'height': tetWidth
    }, tetBack1
  )

  system.addElement(tet, 'tet0')

  sharedAssets.app.addSystem(system, 'dbIndicator')

  sharedAssets.app.setSystemZ('dbIndicator', 10)
