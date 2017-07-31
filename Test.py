import ncs
import socket
import obj_cleanup1

if __name__ == '__main__':
    with ncs.maapi.Maapi() as m:
        with ncs.maapi.Session(m, 'ncsadmin', 'python', groups=['ncsadmin']):

            with m.start_write_trans() as t:
                root = ncs.maagic.get_root(t)
                #root.Object_group_cleaner.search.input.("device","asa-netsim-1")

                holder = "access_list_"
                rul = "extended permit icmp object-group test_og_"

                for i in range(4):
                    acl_num = holder + str(i)
                    root.devices.device["asa-netsim-1"].config.asa__access_list.access_list_id.create(acl_num)
                    rul_num = rul + str(i) + '_'
                    for j in range(20):
                        fake_rule = rul_num + str(j)
                        root.devices.device["asa-netsim-1"].config.asa__access_list.access_list_id[acl_num].rule.create(fake_rule)

                t.apply()

            with m.start_write_trans() as t:
                root = ncs.maagic.get_root(t)

                og = "test_og_"

                i = 0
                for ogtyp in root.devices.device["asa-netsim-1"].config.asa__object_group:
                    og_num = og + str(i) + '_'
                    i = i + 1
                    for j in range(50):
                        fake_og = og_num + str(j)
                        root.devices.device["asa-netsim-1"].config.asa__object_group[ogtyp].create(fake_og)

                t.apply()

            orphaned_ogs = obj_cleanup1.flag_ogs_in_box_test("asa-netsim-1")
            answer = {'icmp-type': ['test_og_2_20', 'test_og_2_21', 'test_og_2_22', 'test_og_2_23', 'test_og_2_24', 'test_og_2_25', 'test_og_2_26', 'test_og_2_27', 'test_og_2_28', 'test_og_2_29', 'test_og_2_30', 'test_og_2_31', 'test_og_2_32', 'test_og_2_33', 'test_og_2_34', 'test_og_2_35', 'test_og_2_36', 'test_og_2_37', 'test_og_2_38', 'test_og_2_39', 'test_og_2_40', 'test_og_2_41', 'test_og_2_42', 'test_og_2_43', 'test_og_2_44', 'test_og_2_45', 'test_og_2_46', 'test_og_2_47', 'test_og_2_48', 'test_og_2_49'], 'user': ['test_og_0_20', 'test_og_0_21', 'test_og_0_22', 'test_og_0_23', 'test_og_0_24', 'test_og_0_25', 'test_og_0_26', 'test_og_0_27', 'test_og_0_28', 'test_og_0_29', 'test_og_0_30', 'test_og_0_31', 'test_og_0_32', 'test_og_0_33', 'test_og_0_34', 'test_og_0_35', 'test_og_0_36', 'test_og_0_37', 'test_og_0_38', 'test_og_0_39', 'test_og_0_40', 'test_og_0_41', 'test_og_0_42', 'test_og_0_43', 'test_og_0_44', 'test_og_0_45', 'test_og_0_46', 'test_og_0_47', 'test_og_0_48', 'test_og_0_49'], 'service': ['test_og_1_20', 'test_og_1_21', 'test_og_1_22', 'test_og_1_23', 'test_og_1_24', 'test_og_1_25', 'test_og_1_26', 'test_og_1_27', 'test_og_1_28', 'test_og_1_29', 'test_og_1_30', 'test_og_1_31', 'test_og_1_32', 'test_og_1_33', 'test_og_1_34', 'test_og_1_35', 'test_og_1_36', 'test_og_1_37', 'test_og_1_38', 'test_og_1_39', 'test_og_1_40', 'test_og_1_41', 'test_og_1_42', 'test_og_1_43', 'test_og_1_44', 'test_og_1_45', 'test_og_1_46', 'test_og_1_47', 'test_og_1_48', 'test_og_1_49'], 'network': ['test_og_3_20', 'test_og_3_21', 'test_og_3_22', 'test_og_3_23', 'test_og_3_24', 'test_og_3_25', 'test_og_3_26', 'test_og_3_27', 'test_og_3_28', 'test_og_3_29', 'test_og_3_30', 'test_og_3_31', 'test_og_3_32', 'test_og_3_33', 'test_og_3_34', 'test_og_3_35', 'test_og_3_36', 'test_og_3_37', 'test_og_3_38', 'test_og_3_39', 'test_og_3_40', 'test_og_3_41', 'test_og_3_42', 'test_og_3_43', 'test_og_3_44', 'test_og_3_45', 'test_og_3_46', 'test_og_3_47', 'test_og_3_48', 'test_og_3_49']}

            if orphaned_ogs == answer:
                print 1
            else:
                print 0
            
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
