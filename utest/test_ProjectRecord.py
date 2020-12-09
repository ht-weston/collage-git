import unittest
import os
import shutil

from ProjectRecord import ProjectRecord
import ProjectRecord


class TestProjectRecord(unittest.TestCase):

    def test_load_from_folder(self):
        from_yaml = ProjectRecord.load_project_record_from_yaml("./utest/CheckpointB/CheckpointB.yml")
        from_dir = ProjectRecord.ProjectRecord("./utest/CheckpointB")

        assert(len(from_yaml.sites) == len(from_dir.sites))

    def test_comparetwo(self):
        from_yaml = ProjectRecord.load_project_record_from_yaml("./utest/CheckpointA/CheckpointA.yml")
        from_dir = ProjectRecord.ProjectRecord("./utest/CheckpointB")

        assert(len(from_yaml.sites) == len(from_dir.sites) - 1)

    def test_sync(self):

        from_dir_start = ProjectRecord.ProjectRecord("./utest/CheckpointB")
        initial_site_count = len(from_dir_start.sites)
        print("after initial load")
        ProjectRecord.write_project_record_to_yaml(from_dir_start, "./utest/test_sync_a.yml")

        shutil.move('./utest/CheckpointB/Site 1: North of W Slauson Ave between S. Mullen Ave and Kenniston Ave',
                    './utest/moved')
        from_dir_start._load_from_folder()
        ProjectRecord.write_project_record_to_yaml(from_dir_start, "./utest/test_sync_b.yml")

        shutil.move('./utest/moved',
                    './utest/CheckpointB/Site 1: North of W Slauson Ave between S. Mullen Ave and Kenniston Ave')

        final_site_count = len(from_dir_start.sites)

        assert final_site_count == initial_site_count - 1

