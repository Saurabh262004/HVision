import os
from Utility import Sanitizer, Misc
from Utility.Scrapers import ImageCollector

import SharedAssets

def checkDBStatus(imageDBLocation: str, manifest: dict, cacheBusterOld: dict = None, cacheBusterNew: dict = None) -> dict:
	if not os.path.exists(imageDBLocation):
		os.makedirs(imageDBLocation)

		return manifest

	updateManifest = {}

	# check for unavailable images
	for imageName in manifest:
		imagePath = os.path.join(imageDBLocation, Sanitizer.OSProofName(imageName))

		if not os.path.exists(imagePath):
			updateManifest[imageName] = manifest[imageName]

	if not (cacheBusterOld and cacheBusterNew):
		return updateManifest

	# check for updated images
	for cbImage in cacheBusterNew:
		cbOldVal = cacheBusterOld.get(cbImage, None)

		if not (cacheBusterNew[cbImage] == cbOldVal):
			updateManifest[cbImage] = manifest[cbImage]

	return updateManifest

def updateSingleImage(imageDBLocation: str, imageTitle: str, imageURL: str):
	ImageCollector.collectImage(imageURL, imageDBLocation, imageTitle)

def updateImageDB() -> bool:
	startTime = Misc.timeMS()

	imageDBLocation = SharedAssets.config.get('ImageDBLocation', None) if SharedAssets.db else None
	manifest = SharedAssets.db.get('ImageCollectorManifest', None) if SharedAssets.db else None
	cacheBusterOld = SharedAssets.oldDB.get('CacheBusters', None) if SharedAssets.oldDB else None
	cacheBusterNew = SharedAssets.db.get('CacheBusters', None) if SharedAssets.db else None

	if not (imageDBLocation or manifest):
		return False

	updateManifest = checkDBStatus(imageDBLocation, manifest, cacheBusterOld, cacheBusterNew)

	if len(updateManifest) == 0:
		print('Image Database is already up to date')
		return False

	print('Updating Image DataBase...')
	print('Expected time: ', len(updateManifest) * 2.5, ' seconds or more')

	stallTime = ImageCollector.collectBatch(updateManifest, imageDBLocation)

	endTime = Misc.timeMS()

	processingTime = endTime - (startTime - stallTime)

	print(f'Done updating Image DataBase in {processingTime}ms. excluding {stallTime/1000}s of stall time')

	return True
