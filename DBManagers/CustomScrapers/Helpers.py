from orjson import loads
from Utility.Scrapers import Fetcher

def getFandomPageHTML(fandomName: str, page: str) -> str:
	return loads(Fetcher.fetchContent(
	f'https://{fandomName}.fandom.com/api.php?action=parse&page={page}&prop=text&format=json'
	))['parse']['text']['*']

def removeImageOptions(url: str) -> str:
	return url[:url.find('.png') + 4]
