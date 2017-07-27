import unittest
sys.path.append('../python')
import obj_cleanup
import ncs

class TestOGC(unittest.TestCase):

    def test_search_empty(self):
        with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
            root = ncs.maagic.get_root(t)
            root.Object_group_cleaner.search.input.("device","asa-netsim-1")

    def test_seach_reg(self):

    def test_perf(self):

    def test_remove(self):

if __name__ == '__main__':
    unittest.main()
