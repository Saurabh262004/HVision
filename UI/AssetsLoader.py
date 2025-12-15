import time
from typing import Iterable
import os
import pygame as pg
import pg_extended as pgx
from Utility import Sanitizer
import SharedAssets

def getIcon(path: str) -> pg.Surface | pg.Color:
  try:
    icon = pg.image.load(path).convert_alpha()
  except Exception as e:
    print(f'Failed to load image from "{path}":\n- {e}')
    icon = pg.Surface((64, 64), pg.SRCALPHA)
    icon.fill((255, 0, 64, 128))

  return icon

def getCustomAssets() -> dict[str, pg.Surface]:
  imageDBLocation = SharedAssets.config['ImageDBLocation']

  customAssets = {}

  customAssets['Genshin_RarityStar'] = getIcon(
    os.path.join(
      imageDBLocation,
      'Genshin_RarityStar'
    )
  )

  customAssets['Genshin_Region_Unknown'] = getIcon(
    os.path.join(
      imageDBLocation,
      'Genshin_Region_Unknown'
    )
  )

  rarityStarWidth, rarityStarHeight = customAssets['Genshin_RarityStar'].get_size()

  customAssets['Genshin_RarityStar_4'] = pg.Surface(
    (4 * rarityStarWidth, rarityStarHeight),
    pg.SRCALPHA
  )

  customAssets['Genshin_RarityStar_5'] = pg.Surface(
    (5 * rarityStarWidth, rarityStarHeight),
    pg.SRCALPHA
  )

  for i in range(5):
    if i < 4:
      customAssets['Genshin_RarityStar_4'].blit(customAssets['Genshin_RarityStar'], (i * rarityStarWidth, 0))

    customAssets['Genshin_RarityStar_5'].blit(customAssets['Genshin_RarityStar'], (i * rarityStarWidth, 0))

  customAssets['Genshin_RarityBack_4'] = pgx.ImgManipulation.getGradient(
    [(141, 22, 245), (50, 50, 50)],
    [1, 5],
    'right'
  )

  customAssets['Genshin_RarityBack_5'] = pgx.ImgManipulation.getGradient(
    [(245, 200, 39), (50, 50, 50)],
    [1, 5],
    'right'
  )

  return customAssets

def loadAssets(assetNames: Iterable[str] = None, loadCustoms: bool = True):
  startTime = time.time()

  print('loading assets...')

  customAssetsLoaded = 0

  if assetNames is None:
    assetNames = SharedAssets.db['ImageCollectorManifest']

  if isinstance(assetNames, dict):
    assetNames = assetNames.keys()
  elif isinstance(assetNames, tuple):
    assetNames = list(assetNames)

  if loadCustoms:
    customAssets = getCustomAssets()

    SharedAssets.dbAssets.update(customAssets)

    customAssetsLoaded += len(customAssets)

  imageDBLocation = SharedAssets.config['ImageDBLocation']

  for assetName in assetNames:
    OSProofName = Sanitizer.OSProofName(assetName)

    SharedAssets.dbAssets[assetName] = getIcon(
      os.path.join(
        imageDBLocation,
        OSProofName
      )
    )

  print(f'Loaded {customAssetsLoaded + len(assetNames)} assets in {(time.time() - startTime):.4f}s.')
