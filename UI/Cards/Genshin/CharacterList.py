import pg_extended as pgx
from UI.Cards.Genshin.CharacterResources import CharacterResources
from UI.Cards.Genshin.CharacterBase import CharacterBase
from Utility import Searcher
import sharedAssets

class CharacterList:
  def __init__(self, cardDim: dict[str, pgx.DynamicValue], maxListLength: int, padding: pgx.DynamicValue, lazyCards: bool = True):
    self.cardDim = cardDim
    self.lazyCards = lazyCards
    self.maxListLength = maxListLength
    self.padding = padding

    self.characters: list[str] = []

    self.filters: tuple[str] = (
      'Rarity',
      'Element',
      'WeaponClass',
      'Region',
      'Model'
    )

    self.activeFilters: dict[str, list[str]] = {
      'Rarity': [],
      'Element': [],
      'WeaponClass': [],
      'Region': [],
      'Model': []
    }

    self.activeList: list[str] = []

    self.listCards: list[dict[str, pgx.UIElement]] = []

    self.listPosition: int = 0

    self.imageDBPath = sharedAssets.config['ImageDBLocation']

    self.basicAssets = CharacterResources.getBasicResources(self.imageDBPath)

    for char in sharedAssets.db['GenshinImpact']['Items']['Characters']:
      self.characters.append(char)

    self.characterIcons = CharacterResources.getCharacterIcons(self.characters, self.imageDBPath)

    def getDimY(i):
      self.padding.resolveValue()
      return self.cardDim['y'].value + ((self.cardDim['height'].value + self.padding.value) * i)

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

  def activateFilters(self, filterType: str, filterData: str | list[str] | tuple[str]) -> bool:
    if filterType not in self.filters:
      return False

    if isinstance(filterData, (str)):
      filterData = (filterData,)

    for data in filterData:
      if not filterData in self.activeFilters[filterType]:
        self.activeFilters[filterType].append(data)

    return True

  def deactivateFilters(self, filterType: str, filterData: str | list[str] | tuple[str]) -> bool:
    if filterType not in self.filters:
      return False

    if isinstance(filterData, str):
      filterData = (filterData,)

    for data in filterData:
      if data in self.activeFilters[filterType]:
        self.activeFilters[filterType].remove(data)

    return True

  def deactivateFiltersAll(self):
    for filterType in self.activeFilters:
      self.activeFilters[filterType] = []

  def getFilteredChars(self) -> dict[str, dict[str, str]]:
    charDicts = sharedAssets.db['GenshinImpact']['Items']['Characters']

    activeFiltersCount = 0

    for filterType in self.activeFilters:
      activeFiltersCount += len(self.activeFilters[filterType])

    if activeFiltersCount == 0:
      return charDicts

    multipleFilterMatches = []

    for filterType in self.activeFilters:
      if len(self.activeFilters[filterType]) == 0:
        continue

      singleFilterMatches = []

      for filterData in self.activeFilters[filterType]:
        for charName, charData in charDicts.items():
          if (charData[filterType] == filterData) and (charName not in singleFilterMatches):
            singleFilterMatches.append(charName)

      multipleFilterMatches.append(singleFilterMatches)

    results = {}

    for char in charDicts:
      addChar = True

      for singleFilterMatches in multipleFilterMatches:
        if char not in singleFilterMatches:
          addChar = False

      if addChar:
        results[char] = charDicts[char]

    return results

  def displaySearchName(self, searchInput: str):
    foundChars = Searcher.flatSerialSearch(self.characters, searchInput, True, False, returnIndices=False)
    self.displayCharacters(foundChars)

  def displaySearchAll(self, searchInput: str):
    filterdDict = self.getFilteredChars()

    searchResult = Searcher.recursiveIterableSearch(
      filterdDict,
      searchInput,
      False,
      'all',
      False,
      False
    )

    charList = []

    for accessPoints in searchResult:
      charList.append(accessPoints[0])

    self.displayCharacters(charList)
