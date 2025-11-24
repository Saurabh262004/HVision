import os
import pygame as pg
import pg_extended as pgx
import sharedAssets
from UI import SystemSwitch

HOME_CARDS_DATA = {
  'titles': (
    'Genshin Impact',
    'Zenless Zone Zero'
  ),
  'iconNames': (
    'Genshin_Logo',
    'Zenless_Logo'
  ),
  'bgSizes': (
    150,
    70
  ),
  'systems': (
    ['Nav', 'GCDBList', 'GCDBFilters'],
    []
  ),
  'len': 2
}

def getSectionCards(container: pgx.Section) -> dict[str, pgx.UIElement]:
  global HOME_CARDS_DATA

  imageDBLocation = sharedAssets.config['ImageDBLocation']

  icons = [
    pg.image.load(
      os.path.join(
        imageDBLocation,
        'common',
        iconName
      )
    ).convert_alpha()

    for iconName in HOME_CARDS_DATA['iconNames']
  ]

  per = lambda val, perc: val / 100 * perc

  matrixRows = 5
  sectionWidthPer = 15
  sectionHeightPer = per(sectionWidthPer, 50)
  marginPer = (100 - (sectionWidthPer * matrixRows)) / (matrixRows + 1)

  def getSectionX(i: int):
    nonlocal per, sectionWidthPer, marginPer, matrixRows

    sx = container.x

    sw = container.width

    i = i % matrixRows

    padding = per(sw, marginPer)

    sectionWidth = per(sw, sectionWidthPer + marginPer)

    return sx + padding + (sectionWidth * i)

  def getSectionY(i: int):
    nonlocal per, sectionWidthPer, sectionHeightPer, marginPer, matrixRows

    sy = container.y

    sh = container.height

    sw = container.width

    i = int(i / matrixRows)

    padding = per(sh, 10)

    sectionHeight = per(sw, sectionHeightPer) + per(sw, marginPer)

    return sy + padding + (sectionHeight * i)

  cards = {}
  for i in range(HOME_CARDS_DATA['len']):
    bg = pgx.Section(
      {
        'x': pgx.DynamicValue(getSectionX, args={'i': i}),
        'y': pgx.DynamicValue(getSectionY, args={'i': i}),
        'width': pgx.DynamicValue(container, 'width', percent=sectionWidthPer),
        'height': pgx.DynamicValue(container, 'width', percent=sectionHeightPer)
      }, pg.Color(100, 100, 100, 64), 10
    )

    icon = pgx.Section(
      bg.dimensions, icons[i], 0, 'fit', 'center', HOME_CARDS_DATA['bgSizes'][i]
    )

    btn = pgx.Button(
      bg,
      callback=pgx.CallbackSet(
        (
          pgx.Callback(
            ('mouseUp',),
            SystemSwitch.switch,
            {
              'systems': HOME_CARDS_DATA['systems'][i]
            }
          ),
        )
      )
    )

    cards[f'{HOME_CARDS_DATA['iconNames'][i]}_btn'] = btn
    cards[f'{HOME_CARDS_DATA['iconNames'][i]}_icon'] = icon

  return cards

def addHome() -> bool:
  window = sharedAssets.app

  if 'Home' in window.systems:
    return False

  home = pgx.System(preLoadState=True)

  homeContainer = pgx.Section(
    {
      'x': pgx.DynamicValue(window, 'screenWidth', percent=7),
      'y': pgx.DynamicValue(0),
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

  cards = getSectionCards(homeContainer)

  def triggetOPIntro():
    nonlocal openingAnim

    openingAnim.trigger(delay=500)

  window.customData['triggetOPIntroFunc'] = triggetOPIntro

  window.customAnimatedValues['openingAnim'] = openingAnim

  home.addElement(homeContainer, 'homeBG')

  home.addElement(HVisionText, 'HVisionText')

  home.addElements(cards)

  window.addSystem(home, 'Home')

  window.setSystemZ('Home', 0)

  return True
