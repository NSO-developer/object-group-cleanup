#UNTESTED CODE

import ncs
import socket
import multiprocessing as mp
import Queue
import threading


#found = Queue.Queue()

#/ ncs:devices / device { svl-gem-joe-asa-fw1.cisco.com } / config / asa:access-list / access-list-id { gem_ft_apt }
def find_rule_in_ACL (box, og, ACL, flag):
    """
    This funcion will iterate through the rules in the ACL to find matches of the given OG. Returns boolean
    values
    """
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        for rul in root.devices.device[box].config.asa__access_list.access_list_id[ACL.id].rule:
            #if flag.value == 1:
                #return
        #print rul.id
            if og in rul.id:
            #print og
            #return True
            #with found.mutex:
            #found.put('T')
                flag.value = 1
                return         #return true for continuous iteration
    #with found.mutex:
        #found.put('F')
        return
    #return False               #return false for flagging for removal

def find_in_ACLS(box, og, root):
    """
    Function will iterate through the ACL's within device and return true if found (keep)
    and false if not found (remove)
    """
    found = mp.Value('i', 0)
    pro = []
    #flag = False
    #found.queue.clear()
    #found = ['F']
    #/ ncs:devices / device { svl-gem-joe-asa-fw1.cisco.com } / config / asa:access-list / access-list-id { jw_apt }
    for acl in root.devices.device[box].config.asa__access_list.access_list_id:
        p = mp.Process(target=find_rule_in_ACL, args=(box, og, acl, found))
        pro.append(p)
        p.start()
    for i in pro:
        i.join()
    if found.value == 1:
        return True
    else:
        return False
    #while True:
        #if 'T' in found:
            #return True
        #elif mp.activeCount() == 0:
            #return False
        #print acl.id
        #flag = find_rule_in_ACL(box, og, root, acl)
        #if flag:
            #break
    #return flag            #return true if found, false if not

def flag_ogs_in_box(box):
    """
    This function returns a list of object groups that are orphaned in that device.
    """
    #og_type = ['icmp_type','network','service','user']
    orphaned_og = []
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        #for ogtyp in root.devices.device[box].config.asa__object_group:
        for og in root.devices.device[box].config.asa__object_group['asa:network']:
            if not find_in_ACLS(box,og.id,root):
                    #print og.id
                orphaned_og.append(og.id)
        return orphaned_og

if __name__ == "__main__":
    #found = []
    #test = ['hello','Hi']
    #if 'hello' in test:
        #print "yes!"
    print flag_ogs_in_box('svl-gem-joe-asa-fw1.cisco.com')
