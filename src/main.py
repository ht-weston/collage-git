#!/bin/python

import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import glob
import sys
from collections import defaultdict


class img():
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

    def __init__(self,path):
        try:
            pic = Image.open(path)
            pic.verify()
            self._is_valid = True
            exif = pic._getexif()
            labels = {}
            geotgs = {}
            for (key,val) in exif.items():
                labels[TAGS.get(key)] = val

            for (idx, tag) in TAGS.items():
                if tag == 'GPSInfo':
                    if idx not in exif:
                        raise ValueError("No EXIF geotagging found")

                    for (key, val) in GPSTAGS.items():
                        if key in exif[idx]:
                            geotgs[val] = exif[idx][key] # Get Geotags.

            coord = img._get_coordinates(geotgs)
            self._path = path
            self._gpsLati = coord[0]
            self._gpsLong = coord[1]
            self._ctime = labels['DateTime']
            self._desc = labels["UserComment"]
        except Exception as e:
            raise e

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

        return (lat,lon)

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

def to_latex(dirpath):
    cnt=1
    col=1
    row=0
    rows=3
    cols=2
    AddedEnd=0
    lim=len(glob.glob1(dirpath,"*.jpg"))
    imgdict = defaultdict(list)
    latex=""
    # result = [os.path.join(dp, f) for dp, dn, filenames in os.walk(PATH) for f in filenames if os.path.splitext(f)[1] == '.txt']
    for dp,dn,fs in os.walk(dirpath):
        for f in fs:
            try:
                imgdict[dp].append(img(os.path.join(dp,f)))
            except Exception as e:
                continue
        imgdict[dp].sort(key=lambda x: x.ctime,reverse=False)

    for key,fs in imgdict.items():
        latex+="\section{%s}\n"%(key)
        figlist="{"
        captlist="{"
        labellist="["
        latex+="""\\begin{minipage}{\\linewidth}
        \\begin{InsertImages}
        """
        for f in fs:
            if ((cnt)%(cols)):
               figlist+="%s,"%f.path
               captlist+="Figure %s,"%cnt
               labellist+="Fig:%s,"%cnt
            else:
                row+=1
                latex+="\InsertRowOfFigures{\linewidth}{3.1in}{2.5in}{m}%s%s}\n"%(figlist,f.path)
                figlist="{"
                latex+="\InsertCaptions%sFig:%s]%sFigure %s}{t}{figure}\n"%(labellist,cnt,captlist,cnt)
                # test
                if (rows==row):
                  latex+="""\end{InsertImages}\n\end{minipage}\n\n"""
                  AddedEnd=1
                  row=0
                  if cnt < lim:
                    latex+="""\n\\begin{minipage}{\linewidth}\n\\begin{InsertImages}\n"""
                else:
                    AddedEnd=0
                labellist="["
                captlist="{"
            cnt+=1
        if ((AddedEnd==0) & (col>=lim)):
              latex+="""\end{InsertImages}\n\end{minipage}\n\n"""
    return latex

if __name__ == "__main__":
    st = to_latex(sys.argv[1])
    print(st)
