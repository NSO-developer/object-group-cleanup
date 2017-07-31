import unittest
sys.path.append('../python')
import obj_cleanup
import ncs
import socket

class TestOGC(unittest.TestCase):

    def test_search_empty(self):
        """
        This function tests if the device is returning the correct output from the Object_group_cleaner tool.
        """
        device_typ = "device"
        device_name = "asa-netsim-1"
        with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
            root = ncs.maagic.get_root(t)
            device = root.devices.device[device_name]
            input1 = root.Object_group_cleaner.search.get_input()
            new_obj = input1.inputs.create()
            new_obj.input_type = device_typ
            new_obj.value = device_name
            #check output

    def test_seach_reg(self):

    def test_perf(self):

    def test_remove(self):

if __name__ == '__main__':
    unittest.main()
