import logging
from datetime import datetime, timedelta
from exif import Image, DATETIME_STR_FORMAT

ACTION_TIME_ADD = 'timeAdd'
ACTION_TIME_SUB = 'timeSub'

def processImage(imageName: str, timeDelta: timedelta):
  logging.info("Process file: %s", imageName)
  with open(imageName, 'rb+') as imageFile:
    imageExif = Image(imageFile)
    if not imageExif.has_exif:
      logging.error("Image %s does not include EXIF tags", imageName)
    else:
      imageExif = processExif(imageExif, timeDelta)
      imageFile.seek(0)
      imageFile.write(imageExif.get_file())

def processExif(imageExif: Image, timeDelta: timedelta):
  logging.info("Datetime: %s", imageExif.datetime)
  logging.info("DatetimeDigitized: %s", imageExif.datetime_digitized)
  logging.info("DatetimeOriginal: %s", imageExif.datetime_original)

  datetimeOriginal = datetime.strptime(imageExif.datetime_original, DATETIME_STR_FORMAT)
  newDatetime = datetimeOriginal + timeDelta
  newDatetimeFormatted = newDatetime.strftime(DATETIME_STR_FORMAT)

  imageExif.datetime_original = newDatetimeFormatted
  imageExif.datetime_digitized = newDatetimeFormatted
  imageExif.datetime = newDatetimeFormatted

  logging.info("Datetime: %s", imageExif.datetime)
  logging.info("DatetimeDigitized: %s", imageExif.datetime_digitized)
  logging.info("DatetimeOriginal: %s", imageExif.datetime_original)
  return imageExif

def processAction(fileName: str, args: any):
  timeDelta = timedelta(hours=args.hours, minutes=args.minutes)
  if args.action == ACTION_TIME_SUB:
    timeDelta = -timeDelta
  logging.info("Delta: %s", str(timeDelta))

  # IMAGE_FILE = '/Users/mackoj/Pictures/toDVD/2024/05.new-york-2/DSCF9991.JPG'
  # IMAGE_FILE = '/Users/mackoj/Pictures/toDVD/2024/05.new-york-2/20240507_205058.jpg'
  processImage(fileName, timeDelta)

def isEligible(action: str):
  return action in [ACTION_TIME_ADD, ACTION_TIME_SUB]
