from typing import List
from time import sleep
import os
import json
import requests
from bs4 import BeautifulSoup
from Network import navigate

def scrapeLayouts(layoutSources: List[str]):
  scrapedData = []

  for layoutSRC in layoutSources:

    if not os.path.isfile(layoutSRC):
      pass

    with open(layoutSRC, 'r') as layoutFile:
      layoutData = json.load(layoutFile)

      for pageKey in layoutData:
        page = layoutData[pageKey]

        sleep(2)

        url = page['URL']

        del page['URL']

        response = requests.get(url)

        if not (response.status_code == 200):
          print(f'Error with URL: {url}\nError code: {response.status_code}')
          continue

        soup = BeautifulSoup(response.text, 'html.parser')

        scrapedData[pageKey] = {}

        for layoutKey in page:
          layout = page[layoutKey]

          scrapedData[pageKey][layoutKey] = {
            "source": url,
            "data": navigate(layout, soup)
          }

  return scrapedData
