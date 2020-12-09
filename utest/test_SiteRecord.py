import unittest
import os

from SiteRecord import SiteRecord


class TestSiteRecord(unittest.TestCase):

    def test_load_from_folder(self):
        x = SiteRecord(os.getcwd() + "/src/imgs/Site 1: North of W Slauson Ave between S. Mullen Ave and Kenniston Ave")

        assert(len(x.images) == 10)
