from orjson import loads
from bs4 import BeautifulSoup, NavigableString
from Utility.Scrapers import Fetcher
import copy

def getFandomPageHTML(fandomName: str, page: str) -> str:
	return loads(Fetcher.fetchContent(
	f'https://{fandomName}.fandom.com/api.php?action=parse&page={page}&prop=text&format=json'
	))['parse']['text']['*']

def removeImageOptions(url: str) -> str:
	return url[:url.find('.png') + 4]

def safeAttr(fn: callable, default: str = 'Unknown'):
	try:
		return fn()
	except:
		return default

def extractInlineText(tag: BeautifulSoup) -> str:
	tag = copy.copy(tag)

	for br in tag.find_all('br'):
		br.replace_with('\n')

	lines = [line.strip() for line in tag.get_text().split('\n')]

	return ' '.join(line for line in lines if line)

def extractLeafText(tag: BeautifulSoup) -> str:
	tag = copy.copy(tag)

	for nested in tag.find_all(['ul', 'ol']):
		nested.decompose()

	return extractInlineText(tag)

def parseEffectList(listTag: BeautifulSoup) -> list[dict]:
	effects = []
	current = None

	for child in listTag.find_all(['li', 'ul', 'ol'], recursive=False):
		if child.name == 'li':
			effect = {'text': extractLeafText(child)}

			nested = child.find(['ul', 'ol'], recursive=False)
			if nested is not None:
				effect['subEffects'] = parseEffectList(nested)

			effects.append(effect)
			current = effect
		else:
			subEffects = parseEffectList(child)

			if current is not None:
				current.setdefault('subEffects', []).extend(subEffects)
			else:
				effects.extend(subEffects)

	return effects

def parsePassive(cell: BeautifulSoup) -> dict:
	body = copy.copy(cell)

	titleTag = body.find(['big', 'b'])
	title = titleTag.get_text(strip=True) if titleTag else ''
	if titleTag is not None:
		titleTag.decompose()

	firstBr = body.find('br')
	if firstBr is not None:
		firstBr.decompose()

	effects = []
	proseRun = BeautifulSoup('', 'html.parser').new_tag('div')

	def flushProse():
		text = extractInlineText(proseRun)
		proseRun.clear()
		if text:
			effects.append({'text': text})

	for child in list(body.contents):
		if getattr(child, 'name', None) in ('ul', 'ol'):
			flushProse()
			effects.extend(parseEffectList(child))
		else:
			proseRun.append(copy.copy(child))

	flushProse()

	return {'title': title, 'effects': effects}

def getStatLines(cell: BeautifulSoup) -> list[str]:
	tag = copy.copy(cell)
	for br in tag.find_all('br'):
		br.replace_with('\n')
	return [line.strip() for line in tag.get_text().split('\n') if line.strip()]

def getTitleIconPair(td: BeautifulSoup):
	try:
		elementA = td.find('a')
		title = elementA.get('title')
		icon = removeImageOptions(elementA.find('img').get('data-src'))
		return title, icon
	except:
		return 'N/A', 'Unknown'
