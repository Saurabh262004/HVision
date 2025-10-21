from bs4 import BeautifulSoup
from typing import List, Union

def navigate(layout: List[List[Union[str, int]]], soupData: BeautifulSoup) -> List[str]:
  results = []

  for i in range(len(layout)):
    step = layout[i]

    if step[0] == 'tag':
      if step[2] == '~':
        elements = soupData.find_all(step[1])
        partialLayout = layout[i+1:]

        for element in elements:
          results.extend(navigate(partialLayout, element))

        return results

      else:
        try:
          soupData = soupData.find_all(step[1])[step[2]]
        except:
          results.append('N/A')
          return results

    elif step[0] == 'attr':
      try:
        results.append(soupData[step[1]])
      except:
        results.append('N/A')

    elif step[0] == 'text':
      try:
        results.append(soupData.get_text())
      except:
        results.append('N/A')

  return results
