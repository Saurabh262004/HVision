import pygame as pg
import pg_extended as pgx
import sharedAssets

def addHome():
  window = sharedAssets.app

  home = pgx.UI.System()

  homeBG = pgx.Section(
    {
      'x': pgx.DynamicValue('number', 0),
      'y': pgx.DynamicValue('number', 0),
      'width': pgx.DynamicValue('classNum', window, classAttribute='screenWidth'),
      'height': pgx.DynamicValue('classNum', window, classAttribute='screenHeight')
    }, pg.Color(20, 10, 20)
  )

  openingAnim = pgx.AnimatedValue(
    (
      pgx.DynamicValue('classNum', window, classAttribute='screenHeight'),
      pgx.DynamicValue('classPer', window, classAttribute='screenHeight', percent=20)
    ), 250, 'start', 'easeOut'
  )

  HVisionText = pgx.TextBox(
    pgx.Section(
      {
        'x': pgx.DynamicValue('number', 0),
        'y': pgx.DynamicValue('number', 0),
        'width': pgx.DynamicValue('classNum', window, classAttribute='screenWidth'),
        'height': pgx.DynamicValue('classNum', openingAnim, classAttribute='value')
      }, pg.Color(20, 10, 20), 8
    ),
    'HVision',
    'Resources/Fonts/thicccboi/fonts/TTF/THICCCBOI-Bold.ttf',
    pg.Color(100, 100, 100, 100),
    pgx.DynamicValue('number', 50)
  )

  HVisionText.lazyUpdate = False

  window.customAnimatedValues.append(openingAnim)

  home.addElement(homeBG, 'homeBG')

  home.addElement(HVisionText, 'HVisionText')

  window.addSystem(home, 'home')

  window.setSystemZ('home', 0)
