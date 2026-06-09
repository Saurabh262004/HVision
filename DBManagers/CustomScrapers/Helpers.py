from orjson import loads
from Utility.Scrapers import Fetcher

def getFandomPageHTML(url: str) -> str:
	return loads(Fetcher.fetchContent(url))['parse']['text']['*']

def removeImageOptions(url: str) -> str:
	return url[:url.find('.png') + 4]

def safeAttr(func, default='Unknown') -> str | int:
	try:
		return func()
	except:
		return default
