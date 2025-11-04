import pygame as pg
import pg_extended as pgx
import sharedAssets

def addHome():
  window: pgx.Window = sharedAssets.app

  home: pgx.UI.System = pgx.UI.System()

  homeBG: pgx.Section = pgx.Section(
    {
      'x': pgx.DynamicValue('number', 0),
      'y': pgx.DynamicValue('number', 0),
      'width': pgx.DynamicValue('classNum', window, classAttribute='screenWidth'),
      'height': pgx.DynamicValue('classNum', window, classAttribute='screenHeight')
    }, pg.Color(20, 10, 20)
  )

  home.addElement(homeBG, 'homeBG')

  window.addSystem(home, 'home')

  window.setSystemZ('home', 0)
