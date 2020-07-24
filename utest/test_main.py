import pytest
import unittest
import os
import io
import csv
from tabulate import tabulate as tbl
from main import *
import numpy as np

def isclose(a, b, rel_tol=1e-05, abs_tol=0.0):
    a = float(a)
    b = float(b)
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class TestMain(unittest.TestCase):
    def setUp(self):
        self.imgdict = defaultdict(list)
        for dp,dn,fs in os.walk("./src/imgs/"):
            for f in fs:
                try:
                    self.imgsdict[dp].append(img(os.path.join(dp,f)))
                except Exception as e:
                    continue
            # self.imgdict[dp].sort(key=lambda x: x.ctime,reverse=False)

    def off_test_img(self):
        # print(self.imgs[0].gpsLong)
        # print(self.imgs[1].path)
        # print(self.imgs[1].ctime)
        assert(False)

    def test_tolatex(self):
        print(to_latex("./src/imgs/"))
        assert(False)

