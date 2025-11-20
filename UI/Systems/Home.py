import os
import pygame as pg
import pg_extended as pgx
import sharedAssets

HOME_CARDS_DATA = {
  'titles': (
    'Genshin Impact',
    'Zenless Zone Zero'
  ),
  'iconNames': (
    'Genshin_Logo',
    'Zenless_Logo'
  ),
  'len': 2
}

def getSectionCards():
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

    sw = sharedAssets.app.screenWidth

    i = i % matrixRows

    padding = per(sw, marginPer)

    sectionWidth = per(sw, sectionWidthPer + marginPer)

    return padding + (sectionWidth * i)

  def getSectionY(i: int):
    nonlocal per, sectionWidthPer, sectionHeightPer, marginPer, matrixRows

    sh = sharedAssets.app.screenHeight

    sw = sharedAssets.app.screenWidth

    i = int(i / matrixRows)

    padding = per(sh, 10)

    sectionHeight = per(sw, sectionHeightPer) + per(sw, marginPer)

    return padding + (sectionHeight * i)

  cards = {}
  for i in range(HOME_CARDS_DATA['len']):
    # title = HOME_CARDS_DATA['titles'][i]

    back = pg.Surface((sectionWidthPer * 30, sectionHeightPer * 30), pg.SRCALPHA)

    back.fill(pg.Color(100, 100, 100, 64))

    icon = pgx.Util.ImgManipulation.fit(icons[i], back.get_size(), True)

    back.blit(icon)

    sectionCard = pgx.Section(
      {
        'x': pgx.DynamicValue(getSectionX, args={'i': i}),
        'y': pgx.DynamicValue(getSectionY, args={'i': i}),
        'width': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=sectionWidthPer),
        'height': pgx.DynamicValue(sharedAssets.app, 'screenWidth', percent=sectionHeightPer)
      }, back, 10
    )

    cards[HOME_CARDS_DATA['iconNames'][i]] = sectionCard

  return cards

def addHome() -> bool:
  window = sharedAssets.app

  if 'home' in window.systems:
    return False

  home = pgx.System(preLoadState=True)

  homeBG = pgx.Section(
    {
      'x': pgx.DynamicValue(0),
      'y': pgx.DynamicValue(0),
      'width': pgx.DynamicValue(window, 'screenWidth'),
      'height': pgx.DynamicValue(window, 'screenHeight')
    }, pg.Color(20, 10, 20)
  )

  opTitleStart = pgx.DynamicValue(window, 'screenHeight')
  opTitleEnd = pgx.DynamicValue(window, 'screenHeight', percent=20)

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
        'x': pgx.DynamicValue(0),
        'y': pgx.DynamicValue(0),
        'width': pgx.DynamicValue(window, 'screenWidth'),
        'height': pgx.DynamicValue(openingAnim, 'value')
      }, pg.Color(20, 10, 20), 8
    ),
    'HVision',
    'Resources/Fonts/thicccboi/fonts/TTF/THICCCBOI-Bold.ttf',
    pg.Color(100, 100, 100, 100),
    pgx.DynamicValue(50)
  )

  HVisionText.lazyUpdate = False

  cards = getSectionCards()

  def triggetOPIntro():
    nonlocal openingAnim

    openingAnim.trigger(delay=500)

  window.customData['triggetOPIntroFunc'] = triggetOPIntro

  window.customAnimatedValues['openingAnim'] = openingAnim

  home.addElement(homeBG, 'homeBG')

  home.addElement(HVisionText, 'HVisionText')

  home.addElements(cards)

  window.addSystem(home, 'home')

  window.setSystemZ('home', 0)

  return True
