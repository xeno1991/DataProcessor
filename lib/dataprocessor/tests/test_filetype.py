import unittest

from ..filetype import FileType
from ..filetype import path_to_filetype


class TestFileType(unittest.TestCase):

    def test_get_filetype(self):
        self.assertEqual(FileType.ini,  path_to_filetype("/path/to/hoge.ini"))
        self.assertEqual(FileType.ini,  path_to_filetype("/path/to/hoge.conf"))
        self.assertEqual(FileType.yaml, path_to_filetype("/path/to/hoge.yml"))
        self.assertEqual(FileType.yaml, path_to_filetype("/path/to/hoge.yaml"))
        # TODO catch exception after #169 is merges
        # self.assertEqual(FileType.NONE, path_to_filetype("/path/to/hoge.jpg"))
