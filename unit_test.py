import unittest
import sys
sys.path.append('../python')
import ncs
import socket
import obj_cleanup


if __name__ == '__main__':

    device_typ = "device"
    device_name = "asa-netsim-1"
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        device = root.devices.device[device_name]
        input1 = root.Object_group_cleaner.search.get_input()
        new_obj = input1.inputs.create()
        new_obj.input_type = device_typ
        new_obj.value = device_name
        print new_obj.input_type
        print new_obj.value
