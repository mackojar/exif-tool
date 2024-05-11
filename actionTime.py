import logging
from datetime import datetime, timedelta
from exif import Image, DATETIME_STR_FORMAT

ACTION_TIME_ADD = 'timeAdd'
ACTION_TIME_SUB = 'timeSub'

def isEligible(action: str):
  return action in [ACTION_TIME_ADD, ACTION_TIME_SUB]

class ActionTime:

  def __init__(self, args: any):
    timeDelta = timedelta(hours=args.hours, minutes=args.minutes)
    if args.action == ACTION_TIME_SUB:
      timeDelta = -timeDelta
    self.__timeDelta = timeDelta
    logging.info("Delta: %s", str(self.__timeDelta))

  def __processExif(self, imageExif: Image) -> Image:
    logging.debug("Original Datetime: %s", imageExif.datetime)
    logging.debug("Original DatetimeDigitized: %s", imageExif.datetime_digitized)
    logging.debug("Original DatetimeOriginal: %s", imageExif.datetime_original)

    datetimeOriginal = datetime.strptime(imageExif.datetime_original, DATETIME_STR_FORMAT)
    newDatetime = datetimeOriginal + self.__timeDelta
    newDatetimeFormatted = newDatetime.strftime(DATETIME_STR_FORMAT)

    imageExif.datetime_original = newDatetimeFormatted
    imageExif.datetime_digitized = newDatetimeFormatted
    imageExif.datetime = newDatetimeFormatted

    logging.debug("Updated Datetime: %s", imageExif.datetime)
    logging.debug("Updated DatetimeDigitized: %s", imageExif.datetime_digitized)
    logging.debug("Updated DatetimeOriginal: %s", imageExif.datetime_original)
    return imageExif

  def processAction(self, fileName: str):
    logging.info("Process file: %s...", fileName)
    with open(fileName, 'rb+') as imageFile:
      imageExif = Image(imageFile)
      if not imageExif.has_exif:
        logging.error("Image %s does not include EXIF tags", fileName)
      else:
        imageExif = self.__processExif(imageExif)
        imageFile.seek(0)
        imageFile.write(imageExif.get_file())
        logging.info("File %s updated", fileName)
