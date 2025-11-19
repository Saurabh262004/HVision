import pg_extended as pgx
from UI.Cards.Genshin.CharacterResources import CharacterResources
from UI.Cards.Genshin.CharacterBase import CharacterBase
from Utility import Searcher
import sharedAssets

class CharacterList:
  def __init__(self, cardDim: dict[str, pgx.DynamicValue], callback: callable = None, callbackParams: list = None, lazyCards: bool = True, maxListLength: int = 5, padding: int = 5):
    self.cardDim = cardDim
    self.callback = callback
    self.callbackParams = callbackParams
    self.lazyCards = lazyCards
    self.maxListLength = maxListLength
    self.padding = padding

    self.characters: list[str] = []

    self.activeList: list[str] = []

    self.listCards: list[dict[str, pgx.UIElement]] = []

    self.listPosition: int = 0

    self.imageDBPath = sharedAssets.config['ImageDBLocation']

    self.basicAssets = CharacterResources.getBasicResources(self.imageDBPath)

    for char in sharedAssets.db['GenshinImpact']['Items']['Characters']:
      self.characters.append(char)

    self.characterIcons = CharacterResources.getCharacterIcons(self.characters, self.imageDBPath)

    def getDimY(i):
      return self.cardDim['y'].value + ((self.cardDim['height'].value + self.padding) * i)

    for i in range(self.maxListLength):
      if i == 0:
        newCardDim = self.cardDim
      else:
        newCardDim = {
          'x': self.cardDim['x'],
          'y': pgx.DynamicValue(getDimY, args={'i': i}),
          'width': self.cardDim['width'],
          'height': self.cardDim['height']
        }

      self.listCards.append(CharacterBase.getCardBase(newCardDim, f'{str(i)}_'))

    self.setActiveCards(0)

  def setLazyCards(self, lazyUpdate: bool):
    for card in self.listCards:
      for elementKey in card:
        element = card[elementKey]
        element.lazyUpdate = lazyUpdate

  def setActiveCards(self, length: int):
    for i in range(self.maxListLength):
      if i >= self.maxListLength:
        return None

      elements = self.listCards[i].values()

      if i < length:
        for element in elements:
          element.active = True
      else:
        for element in elements:
          element.active = False

  def applyCharacterToBase(self, character: str, index: int) -> bool:
    if character not in self.characters:
      return False

    if index < 0 or index >= self.maxListLength:
      return False

    characterDetails = sharedAssets.db['GenshinImpact']['Items']['Characters'][character]

    rarity = int(characterDetails['Rarity'][0])

    element = characterDetails['Element']

    weaponClass = characterDetails['WeaponClass']

    region = characterDetails['Region']

    if f'Nation_Emblem_{region}' not in self.basicAssets:
      region = 'Unknown'

    if rarity < 4 or rarity > 5:
      return False

    if 'N/A' in element or 'N/A' in weaponClass:
      return False

    base = self.listCards[index]

    base[f'{index}_cardSection'].defaultBackground = self.basicAssets[f'RarityBack{rarity}']

    base[f'{index}_cardSection'].section.background = self.basicAssets[f'RarityBack{rarity}']

    base[f'{index}_cardSection'].section.update()

    base[f'{index}_iconSection'].background = self.characterIcons[character]

    base[f'{index}_nameTextBox'].text = character

    base[f'{index}_elementSection'].background = self.basicAssets[f'Element_{element}']

    base[f'{index}_weaponTypeSection'].background = self.basicAssets[f'WeaponClass_{weaponClass}']

    base[f'{index}_nationSection'].background = self.basicAssets[f'Nation_Emblem_{region}']

    base[f'{index}_raritySection'].background = self.basicAssets[f'RarityStars{rarity}']

    base[f'{index}_raritySection'].backgroundSizePercent = (100 / 6) * rarity

    for elementKey in base:
      base[elementKey].update()

    return True

  def displayCharacters(self, characters: tuple[str] | list[str] | str):
    if characters == 'prev':
      pass
    elif characters == 'all':
      self.activeList = self.characters
    else:
      validChars = []

      for char in characters:
        if char in self.characters:
          validChars.append(char)

      self.activeList = validChars

    self.setActiveCards(self.maxListLength)

    totalActive = len(self.activeList)

    activatedCards = 0
    cardIndex = self.listPosition

    for _ in range(totalActive):
      if activatedCards >= self.maxListLength or cardIndex >= totalActive:
        break

      char = self.activeList[cardIndex]

      if not self.applyCharacterToBase(char, activatedCards):
        cardIndex += 1
        continue

      cardIndex += 1
      activatedCards += 1

    self.setActiveCards(activatedCards)

  def updateListPosition(self, listPosition: int = 0):
    self.listPosition = int(listPosition)
    self.displayCharacters('prev')

  def displaySearchName(self, searchInput: str):
    foundChars = Searcher.flatSerialSearch(self.characters, searchInput, True, False)
    self.displayCharacters(foundChars)

  def displaySearchAll(self, searchInput: str):
    charDicts = sharedAssets.db['GenshinImpact']['Items']['Characters']

    foundChars = Searcher.shallowDictSearch(charDicts, searchInput, True, None, False, False)

    self.displayCharacters(foundChars)
