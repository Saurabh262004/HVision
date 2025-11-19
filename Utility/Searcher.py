from typing import Any, Literal

class Searcher:
  # basic one-to-one comparison search nothing fancy
  @staticmethod
  def basicStrictSearch(items: list, findVal: Any) -> list:
    result = []

    for item in items:
      if item == findVal:
        result.append(item)

    return result

  # in the items list, look if the findVal exists in individual values if the value is a string else just compaire them directly
  @staticmethod
  def inclusiveStrSearch(items: list, findVal: str) -> list[str]:
    result = []

    for item in items:
      if (isinstance(item, str) and findVal in item) or (item == findVal):
        result.append(item)

    return result

  # just combines both the above + case sensitive search. only looks for keys in dicts.
  @staticmethod
  def flatSerialSearch(items: tuple | list | dict, findVal: Any, caseSensitiveSearch: bool = True, strictSearch: bool = True) -> list:
    if not caseSensitiveSearch:
      if isinstance(findVal, str):
        findVal = findVal.strip().lower()

      searchList = [item.lower() if isinstance(item, str) else item for item in items]

    else:
      searchList = [item for item in items]

    if strictSearch:
      return Searcher.basicStrictSearch(searchList, findVal)

    return Searcher.inclusiveStrSearch(searchList, findVal)

  # look for values in a dict and returs keys associated with those values
  @staticmethod
  def strictDictValSearch(items: dict, findVal: Any) -> list[str]:
    result = []

    for k, v in items.items():
      if v == findVal:
        result.append(k)

    return result

  # same as the above except if the value in dict is a string check if the findVal exists inside the value
  @staticmethod
  def inclusiveDictValStrSearch(items: dict[str, Any], findVal: str) -> list[str]:
    result = []

    for k, v in items.items():
      if (isinstance(v, str) and findVal in v) or (findVal == v):
        result.append(k)

    return result

  # look for keys and values in a dict
  type SEARCH_VAL_TYPE = list[str] | tuple[str] | Literal['all'] | None
  @staticmethod
  def shallowDictSearch(items: dict, findVal: Any, searchKeys: bool = True, searchValues: SEARCH_VAL_TYPE = None, caseSensitiveSearch: bool = True, strictSearch: bool = True) -> list[str]:
    result = []

    if not caseSensitiveSearch:
      if isinstance(findVal, str):
        findVal = findVal.strip().lower()

    if searchKeys:
      if not caseSensitiveSearch:
        searchList = [key.lower() for key in items]

      else:
        searchList = [key for key in items]

      if strictSearch:
        result = Searcher.basicStrictSearch(searchList, findVal)

      else:
        result = Searcher.inclusiveStrSearch(searchList, findVal)

    if searchValues is not None:
      searchList = []

      if not caseSensitiveSearch:
        if searchValues == 'all':
          searchDict = {}

          for k, v in items.items():
            if isinstance(v, str):
              searchDict[k] = v.lower()

            else:
              searchDict[k] = v

        else:
          searchDict = {}

          for k in searchValues:
            if k in items:
              if isinstance(items[k], str):
                searchDict[k] = items[k].lower()

              else:
                searchDict[k] = items[k]

      else:
        if searchValues == 'all':
          searchDict = {}

          for k, v in items.items():
            searchDict[k] = v

        else:
          searchDict = {}

          for k in searchValues:
            if k in items:
              searchDict[k] = items[k]

      if strictSearch:
        result = list(dict.fromkeys(result + Searcher.strictDictValSearch(searchDict, findVal)))
      else:
        result = list(dict.fromkeys(result + Searcher.inclusiveDictValStrSearch(searchDict, findVal)))

    return result
