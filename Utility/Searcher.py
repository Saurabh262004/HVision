class Searcher:
  @staticmethod
  def search(items: tuple[str] | list[str], findVal: str) -> list:
    foundList = []

    findVal = findVal.lower()

    for item in items:
      if findVal in item.lower():
        foundList.append(item)

    return foundList

  @staticmethod
  def seachDicts(items: dict[str, dict[str, str]], findVal: str, includeKeys: bool = False) -> list[str]:
    foundList = []

    findVal = findVal.lower()

    for k1 in items:
      item = items[k1]

      if includeKeys and (findVal in k1.lower()):
        foundList.append(k1)
        continue

      for k2 in item:
        if findVal in item[k2].lower():
          foundList.append(k1)
          break

    return foundList
