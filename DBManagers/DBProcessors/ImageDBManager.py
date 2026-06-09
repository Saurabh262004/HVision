import os
from Utility import Sanitizer, Misc
from Utility.Scrapers import ImageCollector

def checkDBStatus(imageDBLocation: str, manifest: dict) -> dict:
	if not os.path.exists(imageDBLocation):
		os.makedirs(imageDBLocation)

		return manifest

	unavailableImages = {}

	for imageName in manifest:
		imagePath = os.path.join(imageDBLocation, Sanitizer.OSProofName(imageName))

		if not os.path.exists(imagePath):
			unavailableImages[imageName] = manifest[imageName]

	return unavailableImages

def updateImageDB(imageDBLocation: str, manifest: dict) -> bool:
	startTime = Misc.timeMS()

	manifest = checkDBStatus(imageDBLocation, manifest)

	if len(manifest) == 0:
		print('Image Database is already up to date')
		return False

	print('Updating Image DataBase...')
	print('Expected time: ', len(manifest) * 2, ' seconds or more')

	ImageCollector.collectBatch(manifest, imageDBLocation)

	endTime = Misc.timeMS()

	stallTime = len(manifest) * 2

	processingTime = endTime - (startTime - stallTime)

	print(f'Done updating Image DataBase in {processingTime}ms. excluding {stallTime}S of stall time')

	return True
