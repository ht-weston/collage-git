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
    cnt=0
    col=1
    row=0
    rows=2
    cols=2
    proposedWidth=3.1 #in
    proposedHeight=2.5 #in
    collageID=0
    totalRows=1
    totalCols=0
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

    shapeFile = open("shapeFile.csv","w")
    shapeFile.write("file path, file name, atitude, longitude, collage id\n")
    for key,fs in imgdict.items():
        figlist="{"
        captlist="{"
        labellist="["
        cnt=0
        if (len(fs)):
            latex+="\n\n\section{%s}\n\\refstepcounter{imsection}\n"%(key[key.rindex('/',0,-1)+1:-1])
            latex+="\n\\noindent\\begin{minipage}{\\linewidth}\n\\begin{InsertImages}"
            col=1
            row=0
        else:
            cnt+=1
            continue
        for f in fs:
            cnt+=1
            AddedEnd=0
            im=Image.open(f.path)
            wid,hei=im.size
            if ((cnt==len(fs))):
                figlist+="%s}"%f.path
                captlist+="%s}"%f.path[f.path.rindex('/',0,-4)+1:-4]
                labellist+="Fig:\\theimsection.%s]"%cnt
                col+=1
                collageID+=1
                totalCols+=1
                shapeFile.write("%s, %s, %s, %s, %s\n"%(f.path,f.path[f.path.rindex('/',0,-4)+1:-4],totalRows,totalCols,collageID ))# file path, file name, atitude, longitude, collage id.
            elif((col)%(cols)):
                figlist+="%s,"%f.path
                captlist+="%s,"%f.path[f.path.rindex('/',0,-4)+1:-4]
                labellist+="Fig:\\theimsection.%s,"%cnt
                col+=1
                collageID+=1
                totalCols+=1
                shapeFile.write("%s, %s, %s, %s, %s\n"%(f.path,f.path[f.path.rindex('/',0,-4)+1:-4],totalRows,totalCols,collageID ))
            else:
                figlist+="%s}"%f.path
                captlist+="%s}"%f.path[f.path.rindex('/',0,-4)+1:-4]
                labellist+="Fig:\\theimsection.%s]"%cnt
                col=1
                row+=1
                collageID+=1
                totalCols+=1
                shapeFile.write("%s, %s, %s, %s, %s\n"%(f.path,f.path[f.path.rindex('/',0,-4)+1:-4],totalRows,totalCols,collageID ))
                totalRows+=1
                totalCols=0
                latex+="\InsertRowOfFigures{\linewidth}{%sin}{%sin}{m}%s\n"%(proposedWidth,proposedHeight,figlist)
                latex+="\InsertCaptions%s%s{t}{figure}\n"%(labellist,captlist)
                figlist="{"
                captlist="{"
                labellist="["

            if ((row==rows)):
                latex+="\end{InsertImages}\n\end{minipage}\n\n"
                AddedEnd=1
                row=0
                if (cnt<len(fs)):
                    latex+="\n\\begin{minipage}{\\linewidth}\n\\begin{InsertImages}\n"
                    AddedEnd=0
                    row=0

            elif((cnt==len(fs))&(AddedEnd==0)):
                if (figlist!="{"):
                    totalCols=0
                    totalRows+=1
                    latex+="\InsertRowOfFigures{\linewidth}{%sin}{%sin}{m}%s\n"%(proposedWidth,proposedHeight,figlist)
                    latex+="\InsertCaptions%s%s{t}{figure}\n"%(labellist,captlist)
                    #k=1
                    #for letterB in figlist:
                    #    if (letterB==','):
                    #        k+=1
                    #collageID+=k

                latex+="\end{InsertImages}\n\end{minipage}\n\n"
                AddedEnd=1
                row=0

    return latex

if __name__ == "__main__":
    st = to_latex(sys.argv[1])
    print(st)
