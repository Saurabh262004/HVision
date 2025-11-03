class Searcher:
  @staticmethod
  def search(items: tuple[str] | list[str], findVal: str) -> list:
    foundList = []

    findVal = findVal.lower()

    for item in items:
      if findVal in item.lower():
        foundList.append(item)

    return foundList
