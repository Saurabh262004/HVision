import time
import socket
from Utility import Misc
from DBManagers.CustomScrapers import GamesScraper
from DBManagers.DBProcessors import DBPostProcessor

TESTING_CONNECTION_HOSTS = (
	('8.8.8.8', 53), # Google DNS
	('1.1.1.1', 53), # Cloudflare DNS
	('9.9.9.9', 53), # Quad9 DNS
	('208.67.222.222', 53), # OpenDNS
)

def checkInternetConnection(host: str = '8.8.8.8', port: int = 53, timeout: int = 5) -> bool:
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except Exception as ex:
		print(f'Internet connection check failed: {host}:{port}')
		print(f'Error: {ex}')
		return False

def ensureInternetConnection(timeout: int = 5) -> bool:
	for host, port in TESTING_CONNECTION_HOSTS:
		if checkInternetConnection(host, port, timeout):
			return True
	return False

def makeDB() -> tuple[dict, dict] | bool:
	print(f'Building database.')

	if not ensureInternetConnection():
		print('No internet connection available. Cannot proceed with database creation.')
		return False

	scrapedData, fetchTime, processTime, stallTime = GamesScraper.getData()

	start = Misc.timeMS()

	db = DBPostProcessor.processDB(scrapedData)

	postProcessTime = Misc.timeMS() - start

	totalTime = stallTime + fetchTime + processTime + postProcessTime

	db['_metadata_'] = {
		'creationEpoch': int(time.time()),
		'fetchTime': fetchTime,
		'processTime': processTime,
		'postProcessTime': postProcessTime,
		'stallTime': stallTime,
		'totalTime': totalTime,
		'safe': True
	}

	print(f'Done building Database in {totalTime}ms')
	print(f'Stall time: {stallTime}ms')
	print(f'Fetch time: {fetchTime}ms')
	print(f'Processing time: {processTime}ms')
	print(f'Post processing time: {postProcessTime}ms')

	return db, scrapedData
