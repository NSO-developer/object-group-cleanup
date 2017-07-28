import unittest
sys.path.append('../python')
import obj_cleanup
import ncs
import socket

class TestOGC(unittest.TestCase):

    def test_search_empty(self):
        with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
            root = ncs.maagic.get_root(t)
            #root.Object_group_cleaner.search.input.("device","asa-netsim-1")
            root.devices.device["asa-netsim-1"].config.asa__access_list.access_list_id.create("access_list_0")
            root.devices.device["asa-netsim-1"].config.asa__access_list.access_list_id.create("access_list_1")
            root.devices.device["asa-netsim-1"].config.asa__access_list.access_list_id.create("access_list_2")

    def test_seach_reg(self):

    def test_perf(self):

    def test_remove(self):

if __name__ == '__main__':
    unittest.main()
