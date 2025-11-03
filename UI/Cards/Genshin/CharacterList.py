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

    self.listCards: list[dict[str, pgx.UIElement]] = []

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
          'y': pgx.DynamicValue('callable', getDimY, i),
          'width': self.cardDim['width'],
          'height': self.cardDim['height']
        }

      self.listCards.append(CharacterBase.getCardBase(newCardDim, f'{str(i)}_'))

    self.deactivateCards('all')

  def setLazyCards(self, lazyUpdate: bool):
    for card in self.listCards:
      for elementKey in card:
        element = card[elementKey]
        element.lazyUpdate = lazyUpdate

  def setActiveCards(self, indices: list[int]):
    for index in indices:
      if index < 0 or index >= self.maxListLength:
        return False

      elements = self.listCards[index].values()

      for element in elements:
        element.active = True

  def deactivateCards(self, indices: list[int] | str):
    if indices == 'all':
      indices = range(self.maxListLength)

    for index in indices:
      if index < 0 or index >= self.maxListLength:
        return False

      elements = self.listCards[index].values()

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

    base[f'{index}_raritySection'].background = self.basicAssets[f'RarityStars{rarity}']

    base[f'{index}_raritySection'].backgroundSizePercent = (100 / 6) * rarity

    for elementKey in base:
      base[elementKey].update()

    return True

  def displayCharacters(self, characters: tuple[str] | list[str]):
    validChars = []

    for char in characters:
      if char in self.characters:
        validChars.append(char)

    totalCards = min(self.maxListLength, len(validChars))

    activeCards = range(totalCards)

    deactiveCards = range(totalCards, self.maxListLength)

    self.setActiveCards(activeCards)
    self.deactivateCards(deactiveCards)

    index = 0
    for char in validChars:
      if not self.applyCharacterToBase(char, index):
        continue

      index += 1

  def displaySearchName(self, searchInput: str):
    foundChars = Searcher.search(self.characters, searchInput)
    self.displayCharacters(foundChars)

  def displaySearchAll(self, searchInput: str):
    charDicts = sharedAssets.db['GenshinImpact']['Items']['Characters']

    foundChars = Searcher.seachDicts(charDicts, searchInput, True)

    self.displayCharacters(foundChars)
