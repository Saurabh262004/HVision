import pygame as pg
import pg_extended as pgx
import sharedAssets

def addHome() -> bool:
  window = sharedAssets.app

  if 'Home' in window.systems:
    return False

  home = pgx.System(preLoadState=True)

  homeBG = pgx.Section(
    {
      'x': 0,
      'y': 0,
      'width': pgx.DynamicValue(window, 'screenWidth'),
      'height': pgx.DynamicValue(window, 'screenHeight')
    }, pg.Color(20, 10, 20)
  )

  homeContainer = pgx.Section(
    {
      'x': pgx.DynamicValue(window, 'screenWidth', percent=7),
      'y': 0,
      'width': pgx.DynamicValue(window, 'screenWidth', percent=93),
      'height': pgx.DynamicValue(window, 'screenHeight')
    }, pg.Color(20, 10, 20)
  )

  homeContainer.activeDraw = False

  opTitleStart = pgx.DynamicValue(homeContainer, 'height')
  opTitleEnd = pgx.DynamicValue(homeContainer, 'height', percent=20)

  openingAnim = pgx.AnimatedValue(
    (
      opTitleStart,
      opTitleEnd
    ),
    500, 'start', 'easeInOut'
  )

  HVisionText = pgx.TextBox(
    pgx.Section(
      {
        'x': pgx.DynamicValue(homeContainer, 'x'),
        'y': pgx.DynamicValue(0),
        'width': pgx.DynamicValue(homeContainer, 'width'),
        'height': pgx.DynamicValue(openingAnim, 'value')
      }, pg.Color(20, 10, 20), 8
    ),
    'HVision',
    'Resources/Fonts/thicccboi/fonts/TTF/THICCCBOI-Bold.ttf',
    pg.Color(100, 100, 100, 100),
    pgx.DynamicValue(50)
  )

  HVisionText.lazyUpdate = False

  def triggetOPIntro():
    nonlocal openingAnim

    openingAnim.trigger(delay=500)

  window.customData['triggetOPIntroFunc'] = triggetOPIntro

  window.customAnimatedValues['openingAnim'] = openingAnim

  home.addElement(homeBG, 'homeBG')

  home.addElement(homeContainer, 'homeContainer')

  home.addElement(HVisionText, 'HVisionText')

  window.addSystem(home, 'Home')

  window.setSystemZ('Home', 0)

  return True
