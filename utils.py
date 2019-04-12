import os
import exifread
from datetime import datetime


def get_extension(filename):
    filename, file_extension = os.path.splitext(filename)
    return file_extension.lower()


def parse_date(filename_and_exif):
    filename, exif_info = filename_and_exif

    if not exif_info:
        return filename, None
    date = exif_info.get('Image DateTime')
    if not date:
        return filename, None
    try:
        return filename, datetime.strptime(str(date.values), '%Y:%m:%d %H:%M:%S').date()
    except:
        print(date)


def get_exif(filename):
    try:
        with open(filename, 'rb') as f:
            return filename, exifread.process_file(f)
    except:
        return filename, None

