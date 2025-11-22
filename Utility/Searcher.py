from typing import Any, Literal

class Searcher:
  # basic one-to-one comparison search nothing fancy
  @staticmethod
  def basicStrictSearch(items: list, findVal: Any, returnIndices: bool = True) -> list[Any]:
    findVal = str(findVal).strip()

    if returnIndices:
      return [
        i for i, item in enumerate(items)
        if (isinstance(item, str) and item.strip() == findVal) or (item == findVal)
      ]

    return [
      item for item in items
      if (isinstance(item, str) and item.strip() == findVal) or (item == findVal)
    ]

  # in the items list, look if the findVal exists in individual values if the value is a string else just compaire them directly
  @staticmethod
  def inclusiveSearch(items: list, findVal: str, returnIndices: bool = True) -> list[Any]:
    findVal = str(findVal).strip()

    if returnIndices:
      return [
        i for i, item in enumerate(items)
        if (isinstance(item, str) and findVal in item) or (findVal == item)
      ]

    return [
      item for item in items
      if (isinstance(item, str) and findVal in item) or (findVal == item)
    ]

  # basic strict search - just non case sensitive
  @staticmethod
  def ncsStrictSearch(items: list, findVal: str, returnIndices: bool = True) -> list[Any]:
    findVal = str(findVal).strip().lower()

    if returnIndices:
      return [
        i for i, item in enumerate(items)
        if isinstance(item, str) and findVal == item.strip().lower()
      ]

    return [
      item for item in items
      if isinstance(item, str) and findVal == item.strip().lower()
    ]

  # inclusive search - just non case sensitive
  @staticmethod
  def ncsInclusiveSearch(items: list, findVal: str, returnIndices: bool = True) -> list[Any]:
    findVal = str(findVal).strip().lower()

    if returnIndices:
      return [
        i for i, item in enumerate(items)
        if (isinstance(item, str) and findVal in item.lower()) or findVal == str(item).strip().lower()
      ]

    return [
      item for item in items
      if (isinstance(item, str) and findVal in item.lower()) or findVal == str(item).strip().lower()
    ]

  # just combines the above four searches into one
  @staticmethod
  def flatSerialSearch(items: tuple | list | dict, findVal: Any, caseSensitiveSearch: bool = True, strictSearch: bool = True, dictSearchMode: Literal['keys', 'values'] = 'values', returnIndices: bool = True) -> list[Any]:
    if isinstance(items, dict):
      if dictSearchMode == 'keys':
        items = list(items.keys())
      elif dictSearchMode == 'values':
        items = list(items.values())
      else:
        raise ValueError(f'Invalid dictSearchMode: {dictSearchMode}. Please provide either \'keys\' or \'values\'')

    if caseSensitiveSearch:
      if strictSearch:
        return Searcher.basicStrictSearch(items, findVal, returnIndices)
      return Searcher.inclusiveSearch(items, findVal, returnIndices)
    if strictSearch:
      return Searcher.ncsStrictSearch(items, findVal, returnIndices)
    return Searcher.ncsInclusiveSearch(items, findVal, returnIndices)

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
      if (isinstance(v, str) and findVal in v) or (findVal == v)
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
      if (isinstance(v, str) and findVal in v.lower()) or (findVal == v)
    ]

  # look for keys and values in a dict. only returns keys
  @staticmethod
  def shallowDictSearch(
        items: dict,
        findVal: Any,
        searchKeys: bool = True,
        searchValuesAtKeys: list[str] | tuple[str] | Literal['all'] | None = None,
        caseSensitiveSearch: bool = True,
        strictSearch: bool = True
      ) -> list[str]:

    results = []

    if searchKeys:
      results = Searcher.flatSerialSearch(items, findVal, caseSensitiveSearch, strictSearch, 'keys', False)

    if searchValuesAtKeys is not None:
      if searchValuesAtKeys  == 'all':
        lookupDict = items
      else:
        lookupDict = {}

        for key in searchValuesAtKeys:
          if key in items:
            lookupDict[key] = items[key]

      if caseSensitiveSearch:
        if strictSearch:
          results.extend(list(dict.fromkeys(Searcher.strictDictValSearch(lookupDict, findVal))))
        else:
          results.extend(list(dict.fromkeys(Searcher.inclusiveDictValStrSearch(lookupDict, findVal))))
      else:
        if strictSearch:
          results.extend(list(dict.fromkeys(Searcher.ncsStrictDictValSearch(lookupDict, findVal))))
        else:
          results.extend(list(dict.fromkeys(Searcher.ncsInclusiveDictValSearch(lookupDict, findVal))))

    deDuped = []

    for result in results:
      if result not in deDuped:
        deDuped.append(result)

    return deDuped

  # idk just throw whatever you want at this and it'll do some magic and find your shit. only gives access points (indices for lists/tuples and keys for dicts)
  @staticmethod
  def recursiveIterableSearch(
        items: list | tuple | dict,
        findVal: Any,
        searchDictKeys: bool = True,
        searchValuesAtKeys: list[str] | tuple[str] | Literal['all'] | None = None,
        caseSensitiveSearch: bool = True,
        strictSearch: bool = True,
        maxDepth: int = 5
      ):

    result = []

    if isinstance(items, dict):
      if searchDictKeys:
        matches = Searcher.flatSerialSearch(
          items,
          findVal,
          caseSensitiveSearch,
          strictSearch,
          'keys',
          False
        )
        
        for match in matches:
          result.append([match])

      if searchValuesAtKeys is not None:
        matches = Searcher.shallowDictSearch(
          items,
          findVal,
          False,
          searchValuesAtKeys,
          caseSensitiveSearch,
          strictSearch
        )

        for match in matches:
          result.append([match])

      for k, v in items.items():
        if isinstance(v, (list, tuple, dict)) and maxDepth > 0:
          matches = Searcher.recursiveIterableSearch(
            v,
            findVal,
            searchDictKeys,
            searchValuesAtKeys,
            caseSensitiveSearch,
            strictSearch,
            maxDepth-1
          )

          if len(matches) > 0:
            result.append([k])
            result[-1].append(matches)

    elif isinstance(items, (list, tuple)):
      deepSearches = []

      if maxDepth > 0:
        for i in range(len(items)):
          if isinstance(items[i], (list, tuple, dict)):
            deepSearches.append(i)

      if not len(deepSearches) == len(items):
        matches = Searcher.flatSerialSearch(
          items,
          findVal,
          caseSensitiveSearch,
          strictSearch
        )

        for match in matches:
          result.append([match])

      for i in deepSearches:
        matches = Searcher.recursiveIterableSearch(
          items[i],
          findVal,
          searchDictKeys,
          searchValuesAtKeys,
          caseSensitiveSearch,
          strictSearch,
          maxDepth-1
        )

        if len(matches) > 0:
          result.append([i])
          result[-1].append(matches)

    return result
