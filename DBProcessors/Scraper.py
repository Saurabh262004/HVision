from time import sleep
import os
import orjson
import requests
from bs4 import BeautifulSoup
from DBProcessors import navigate

def scrapeLayouts(layoutSources: list[str]):
  scrapedData = {}
  failedURLs = []

  for layoutSRC in layoutSources:

    if not os.path.isfile(layoutSRC):
      print(f'Layout file: "{layoutSRC}" does not exist')
      continue

    print(f'Scraping layout file "{layoutSRC}"...')

    with open(layoutSRC, 'rb') as layoutFile:
      try:
        layoutData = orjson.loads(layoutFile.read())
      except Exception as e:
        print(f'Failed to parse json data form file: "{layoutSRC}"\n{e}')
        continue

      pageCount = 0

      for pageKey in layoutData:
        page = layoutData[pageKey]

        url = page['URL']

        del page['URL']

        print(f'Requesting page: "{url}"')

        try:
          response = requests.get(url)
        except Exception as e:
          print(f'Failed to get request for URL: "{url}"\n{e}')
          continue

        if not (response.status_code == 200):
          print(f'Error with URL: "{url}"\nError code: {response.status_code}')

          failedURLs.append(url)

          continue

        soup = BeautifulSoup(response.text, 'html.parser')

        scrapedData[pageKey] = {}

        print(f'Extracting {len(page)} layouts from the page')

        for layoutKey in page:
          layout = page[layoutKey]

          scrapedData[pageKey][layoutKey] = {
            "source": url,
            "data": navigate(layout, soup)
          }

        print(f'Extraction successful')

        if pageCount < len(layoutData) - 1:
          print('waiting for 2 seconds before next request')
          sleep(2)

        pageCount += 1

  return scrapedData, failedURLs
