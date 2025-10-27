from bs4 import BeautifulSoup

def formatTextFromSoup(soup: BeautifulSoup) -> str:
  html = str(soup)

  html = html.replace("<br>", "\n").replace("<br/>", "\n")

  soup = BeautifulSoup(html, "html.parser")

  text = soup.get_text().strip()

  return text

def navigate(layout: list[list[str | int]], soupData: BeautifulSoup) -> list[str]:
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
          results.append(f'N/A : {step[1]} at index {step[2]}')
          return results

    elif step[0] == 'attr':
      try:
        results.append(soupData[step[1]])
      except:
        results.append(f'N/A : attribute {step[1]}')

    elif step[0] == 'text':
      try:
        results.append(formatTextFromSoup(soupData))
      except:
        results.append('N/A : text')

  return results
