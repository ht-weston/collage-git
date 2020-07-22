#!/bin/python

import os
import re
import glob

d='./imgs/'
cnt=1
col=1
row=0
rows=3
cols=2
AddedEnd=0
lim=len(glob.glob1(d,"*.jpg"))
figlist="{"
captlist="{"
labellist="["
latex="""
\\begin{minipage}{\\linewidth}
\\begin{InsertImages}
"""
for f in os.listdir(d):
    if not(f.endswith(".jpg")):
        continue
    if ((cnt)%(cols)):
       figlist+="%s,"%(d+f)
       captlist+="Figure %s,"%cnt
       labellist+="Fig:%s,"%cnt
    else:
        row+=1
        latex+="\InsertRowOfFigures{\linewidth}{3.1in}{2.5in}{m}%s%s}\nRow=%s\n"%(figlist,(d+f),row)
        figlist="{"
        latex+="\InsertCaptions%sFig:%s]%sFigure %s}{t}{figure}\n"%(labellist,cnt,captlist,cnt)
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
print(latex)
