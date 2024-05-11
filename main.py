import logging
import argparse
import actionTime
import glob

def main():
  parser = argparse.ArgumentParser(
                    prog='ExifTool',
                    description='Process EXIF data for given filenames: change datetime',
                    epilog='')
  parser.add_argument('filename', help='List of files, wildcards can be used here')
  parser.add_argument('-H', '--hours', required=True, type=int)
  parser.add_argument('-m', '--minutes', required=True, type=int)
  parser.add_argument('-a', '--action', choices=['timeAdd', 'timeSub'], required=True)
  args = parser.parse_args()

  fileList = glob.glob(args.filename)
  for fileName in fileList:
    if actionTime.isEligible(args.action):
      actionTime.processAction(fileName, args)

logging.basicConfig(level=logging.DEBUG)
main()
