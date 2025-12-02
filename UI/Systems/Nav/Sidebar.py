import pygame as pg
import pg_extended as pgx
from UI import SystemSwitch
import sharedAssets

BTN_INFO = (
  {
    'title': 'HVision',
    'bg': None,
    'textSize': 10,
    'systems': ['Nav', 'Home']
  },
  {
    'title': 'Genshin',
    'bg': None,
    'textSize': 10,
    'systems': ['Nav', 'GCDBList', 'GCDBFilters', 'GINav']
  },
)

def getBTNY(container: pgx.Section, index: int) -> int | float:
  per = lambda n, p: n / 100 * p

  margin = per(container.width, 10)

  btnH = per(container.width, 80)

  return margin + ((btnH + margin) * index)

def getBTN(container: pgx.Section, index: int) -> pgx.Button:
  global BTN_INFO

  btnS = pgx.DynamicValue(container, 'width', percent=80)

  btn = pgx.Button(
    pgx.TextBox(
      pgx.Section(
        {
          'x': pgx.DynamicValue(container, 'width', percent=10),
          'y': pgx.DynamicValue(getBTNY, args={'container': container, 'index': index}),
          'width': btnS,
          'height': btnS
        }, pg.Color(0, 0, 0)
      ), BTN_INFO[index]['title'], 'Arial', pg.Color(255, 255, 255), pgx.DynamicValue(btnS, percent=20)
    ),
    pgx.CallbackSet(
      (
        pgx.Callback(
          ('mouseUp',),
          SystemSwitch.switch,
          {
            'systems': BTN_INFO[index]['systems']
          }
        ),
      )
    )
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
      'x': 0,
      'y': 0,
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
