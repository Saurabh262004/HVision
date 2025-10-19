import pygame as pg
import pg_extended as pgx

def addHome(window: pgx.Window):
  homeSystem: pgx.UI.System = pgx.UI.System()

  bgSurface: pg.Surface = pg.Surface((1000, 1000))

  pg.draw.rect(bgSurface, (128, 64, 200), (0, 0, 1000, 1000))

  homeBG: pgx.Section = pgx.Section(
    {
      'x': pgx.DynamicValue('number', 0),
      'y': pgx.DynamicValue('number', 0),
      'width': pgx.DynamicValue('classNum', window, classAttribute='screenWidth'),
      'height': pgx.DynamicValue('classNum', window, classAttribute='screenHeight')
    }, bgSurface, backgroundSizeType='squish'
  )

  homeSystem.addElement(homeBG, 'homeBG')

  window.addSystem(homeSystem, 'homeSystem')

  window.setSystemZ('homeSystem', 0)
