import pygame as pg
import pg_extended as pgx
import sharedAssets

BTN_INFO = (
  {'title': 'HVision', 'bg': None, 'textSize': 10},
)

def getBTNY(container: pgx.Section, index: int) -> int | float:
  per = lambda n, p: n / 100 * p

  margin = per(container.height, 5)

  btnH = per(container.width, 80)

  return margin + ((btnH + margin) * index)

def getBTN(container: pgx.Section, index: int) -> pgx.Button:
  global BTN_INFO

  btnS = pgx.DynamicValue(container, 'width', percent=80)

  btn = pgx.Button(
    pgx.Section(
      {
        'x': pgx.DynamicValue(container, 'width', percent=20),
        'y': pgx.DynamicValue(getBTNY, args={'container': container, 'index': index}),
        'width': btnS,
        'height': btnS
      }, pg.Color(0, 0, 0)
    ), text=BTN_INFO[index]['title'], fontPath='Arial', textColor=pg.Color(255, 255, 255),
    callback=pgx.CallbackSet((
      pgx.Callback(
        'mouseUp',
        print,
        {'*values': 'hello?'}
      ),
    ))
  )

  return btn

def getBTNs(container: pgx.Section) -> dict[str, pgx.Button]:
  global BTN_INFO

  BTNCollection = {}

  for i in range(len(BTN_INFO)):
    BTNCollection[BTN_INFO[i]['title']] = getBTN(container, i)

  return BTNCollection

def addSystem():
  window: pgx.Window = sharedAssets.app

  system = pgx.System(preLoadState=True)

  bg = pgx.Section(
    {
      'x': pgx.DynamicValue(0),
      'y': pgx.DynamicValue(0),
      'width': pgx.DynamicValue(window, 'screenWidth', percent=7),
      'height': pgx.DynamicValue(window, 'screenHeight')
    },
    pgx.ImgManipulation.getGradient(
      [
        (255, 255, 255, 32),
        (0, 0, 0)
      ],
      [20, 1],
      'right'
    ),
    backgroundSizeType='squish'
  )

  elements = getBTNs(bg)

  elements.update({'bg': bg})

  system.addElements(elements)

  window.addSystem(system, 'Nav')

  window.setSystemZ('Nav', 999)
