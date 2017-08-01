import unittest
sys.path.append('../python')
import obj_cleanup
import ncs
import socket
import constants

class TestOGC(unittest.TestCase):

    def test_search_empty(self):
        """
        This function tests if the device is returning the correct output from the Object_group_cleaner tool.
        """

        orphaned_ogs = {}

        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, 'ncsadmin', 'python', groups=['ncsadmin']):

                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)

                    holder = "access_list_"
                    rul = "extended permit icmp object-group test_og_"

                    for i in range(4):
                        acl_num = holder + str(i)
                        root.devices.device[constants.device_name].config.asa__access_list.access_list_id.create(acl_num)
                        rul_num = rul + str(i) + '_'
                        for j in range(20):
                            fake_rule = rul_num + str(j)
                            root.devices.device[constants.device_name].config.asa__access_list.access_list_id[acl_num].rule.create(fake_rule)

                    t.apply()

                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)

                    og = "test_og_"

                    i = 0
                    for ogtyp in root.devices.device[constants.device_name].config.asa__object_group:
                        og_num = og + str(i) + '_'
                        i = i + 1
                        for j in range(50):
                            fake_og = og_num + str(j)
                            root.devices.device[constants.device_name].config.asa__object_group[ogtyp].create(fake_og)

                    t.apply()

                with m.start_write_trans() as t:

                    root = ncs.maagic.get_root(t)
                    device = root.devices.device[constants.device_name]
                    input1 = root.Object_group_cleaner.search.get_input()
                    new_obj = input1.inputs.create()
                    new_obj.input_type = constants.device_typ
                    new_obj.value = device_name

                    output1 = root.Object_group_cleaner.search(input1)

                    end_time = output1.end_time
                    org_gps = output1.orphaned_object_groups

                    for og in org_gps:
                        if og.og_type in orphaned_ogs.keys():
                            orphaned_ogs[og.og_type].append(og.object_group)
                        else:
                            orphaned_ogs[og.og_type] = [og.object_group]

                    self.assertEqual(orphaned_ogs, constants.answer)

                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)
                    for ogtyp in root.devices.device["asa-netsim-1"].config.asa__object_group:
                        for og in root.devices.device["asa-netsim-1"].config.asa__object_group[ogtyp]:
                            del root.devices.device["asa-netsim-1"].config.asa__object_group[ogtyp][og.id]

                    t.apply()

                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)
                    for acl in root.devices.device["asa-netsim-1"].config.asa__access_list.access_list_id:
                        del root.devices.device["asa-netsim-1"].config.asa__access_list.access_list_id[acl.id]

                    t.apply()




    def test_seach_reg(self):

    def test_perf(self):

    def test_remove(self):

if __name__ == '__main__':
    unittest.main()
