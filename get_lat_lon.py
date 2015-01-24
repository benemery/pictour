import sys

from photo_geoip.helpers import extract_data

def main(filepath):
    with open(filepath, 'rb') as fin:
        print extract_data(fin)

if __name__ == '__main__':
    main(sys.argv[1])