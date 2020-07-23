#!/bin/python

import os
from PIL import Image
import glob
import exifread

class img():
    @property
    def gpsLati (self):
        return img._to_decimal(self._gpsLati)

    @property
    def gpsLong(self):
        return img._to_decimal(self._gpsLong)

    @property
    def desc(self):
        return self._desc

    @property
    def name(self):
        return self._name

    @property
    def path(self):
         self._path

    @property
    def ctime(self):
        tmp = self._ctime
        # datetime.
        return self._ctime

    @property
    def direc(self):
        return self._direc

    @property
    def caption(self):
        return self._caption

    def __init__(self,p):
        try:
            with open(p,'rb') as f :
                tags = exifread.process_file(f)

            self._gpsLong=tags['GPS GPSLongitude']
            self._gpsLati=tags["GPS GPSLatitude"]
            self._ctime= tags["Image DateTime"]
            self._direc=tags["GPS GPSImgDirection"]
        except Exception as e:
            print(p + " is not a valid image.")

    def _to_decimal(hms):
        hms = str(hms)
        return hms

        # return hms[0] + hms[1]/60 + hms[2]/3600


# d='./src/imgs/'
# cnt=1
# col=1
# row=0
# rows=3
# cols=2
# AddedEnd=0
# lim=len(glob.glob1(d,"*.jpg"))
# figlist="{"
# captlist="{"
# labellist="["
# latex="""
# \\begin{minipage}{\\linewidth}
# \\begin{InsertImages}
# """
# files = os.listdir(d)
# imgs = [ img(f) for f in files ]
# # imgs = sorted(files,key = lambda f: )

# for f in files:
    # if not(f.endswith(".jpg")):
        # continue
    # if ((cnt)%(cols)):
       # figlist+="%s,"%(d+f)
       # captlist+="Figure %s,"%cnt
       # labellist+="Fig:%s,"%cnt
    # else:
        # row+=1
        # latex+="\InsertRowOfFigures{\linewidth}{3.1in}{2.5in}{m}%s%s}\n"%(figlist,(d+f))
        # figlist="{"
        # latex+="\InsertCaptions%sFig:%s]%sFigure %s}{t}{figure}\n"%(labellist,cnt,captlist,cnt)
        # if (rows==row):
          # latex+="""\end{InsertImages}\n\end{minipage}\n\n"""
          # AddedEnd=1
          # row=0
          # if cnt < lim:
            # latex+="""\n\\begin{minipage}{\linewidth}\n\\begin{InsertImages}\n"""
        # else:
            # AddedEnd=0
        # labellist="["
        # captlist="{"
    # cnt+=1
# if ((AddedEnd==0) & (col>=lim)):
      # latex+="""\end{InsertImages}\n\end{minipage}\n\n"""
# print(latex)

