import requests
import random
import time
import cloudscraper

# standard headers for all requests to mimic a real browser
HEADERS = {
	"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
				"(KHTML, like Gecko) Chrome/120.0.6099.224 Safari/537.36",
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Language": "en-US,en;q=0.9",
	"Accept-Encoding": "gzip, deflate",
	"Connection": "keep-alive",
	"Upgrade-Insecure-Requests": "1",
	"Referer": "https://www.google.com/",
}

# statuses worth retrying
RETRY_STATUSES = {
	429,  # too many requests
	502,  # bad gateway
	503,  # service unavailable
	504,  # gateway timeout
}

class Fetcher:
	@staticmethod
	def _get_session(session: cloudscraper.CloudScraper = None) -> cloudscraper.CloudScraper:
		return session or cloudscraper.create_scraper()

	@staticmethod
	def _stall(stall: float, deviation: float) -> float:
		delay = random.uniform(
			max(0.0, stall - deviation),
			stall + deviation
		)

		time.sleep(delay)

		return delay

	@staticmethod
	def _get(url: str, session: cloudscraper.CloudScraper, retries: int = 3, retry_delay: float = 5.0):
		for attempt in range(retries + 1):
			try:
				response = session.get(url, headers=HEADERS)
			except requests.exceptions.RequestException as e:
				if attempt >= retries:
					raise

				delay = retry_delay * (2 ** attempt)
				delay += random.uniform(0, 2)

				print(
					f"{type(e).__name__} from {url} "
					f"(attempt {attempt + 1}/{retries + 1}), "
					f"retrying in {delay:.2f}s..."
				)

				time.sleep(delay)
				continue

			if response.status_code not in RETRY_STATUSES:
				response.raise_for_status()
				return response

			# No retries left
			if attempt >= retries:
				response.raise_for_status()

			# Respect Retry-After when the server provides it
			retry_after = response.headers.get("Retry-After")

			if retry_after:
				try:
					delay = float(retry_after)
				except ValueError:
					delay = retry_delay * (2 ** attempt)
			else:
				delay = retry_delay * (2 ** attempt)
				delay += random.uniform(0, 2)

			print(
				f"{response.status_code} from {url} "
				f"(attempt {attempt + 1}/{retries + 1}), "
				f"retrying in {delay:.2f}s..."
			)

			time.sleep(delay)

		raise RuntimeError("Unreachable")

	@staticmethod
	def fetchText(url: str, session: cloudscraper.CloudScraper = None, retries: int = 3, retry_delay: float = 5.0) -> str:
		session = Fetcher._get_session(session)

		response = Fetcher._get(
			url,
			session,
			retries,
			retry_delay
		)

		return response.text

	@staticmethod
	def fetchTextBatch(
			manifest: dict[str, str],
			session: cloudscraper.CloudScraper = None,
			stall: float = 2.0,
			deviation: float = 0.5,
			retries: int = 3,
			retry_delay: float = 5.0,
		) -> list[dict[str, str], int]:

		session = Fetcher._get_session(session)

		responses = {}

		totalStall = 0

		for key, url in manifest.items():

			totalStall += Fetcher._stall(stall, deviation)

			responses[key] = Fetcher.fetchText(
				url,
				session,
				retries,
				retry_delay
			)

		return responses, int(totalStall*1000)

	@staticmethod
	def fetchContent(url: str, session: cloudscraper.CloudScraper = None, retries: int = 3, retry_delay: float = 5.0) -> bytes:
		session = Fetcher._get_session(session)

		response = Fetcher._get(
			url,
			session,
			retries,
			retry_delay
		)

		return response.content

	@staticmethod
	def fetchContentBatch(
			manifest: dict[str, str],
			session: cloudscraper.CloudScraper = None,
			stall: float = 2.0,
			deviation: float = 0.5,
			retries: int = 3,
			retry_delay: float = 5.0,
		) -> list[dict[str, bytes], int]:

		session = Fetcher._get_session(session)

		responses = {}

		totalStall = 0

		for key, url in manifest.items():

			totalStall += Fetcher._stall(stall, deviation)

			responses[key] = Fetcher.fetchContent(
				url,
				session,
				retries,
				retry_delay
			)

		return responses, int(totalStall*1000)
