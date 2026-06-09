from DBManagers.CustomScrapers import GenshinScraper, ZenlessScraper, StarRailScraper
import time

def getData() -> list:
	genshinData, genshinFetchTime, genshinProcessTime, genshinStallTime = GenshinScraper.getData()
	time.sleep(2)
	zenlessData, zenlessFetchTime, zenlessProcessTime, zenlessStallTime = ZenlessScraper.getData()
	time.sleep(2)
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

	return scrapedData, fetchTime, processTime, stallTime
