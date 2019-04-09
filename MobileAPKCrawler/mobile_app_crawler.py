from Crawler import *
import sys
import argparse
from argparse import RawTextHelpFormatter


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


ARGS = None


def main():
    arg_parser = argparse.ArgumentParser(
      description='Mobile App Crawler Manual',
      formatter_class=RawTextHelpFormatter)
    arg_parser.add_argument('-m', '--method', 
      help=('crawl_new: Scrap PlayStore top 300 app information '
            'for each category\n'
            'crawl_old: Update collected app information\n'
            'update_apk: Download APK file'))
    arg_parser.add_argument('-d', '--desktop', 
      type=str2bool, default=True,
      help=('True(Default): Show web browser (use selenium)\n'
            'False: Do not show web browser (use virtual screen)'))

    args = arg_parser.parse_args()

    if(args.desktop != None):
        desktop = args.desktop

    if(args.method != None):
        method = args.method

    playstore_crawler = Crawler(is_desktop = desktop)

    if(method == "crawl_new"):
        playstore_crawler.crawl_new()
    elif(method == "crawl_old"):
        playstore_crawler.crawl_old()
    elif(method == "update_apk"):
        playstore_crawler.update_apk()

    playstore_crawler.close()



if __name__ == '__main__':
#    import argparse
#    parser = argparse.ArgumentParser(description='How to use APK crawler')
#    parser.add_argument('-t', '--target',
#                        type=str,
#                        help='APK package name')
#    ARGS = parser.parse_args()

    main()

