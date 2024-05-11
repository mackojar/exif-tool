import logging
import argparse
import actionTime

def main():
  parser = argparse.ArgumentParser(
                    prog='ExifTool',
                    description='Process EXIF data for given filenames: change datetime',
                    epilog='')
  parser.add_argument('filenames', help='List of files, wildcards can be used here', nargs='+')
  parser.add_argument('-H', '--hours', required=True, type=int)
  parser.add_argument('-m', '--minutes', required=True, type=int)
  parser.add_argument('-a', '--action', choices=['timeAdd', 'timeSub'], required=True)
  args = parser.parse_args()

  if actionTime.isEligible(args.action):
    actionProcessor = actionTime.ActionTime(args)

  for fileName in args.filenames:
    actionProcessor.processAction(fileName)

logging.basicConfig(level=logging.INFO)
main()
