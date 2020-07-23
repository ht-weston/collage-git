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
        d='./src/imgs/'
        files = os.listdir(d)
        for f in files:
            try:
                self.imgs.append(img(d + f))
            except:
                continue

    def test_img(self):
        print(self.imgs[0].gpsLong)
        print(self.imgs[1].path)
        print(self.imgs[1].ctime)
        assert(False)

    def test_tolatex(self):
        print(to_latex("./src/imgs/"))
        assert(False)

