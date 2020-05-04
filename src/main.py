#!/bin/python

import os
import re
import glob

d='./imgs/'
cnt=1
row=1
rows=3
cols=2
lim=len(glob.glob1(d,"*.jpg"))
latex="""
\\begin{figure}
\\centering
\\begin{tabular}{c c}
"""
for f in os.listdir(d):
    if not(f.endswith(".jpg")):
        continue

    latex+="\subf{\includegraphics[height=2in,width=3.1in]{%s}}\n{\\textbf{Figure %s}: site_location \\\\ description}\n"%(d+f,cnt)
    latex+="&\n"
    cnt+=1

    if cnt % cols:
        latex+="\\\\\n"
        row+=1

    if row > rows:
        # This is a new page
        latex+="""\end{tabular}\n\end{figure}"""
        latex+="""\n\n\\newpage\n\n"""
        row=1

        if cnt < lim:
            latex+="""\\begin{figure}\n\centering\n\\begin{tabular}{c c}\n"""

        if cnt > lim:
            latex+="\\\\\n"
            latex+="""\end{tabular}\n\end{figure}"""

latex+="""
\end{tabular}
\end{figure}
"""
print(latex)
