from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os


def get_image_name_from_path(path):
    return os.path.splitext(os.path.basename(path))[0]


class img:
    def __init__(self, path):
        try:
            pic = Image.open(path)
            pic.verify()
            self._is_valid = True
            exif = pic._getexif()
            labels = {}
            geotags = {}

            for (key, val) in exif.items():
                labels[TAGS.get(key)] = val

            for (idx, tag) in TAGS.items():
                if tag == 'GPSInfo':
                    if idx not in exif:
                        raise ValueError("No EXIF geotagging found")

                    for (key, val) in GPSTAGS.items():
                        if key in exif[idx]:
                            geotags[val] = exif[idx][key]  # Get Geotags.

            coord = img._get_coordinates(geotags)
            self._path = path
            self._name = get_image_name_from_path(path)
            self._gpsLati = coord[0]
            self._gpsLong = coord[1]
            self._ctime = labels['DateTime']
            self._caption = self._create_caption()
            self._desc = labels["UserComment"]

        except Exception as e:
            raise e

    def _create_caption(self):
        return self._ctime

    def _get_decimal_from_dms(dms, ref):
        try:
            degrees = dms[0][0] / dms[0][1]
            minutes = dms[1][0] / dms[1][1] / 60.0
            seconds = dms[2][0] / dms[2][1] / 3600.0
        except:
            degrees = dms[0]
            minutes = dms[1] / 60.0
            seconds = dms[2] / 3600.0

        if ref in ['S', 'W']:
            degrees = -degrees
            minutes = -minutes
            seconds = -seconds

        return round(degrees + minutes + seconds, 8)

    def _get_coordinates(geotags):
        lat = img._get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])

        lon = img._get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

        return lat, lon

    @property
    def gpsLati (self):
        return self._gpsLati

    @property
    def gpsLong(self):
        return self._gpsLong

    @property
    def desc(self):
        return self._desc

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def ctime(self):
        return self._ctime

    @property
    def direc(self):
        return self._direc

    @property
    def caption(self):
        return self._caption

    @property
    def is_valid(self):
        return self._is_valid

    def __eq__(self, other):
        return (self.ctime == other.ctime)

    def __ne__(self, other):
        return (self.ctime != other.ctime)

    def __lt__(self, other):
        return (self.ctime < other.ctime)

    def __le__(self, other):
        return (self.ctime <= other.ctime)

    def __gt__(self, other):
        return (self.ctime > other.ctime)

    def __ge__(self, other):
        return (self.ctime >= other.ctime)

    def __repr__(self):
        return "%s" % (self.path)
