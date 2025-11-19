from typing import Any, Literal

class Searcher:
  # basic one-to-one comparison search nothing fancy
  @staticmethod
  def basicStrictSearch(items: list, findVal: Any) -> list[Any]:
    findVal = str(findVal).strip()

    return [
      item for item in items
      if (isinstance(item, str) and item.strip() == findVal) or (item == findVal)
    ]

  # in the items list, look if the findVal exists in individual values if the value is a string else just compaire them directly
  @staticmethod
  def inclusiveSearch(items: list, findVal: str) -> list[Any]:
    findVal = str(findVal).strip()

    return [
      item for item in items
      if (isinstance(item, str) and findVal in item) or (findVal == item)
    ]

  # basic strict search - just non case sensitive
  @staticmethod
  def ncsStrictSearch(items: list, findVal: str) -> list[Any]:
    findVal = str(findVal).strip().lower()

    return [
      item for item in items
      if isinstance(item, str) and findVal == item.strip().lower()
    ]

  # inclusive search - just non case sensitive
  @staticmethod
  def ncsInclusiveSearch(items: list, findVal: str) -> list[Any]:
    findVal = str(findVal).strip().lower()

    return [
      item for item in items
      if (isinstance(item, str) and findVal in item.lower()) or findVal == str(item).strip().lower()
    ]

  # just combines the above four searches into one
  @staticmethod
  def flatSerialSearch(items: tuple | list | dict, findVal: Any, caseSensitiveSearch: bool = True, strictSearch: bool = True, dictSearchMode: Literal['keys', 'values'] = 'values') -> list[Any]:
    if isinstance(items, dict):
      if dictSearchMode == 'keys':
        items = list(items.keys())
      elif dictSearchMode == 'values':
        items = list(items.values())
      else:
        raise ValueError(f'Invalid dictSearchMode: {dictSearchMode}. Please provide either \'keys\' or \'values\'')

    if caseSensitiveSearch:
      if strictSearch:
        return Searcher.basicStrictSearch(items, findVal)
      return Searcher.inclusiveSearch(items, findVal)
    if strictSearch:
      return Searcher.ncsStrictSearch(items, findVal)
    return Searcher.ncsInclusiveSearch(items, findVal)

  # search for values in a dict and return the keys
  @staticmethod
  def strictDictValSearch(items: dict, findVal: Any) -> list[str]:
    return [
      k for k, v in items.items()
      if v == findVal
    ]

  # same as the above except if the value in dict is a string check if the findVal exists inside the value
  @staticmethod
  def inclusiveDictValStrSearch(items: dict[str, Any], findVal: str) -> list[str]:
    findVal = str(findVal).strip()

    return [
      k for k, v in items.items()
      if (isinstance(v, str) and findVal in v) or (findVal == v.strip())
    ]

  # same as strictDictValSearch except non case sensitive
  @staticmethod
  def ncsStrictDictValSearch(items: dict, findVal: str) -> list[str]:
    findVal = str(findVal).strip().lower()

    return [
      k for k, v in items.items()
      if isinstance(v, str) and findVal == v.strip().lower()
    ]

  # same as inclusiveDictValStrSearch except non case sensitive
  @staticmethod
  def ncsInclusiveDictValSearch(items: dict, findVal: str) -> list[str]:
    findVal = str(findVal).strip().lower()

    return [
      k for k, v in items.items()
      if (isinstance(v, str) and findVal in v.lower()) or (findVal == v.strip().lower())
    ]

  # look for keys and values in a dict. only returns keys
  @staticmethod
  def shallowDictSearch(
        items: dict,
        findVal: Any,
        searchKeys: bool = True,
        searchValues: list[str] | tuple[str] | Literal['all'] | None = None,
        caseSensitiveSearch: bool = True,
        strictSearch: bool = True
      ) -> list[str]:

    pass
