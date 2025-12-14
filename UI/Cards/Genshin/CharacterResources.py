import os
import pygame as pg
import pg_extended as pgx
from Utility import Sanitizer

class CharacterResources:
  @staticmethod
  def getIcon(path: str) -> pg.Surface | pg.Color:
    try:
      icon = pg.image.load(path).convert_alpha()
    except Exception as e:
      print(f'Failed to load image from "{path}": {e}')
      icon = pg.Surface((64, 64), pg.SRCALPHA)
      icon.fill((255, 0, 64, 128))

    return icon

  @staticmethod
  def getBasicResources(imageDBPath: str) -> dict[str, pg.Surface]:
    basicIcons: dict[str, pg.Surface] = {
      'RarityStar': None,
      'WeaponClass_Sword': None,
      'WeaponClass_Polearm': None,
      'WeaponClass_Bow': None,
      'WeaponClass_Catalyst': None,
      'WeaponClass_Claymore': None,
      'Element_Anemo': None,
      'Element_Geo': None,
      'Element_Electro': None,
      'Element_Dendro': None,
      'Element_Hydro': None,
      'Element_Pyro': None,
      'Element_Cryo': None,
      'Nation_Emblem_Mondstadt': None,
      'Nation_Emblem_Liyue': None,
      'Nation_Emblem_Inazuma': None,
      'Nation_Emblem_Sumeru': None,
      'Nation_Emblem_Fontaine': None,
      'Nation_Emblem_Natlan': None,
      'Nation_Emblem_Nod-Krai': None,
      'Nation_Emblem_Unknown': None
    }

    for iconKey in basicIcons:
      basicIcons[iconKey] = CharacterResources.getIcon(
        os.path.join(
          imageDBPath,
          f'Genshin{iconKey}'
        )
      )

    rarityStarWidth, rarityStarHeight = basicIcons['RarityStar'].get_size()

    basicIcons['RarityStars4'] = pg.Surface(
      (4 * rarityStarWidth, rarityStarHeight),
      pg.SRCALPHA
    )

    basicIcons['RarityStars5'] = pg.Surface(
      (5 * rarityStarWidth, rarityStarHeight),
      pg.SRCALPHA
    )

    for i in range(5):
      if i < 4:
        basicIcons['RarityStars4'].blit(basicIcons['RarityStar'], (i * rarityStarWidth, 0))

      basicIcons['RarityStars5'].blit(basicIcons['RarityStar'], (i * rarityStarWidth, 0))

    basicIcons['RarityBack4'] = pgx.ImgManipulation.getGradient(
      [(141, 22, 245), (50, 50, 50)],
      [1, 5],
      'right'
    )

    basicIcons['RarityBack5'] = pgx.ImgManipulation.getGradient(
      [(245, 200, 39), (50, 50, 50)],
      [1, 5],
      'right'
    )

    return basicIcons

  @staticmethod
  def getCharacterIcons(characters: list[str], imageDBPath: str) -> dict[str, pg.Surface]:
    icons = {}

    for character in characters:
      icons[character] = CharacterResources.getIcon(
        os.path.join(
          imageDBPath,
          f'GenshinCharacter{Sanitizer.OSProofName(character)}'
        )
      )

    return icons
