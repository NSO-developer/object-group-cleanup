#UNTESTED CODE

import ncs
import socket

def find_rule_in_ACL (box, og, root, ACL):
    """
    This funcion will iterate through the rules in the ACL to find matches of the given OG. Returns boolean
    values
    """
    for rul in root.devices.device[box].config.asa__access_list.access_list_id[ACL.id].rule:
        if og in rul:
            return True         #return true for continuous iteration
    return False                #return false for flagging for removal

def find_in_ACLS(box, og, root):
    """
    Function will iterate through the ACL's within device and return true if found (keep)
    and false if not found (remove)
    """
    flag = False
    for acl in root.devices.device[box].config.asa__access_list.access_list_id:
        flag = find_rule_in_ACL(box, og, root, acl)
        if flag:
            break
    return flag            #return true if found, false if not

def flag_ogs_in_box(box):
    """
    This function returns a list of object groups that are orphaned in that device.
    """
    orphaned_og = []
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        #print(dir(root.devices.device[box].config.asa__object_group))
        for typ in root.devices.device[box].config.asa__object_group:
            print root.devices.device[box].config.asa__object_group[typ]
            for og in root.devices.device[box].config.asa__object_group[typ]:
                print og
                if not find_in_ACLS(box,og,root):
                    orphaned_og.append(str(og))
    return orphaned_og

if __name__ == "__main__":
    print flag_ogs_in_box('svl-gem-joe-asa-fw1.cisco.com')
