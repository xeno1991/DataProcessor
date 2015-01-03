import os
import unittest

from ..pipes.scan_configure import scan_configure


class TestScanConfigure(unittest.TestCase):

    def _find_by_name(self, node_list, name):
        for node in node_list:
            if node["name"] == name:
                return node
        return None

    def testScanYaml(self):
        ROOT = os.path.dirname(os.path.abspath(__file__))
        node_list = scan_configure([], ROOT, "param.yml", followlinks=False,
                                   filetype=None, section="parameters")

        self.assertEqual(3, len(node_list))

        run1 = self._find_by_name(node_list, "run1")
        self.assertEqual({"n": 1}, run1["configure"])

        run1 = self._find_by_name(node_list, "run2")
        self.assertEqual({"n": 2}, run1["configure"])
