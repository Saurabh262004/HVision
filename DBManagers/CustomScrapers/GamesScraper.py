from DBManagers.CustomScrapers import GenshinScraper, ZenlessScraper, StarRailScraper
import time

def getData() -> list[dict, int, int, int]:
	print('getting Genshin data...')
	genshinData, genshinFetchTime, genshinProcessTime, genshinStallTime = GenshinScraper.getData()
	time.sleep(2)
	print('getting ZZZ data...')
	zenlessData, zenlessFetchTime, zenlessProcessTime, zenlessStallTime = ZenlessScraper.getData()
	time.sleep(2)
	print('getting HSR data...')
	starRailData, starRailFetchTime, starRailProcessTime, starRailStallTime = StarRailScraper.getData()

	fetchTime = genshinFetchTime + zenlessFetchTime + starRailFetchTime
	processTime = genshinProcessTime + zenlessProcessTime + starRailProcessTime
	stallTime = genshinStallTime + zenlessStallTime + starRailStallTime + 4000

	# group scraped data
	scrapedData = {
		'GenshinImpact': genshinData,
		'ZenlessZoneZero': zenlessData,
		'HonkaiStarRail': starRailData
	}

	return scrapedData, int(fetchTime), int(processTime), int(stallTime)
