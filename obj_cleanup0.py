#UNTESTED CODE

import ncs
import socket
#/ ncs:devices / device { svl-gem-joe-asa-fw1.cisco.com } / config / asa:access-list / access-list-id { gem_ft_apt }
def find_rule_in_ACL (box, og, root, ACL):
    """
    This funcion will iterate through the rules in the ACL to find matches of the given OG. Returns boolean
    values
    """
    for rul in root.devices.device[box].config.asa__access_list.access_list_id[ACL.id].rule:
        #print rul.id
        if og in rul.id:
            #print og
            return True         #return true for continuous iteration
    return False                #return false for flagging for removal

def find_in_ACLS(box, og, root):
    """
    Function will iterate through the ACL's within device and return true if found (keep)
    and false if not found (remove)
    """
    flag = False
    #/ ncs:devices / device { svl-gem-joe-asa-fw1.cisco.com } / config / asa:access-list / access-list-id { jw_apt }
    for acl in root.devices.device[box].config.asa__access_list.access_list_id:
        #print acl.id
        flag = find_rule_in_ACL(box, og, root, acl)
        if flag:
            break
    return flag            #return true if found, false if not

def flag_ogs_in_box(box):
    """
    This function returns a list of object groups that are orphaned in that device.
    """
    #og_type = ['icmp_type','network','service','user']
    orphaned_og = []
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        grp = root.devices.device[box].config.asa__object_group
        for ogtyp in grp:
            for og in root.devices.device[box].config.asa__object_group[ogtyp]:
                if not find_in_ACLS(box,og.id,root):
                    #print og.id
                    orphaned_og.append(og.id)
    return orphaned_og

if __name__ == "__main__":
    print flag_ogs_in_box('svl-gem-joe-asa-fw1.cisco.com')
