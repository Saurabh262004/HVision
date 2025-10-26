from typing import List
from time import sleep
import os
import orjson
import requests
from bs4 import BeautifulSoup
from Network import navigate

def scrapeLayouts(layoutSources: List[str]):
  scrapedData = {}
  failedURLs = []

  for layoutSRC in layoutSources:

    if not os.path.isfile(layoutSRC):
      pass

    with open(layoutSRC, 'rb') as layoutFile:
      layoutData = orjson.loads(layoutFile.read())

      for i in range(len(layoutData)):
        pageKey = layoutData[i]

        page = layoutData[pageKey]

        url = page['URL']

        del page['URL']

        response = requests.get(url)

        if i != len(layoutData) - 1:
          sleep(2)

        if not (response.status_code == 200):
          print(f'Error with URL: {url}\nError code: {response.status_code}')

          failedURLs.append(url)

          continue

        soup = BeautifulSoup(response.text, 'html.parser')

        scrapedData[pageKey] = {}

        for layoutKey in page:
          layout = page[layoutKey]

          scrapedData[pageKey][layoutKey] = {
            "source": url,
            "data": navigate(layout, soup)
          }

  return scrapedData, failedURLs
