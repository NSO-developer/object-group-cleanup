#UNTESTED CODE

import ncs
import socket

def flag_ogs_in_box(box):
    """
    This function returns a list of object groups that are orphaned in that device.
    """
    orphaned_og = []
    with ncs.maapi.single_write_trans('admin','python') as t:
        root = ncs.maapi.get_root(t)
        for og in root.devices.device[box].config.object-group:
            if (!find_in_ACLS(box,og,root)):
                orphaned_og.append(str(og))
    return orphaned_og

def find_in_ACLS(box, og, root):
    """
    Function will iterate through the ACL's within device and return true if found (keep)
    and false if not found (remove)
    """
    flag = false

    for acl in root.devices.device[box].config.access_list.extended:
        flag = find_rule_in_ACL(box, og, root, acl)

        if flag == true:
            break

        return flag            #return true if found, false if not

def find_rule_in_ACL (box, og, root, ACL):
    """
    This funcion will iterate through the rules in the ACL to find matches of the given OG. Returns boolean
    values
    """
    for rule in root.devices.device[box].config.access_list[ACL]:
        if og in rule:
            return true         #return true for continuous iteration
    return false                #return false for flagging for removal
