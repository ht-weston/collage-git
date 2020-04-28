#!/bin/python

import os
import re
d='./imgs'
cnt=1
row=1
rows=3
cols=2
lim=len([n for n in os.listdir(d) if n.endswith('*.jpg')])
print(lim)
latex="""
\\begin{figure}
\\centering
\t\\begin{tabular}{c c}
"""
for f in os.listdir(d):
    if not(f.endswith(".jpg")):
        continue

    latex+="\t\t\subf{\includegraphics[width=3.1in]{%s}\n\t\t{Figure %s: site_location \\\\ description}\n"%(d+f,cnt)
    latex+="\t\t&\n"
    cnt+=1

    if cnt % cols:
        latex+="\t\t\\\\\n"
        row+=1

    if row > rows:
        latex+="""\t\end{tabular}\n\end{figure}"""
        row=1

    if cnt < lim:
        latex+="""\n\n\\nextpage\n\n\\begin{figure}\n\centering\n\t\\begin{tabular}{c c}\n"""

    if cnt > 10:
        break

latex+="""
\end{tabular}
\end{figure}
"""
print(latex)
