import unittest
import constants
import ncs
import socket
import time


class TestOGC(unittest.TestCase):
    """
    This program tests if the Object_group_cleaner tool is able to search all the object group list and checks if there are object groups that need to be deleted.
    """
    def test_search_empty(self):
        """
        With this test case, we create a netsim such that none of the object groups need to be deteled. This test passes if no object groups are returned.
        """

        orphaned_ogs = {}
        empty_dict = {}

        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, 'ncsadmin', 'python', groups=['ncsadmin']):

                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)

                    og = "test_og_"

                    num_types = 0
                    for ogtyp in root.devices.device[constants.device_name].config.asa__object_group:
                        og_num = og + str(num_types) + '_'
                        num_types = num_types + 1
                        for j in range(20):
                            fake_og = og_num + str(j)
                            root.devices.device[constants.device_name].config.asa__object_group[ogtyp].create(fake_og)

                    t.apply()

                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)

                    holder = "access_list_"
                    rul = "extended permit icmp object-group test_og_"

                    for i in range(num_types):
                        acl_num = holder + str(i)
                        root.devices.device[constants.device_name].config.asa__access_list.access_list_id.create(acl_num)
                        rul_num = rul + str(i) + '_'
                        for j in range(20):
                            fake_rule = rul_num + str(j)
                            root.devices.device[constants.device_name].config.asa__access_list.access_list_id[acl_num].rule.create(fake_rule)

                    t.apply()


                with m.start_write_trans() as t:

                    root = ncs.maagic.get_root(t)
                    device = root.devices.device[constants.device_name]
                    input1 = root.Object_group_cleaner.search.get_input()
                    new_obj = input1.inputs.create()
                    new_obj.input_type = constants.device_typ
                    new_obj.value = constants.device_name

                    output1 = root.Object_group_cleaner.search(input1)

                    end_time = output1.end_time
                    org_gps = output1.orphaned_object_groups

                    for og in org_gps:
                        if og.og_type in orphaned_ogs.keys():
                            orphaned_ogs[og.og_type].append(og.object_group)
                        else:
                            orphaned_ogs[og.og_type] = [og.object_group]

                    self.assertEqual(orphaned_ogs, empty_dict)

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
        """
        With this test case, we create a netsim such that an arbitrary number of the object groups need to be deteled. This test passes if the required object groups are returned.
        """

        orphaned_ogs = {}

        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, 'ncsadmin', 'python', groups=['ncsadmin']):

                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)

                    og = "test_og_"

                    num_types = 0
                    for ogtyp in root.devices.device[constants.device_name].config.asa__object_group:
                        og_num = og + str(num_types) + '_'
                        num_types = num_types + 1
                        for j in range(50):
                            fake_og = og_num + str(j)
                            root.devices.device[constants.device_name].config.asa__object_group[ogtyp].create(fake_og)

                    t.apply()

                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)

                    holder = "access_list_"
                    rul = "extended permit icmp object-group test_og_"

                    for i in range(num_types):
                        acl_num = holder + str(i)
                        root.devices.device[constants.device_name].config.asa__access_list.access_list_id.create(acl_num)
                        rul_num = rul + str(i) + '_'
                        for j in range(20):
                            fake_rule = rul_num + str(j)
                            root.devices.device[constants.device_name].config.asa__access_list.access_list_id[acl_num].rule.create(fake_rule)

                    t.apply()

                with m.start_write_trans() as t:

                    root = ncs.maagic.get_root(t)
                    device = root.devices.device[constants.device_name]
                    input1 = root.Object_group_cleaner.search.get_input()
                    new_obj = input1.inputs.create()
                    new_obj.input_type = constants.device_typ
                    new_obj.value = constants.device_name

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

    def test_perform(self):
        """
        With this test case, we create a netsim with 5000 object groups and 4500 ACL lines and checked if the tool runs within 500 secs.
        """

        orphaned_ogs = {}

        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, 'ncsadmin', 'python', groups=['ncsadmin']):

                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)

                    og = "test_og_"

                    num_types = 0
                    for ogtyp in root.devices.device[constants.device_name].config.asa__object_group:
                        og_num = og + str(num_types) + '_'
                        num_types = num_types + 1
                        for j in range(5000):
                            fake_og = og_num + str(j)
                            root.devices.device[constants.device_name].config.asa__object_group[ogtyp].create(fake_og)

                    t.apply()

                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)

                    holder = "access_list_"
                    rul = "extended permit icmp object-group test_og_"

                    for i in range(num_types):
                        acl_num = holder + str(i)
                        root.devices.device[constants.device_name].config.asa__access_list.access_list_id.create(acl_num)
                        rul_num = rul + str(i) + '_'
                        for j in range(4500):
                            fake_rule = rul_num + str(j)
                            root.devices.device[constants.device_name].config.asa__access_list.access_list_id[acl_num].rule.create(fake_rule)

                    t.apply()

                with m.start_write_trans() as t:

                    root = ncs.maagic.get_root(t)
                    device = root.devices.device[constants.device_name]
                    input1 = root.Object_group_cleaner.search.get_input()
                    new_obj = input1.inputs.create()
                    new_obj.input_type = constants.device_typ
                    new_obj.value = constants.device_name

                    b = time.time()
                    output1 = root.Object_group_cleaner.search(input1)
                    af = time.time()
                    run_time = af - b

                    self.assertTrue(run_time < 500)

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

    def test_remove(self):
        """
        With this test case, we create a netsim such that all of the object groups need to be deteled. This test passes if all object groups are returned and there are none left.
        """
        orphaned_ogs = {}
        empty_dict = []
        og_list = []

        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, 'ncsadmin', 'python', groups=['ncsadmin']):

                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)

                    og = "test_og_"

                    num_types = 0
                    for ogtyp in root.devices.device[constants.device_name].config.asa__object_group:
                        og_num = og + str(num_types) + '_'
                        num_types = num_types + 1
                        for j in range(20):
                            fake_og = og_num + str(j)
                            root.devices.device[constants.device_name].config.asa__object_group[ogtyp].create(fake_og)

                    t.apply()

                with m.start_write_trans() as t:
                    root = ncs.maagic.get_root(t)

                    holder = "access_list_"
                    rul = "extended permit icmp object-group test_og_"

                    for i in range(num_types):
                        acl_num = holder + str(i)
                        root.devices.device[constants.device_name].config.asa__access_list.access_list_id.create(acl_num)
                        rul_num = rul + str(i) + '_'
                        for j in range(0):
                            fake_rule = rul_num + str(j)
                            root.devices.device[constants.device_name].config.asa__access_list.access_list_id[acl_num].rule.create(fake_rule)

                    t.apply()


                with m.start_write_trans() as t:

                    root = ncs.maagic.get_root(t)
                    device = root.devices.device[constants.device_name]
                    input1 = root.Object_group_cleaner.cleanup.get_input()
                    new_obj = input1.inputs.create()
                    new_obj.input_type = constants.device_typ
                    new_obj.value = constants.device_name

                    output1 = root.Object_group_cleaner.cleanup(input1)

                    end_time = output1.end_time
                    number_of_ogs_deleted = output1.number_of_ogs_deleted

                    self.assertEqual(number_of_ogs_deleted, 0)

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

if __name__ == '__main__':
    unittest.main()
