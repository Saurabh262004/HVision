import requests
import os
import time
from Utility import Sanitizer

def saveImage(url: str, location: str, imageName: str, session: requests.Session = None) -> bool:
  if not os.path.isdir(location):
    os.makedirs(location)

  imagePath = os.path.join(location, Sanitizer.OSProofName(imageName))

  print(f'Collecting image from URL: "{url}"...')

  try:
    if session:
      response = session.get(url)
    else:
      response = requests.get(url)
  except Exception as e:
    print(f'Failed request. Error: {e}')
    return False

  if not response.status_code == 200:
    print(f'Failed. response status code: {response.status_code}')
    return False

  with open(imagePath, 'wb') as imageFile:
    imageFile.write(response.content)

  print(f'Saved the image at: "{imagePath}"')
  return True

def saveImagesBulk(manifest: dict, location: str) -> dict:
  failedImages = {}

  session = requests.Session()

  imageCount = 0
  for imageName in manifest:
    imageURL = manifest[imageName]

    success = saveImage(imageURL, location, imageName, session)

    if imageCount < len(manifest) - 1:
      time.sleep(2)

    imageCount += 1

    if not success:
      failedImages[imageName] = imageURL

  return failedImages

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
  startTime = time.time()

  manifest = checkDBStatus(imageDBLocation, manifest)

  if len(manifest) == 0:
    print('Image Database is already up to date')
    return False

  print('Updating Image DataBase...')
  print('Expected time: ', len(manifest) * 2, ' seconds or more')

  saveImagesBulk(manifest, imageDBLocation)

  endTime = time.time()

  stallTime = len(manifest) * 2

  processingTime = endTime - (startTime - stallTime)

  print(f'Done updating Image DataBase in {processingTime:.2f}S. excluding {stallTime}S of stall time')

  return True
