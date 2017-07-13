import ncs
import socket
import threading
import Queue
import time
import concurrent.futures

def find_rule_in_ACL (box, og, root, rul, q):
    """
    This funcion will iterate through the rules in the ACL to find matches of the given OG. Returns boolean
    values
    """

        #for rul in root.devices.device[box].config.asa__access_list.access_list_id[ACL.id].rule:
            #print rul.id
    if og in rul.id:
        #print og
        #return True
        q.append(True)
        return True
               #return true for continuous iteration
    #q.append(False)
    #return True
    #return False               #return false for flagging for removal
def find_in_ACLS(box, og, root, orphaned_og):
    """
    Function will iterate through the ACL's within device and return true if found (keep)
    and false if not found (remove)
    """
    flag = False
    q = []
    threads = []
    #with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
    #    root = ncs.maagic.get_root(t)
    #/ ncs:devices / device { svl-gem-joe-asa-fw1.cisco.com } / config / asa:access-list / access-list-id { jw_apt }
    for acl in root.devices.device[box].config.asa__access_list.access_list_id:
        for rul in root.devices.device[box].config.asa__access_list.access_list_id[acl.id].rule:
            t = threading.Thread(target=find_rule_in_ACL, args=(box, og, root, rul,q,))
            threads.append(t)

    for t in threads:
        t.start()
    #print threading.activeCount()
    for t in threads:
        t.join()
    if True not in q:
        print "false for " + acl.id
        orphaned_og.append(og)
    #print "true for " + acl.id
        #print acl.id
        #flag = find_rule_in_ACL(box, og, root, acl)
        #if flag:
            #break
    #return flag            #return true if found, false if not
def flag_ogs_in_box(box):
    """
    This function returns a list of object groups that are orphaned in that device.
    """
    orphaned_og = []
    threads = []
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        for ogtyp in root.devices.device[box].config.asa__object_group:
            for og in root.devices.device[box].config.asa__object_group[ogtyp]:
                t = threading.Thread(target=find_in_ACLS, args=(box, og.id, root,orphaned_og,))
                threads.append(t)

        for t in threads:
            t.start()
        #print threading.activeCount()
        for t in threads:
            t.join()

        #if not find_in_ACLS(box,og,root):
                    #print og.id
                    #orphaned_og.append(og.id)
    return orphaned_og

def flag_ogs_in_box_test(box):
    """
    This function uses threads to find the the object groups that need to be removed.
    """
    orphaned_og = []
    og_list = []
    acl_list = []
    banishment = []
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        rul_list = []
        for ogtyp in root.devices.device[box].config.asa__object_group:
            for og in root.devices.device[box].config.asa__object_group[ogtyp]:
                og_list.append(og.id)

        for acl in root.devices.device[box].config.asa__access_list.access_list_id:
            for rul in root.devices.device[box].config.asa__access_list.access_list_id[acl.id].rule:
                rul_list2 = []
                rul_list.append(rul)
                rul_list2.append(rul)
            acl_list.append(rul_list2)
    #print rul_list
    #print og_list

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1000)
    futures = []
    for og in list(set(og_list)):
        for acl in acl_list:
            thread = executor.submit(banish, og, banishment, acl)
            futures.append(thread)
    concurrent.futures.wait(futures)
    return list(set(banishment))

def banish(og, banishment, acl):
    """
    This function appends a object group to a list (banishment) if it is not found in an ACL rule. This function runs on threads.
    """
    for rule in acl:
        if og in rule:
            break
        else:
            banishment.append(og)

def flag_ogs_in_box_test2(box):
    """
    This function finds the object groups that need to be removed for a device (without using threads). It finds this by using set difference of the set of rules and the set of object groups.
    """
    orphaned_og = []
    og_list = []
    og_obj = []
    banishment = []
    b_obj =[]
    ret = {}

    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        rul_list = []
        for ogtyp in root.devices.device[box].config.asa__object_group:
            for og in root.devices.device[box].config.asa__object_group[ogtyp]:
                og_list.append(og.id)
                og_obj.append(og)
                print "OG:" og
                print "OG.id:" og.id


        for acl in root.devices.device[box].config.asa__access_list.access_list_id:
            for rul in root.devices.device[box].config.asa__access_list.access_list_id[acl.id].rule:
                rul_list.append(rul.id)
    og_list = set(og_list)
    rul_list = set(rul_list)

    for og in og_list.difference(rul_list):
        banishment.append(og)

    for i in og_obj:
        if i.id in banishment:
            #remove_ogs(box,i.id, str(i))
            print str(i)
            if str(i) in ret.keys():
                ret[str(i)].append(i.id)
            else:
                ret[str(i)] = [i.id]


    if not banishment:
        no_ogs_error(box)
    else:
        return ret

def print_ogs_to_remove(box):
    """
    This function prints the object groups to be removed before removing.
    """
    og_list = flag_ogs_in_box_test2(box)
    print "Devices to be removed in: ",box,"\n"
    for og in og_list:
        print og

def remove_ogs(box, og_id, og_type):
    """
    This function removes the orphaned object groups for each device.
    """
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        #del root.devices.device[box].config.asa__object_group[og_type][og_id]
        t.apply()

def no_ogs_error(box):
    """
    This function prints an error message if there are no object groups to be removed for a device.
    """
    print "Error: There are no object groups that need to be removed for device ",box,"."

if __name__ == "__main__":
    """
    This is calling two functions and checking how much time it takes to run them.
    """
    b = time.time()
    #print_ogs_to_remove('svl-gem-joe-asa-fw1.cisco.com')
    print flag_ogs_in_box_test2('svl-gem-joe-asa-fw1.cisco.com')
    af = time.time()
    print af-b

    b = time.time()
    flag_ogs_in_box_test('svl-gem-joe-asa-fw1.cisco.com')
    af = time.time()
    print af-b
