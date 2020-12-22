import unittest
import os

from ImageRecord import ImageRecord


class TestImageRecord(unittest.TestCase):

    def test_load_from_folder(self):
        x = ImageRecord(1337, os.getcwd() + "/src/imgs/Site 1: North of W Slauson Ave between S. Mullen Ave and Kenniston Ave/Green Alleys-2020-07-17-11-53-56.jpg")

        assert(x.id == 1337)

        assert(x.caption == "2020:07:17 11:53:55")

        #assert(len(x.images) == 10)