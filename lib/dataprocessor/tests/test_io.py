# coding=utf-8
import os
import tempfile
import copy
import unittest

from .. import io as dpio
from .. import nodes


class TestIo(unittest.TestCase):

    def setUp(self):
        self.jsonfile = os.path.join(tempfile.mkdtemp(), "dat.json")
        open(self.jsonfile, "a").close()

    def tearDown(self):
        import shutil
        shutil.rmtree(os.path.dirname(self.jsonfile))

    def test_datahandler1(self):
        node_list = [{"path": "/path/to/hogehoge", "name": "Oh"},
                     {"path": "/path/to/2", "name": "Yeah!!",
                      "parents": ["/path/to/foo"], "children": []}]
        added_node = {"path": "/path/to/foo", "name": "yahoooooo",
                      "parents": [], "children": ["/path/to/2"]}
        # Create json file
        dpio.save(node_list, self.jsonfile, silent=True)

        compare_node_list = copy.deepcopy(node_list)
        nodes.add(compare_node_list, copy.deepcopy(added_node))

        with dpio.DataHandler(self.jsonfile, True) as data:
            data.add(added_node)
            self.assertEqual(data.get(), compare_node_list)

        node_list = dpio.load([], self.jsonfile)
        self.assertEqual(node_list, compare_node_list)

    def test_datahandler2(self):
        node_list = [{"path": "/path/to/hogehoge", "name": "Oh"},
                     {"path": "/path/to/2", "name": "Yeah!!"}]
        replace_node_list = [{"path": "/path/to/foo", "name": "yahoooooo"}]
        # Create json file
        dpio.save(node_list, self.jsonfile, silent=True)

        compare_node_list = copy.deepcopy(replace_node_list)

        with dpio.DataHandler(self.jsonfile, True) as data:
            data.replace(replace_node_list)

        node_list = dpio.load([], self.jsonfile)
        self.assertEqual(node_list, compare_node_list)

    def test_sync_datahandler(self):
        node_list = [{"path": "/path/to/hogehoge", "name": ""}]

        # Create json file
        dpio.save(node_list, self.jsonfile, silent=True)

        import time

        def do_update1():
            with dpio.SyncDataHandler(self.jsonfile, silent=True) as data:
                node_list = data.get()
                node_list[0]["name"] += "update1"
                time.sleep(1)

        def do_update2():
            with dpio.SyncDataHandler(self.jsonfile, silent=True) as data:
                node_list = data.get()
                node_list[0]["name"] += "update2"
                time.sleep(1)

        from threading import Thread

        t1 = Thread(target=do_update1)
        t2 = Thread(target=do_update2)
        t1.start()
        time.sleep(0.001)
        t2.start()
        t1.join()
        t2.join()

        node_list_last = dpio.load([], self.jsonfile)
        node_list_ans = [
            {"path": "/path/to/hogehoge", "name": "update1update2"}]
        self.assertEqual(node_list_last, node_list_ans)
