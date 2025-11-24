import pg_extended as pgx
import sharedAssets

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

  system.addElements({
    'bg': bg
  })

  window.addSystem(system, 'Nav')

  window.setSystemZ('Nav', 999)
