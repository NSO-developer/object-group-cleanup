import ncs
import socket



def search_and_destroy(box):
    """
    A function that deletes the object groups from the device's object group
    list that are not found in any of the inputted device's access lists
    """
    #Initializing python lists
    og_list = []
    og_typ = []
    acl_list = []
    ret = {}
    empty = True

    #Creating transaction and setting root to access NSO
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        #Adding all of the object groups and their types to python lists
        for ogtyp in root.devices.device[box].config.asa__object_group:
            for og in root.devices.device[box].config.asa__object_group[ogtyp]:
                og_list.append(og.id)
                og_typ.append(str(og))      #str(og) is the object group type

        #Adding each access list's rules to a python list (temp_rul_list) and
        #then adding those lists as elements of another python list (acl_list)
        for acl in root.devices.device[box].config.asa__access_list.access_list_id:
            temp_rul_list = []
            for rul in root.devices.device[box].config.asa__access_list.access_list_id[acl.id].rule:
                if "object-group" in rul.id:
                    temp_rul_list.append(rul.id)
            acl_list.append(temp_rul_list)

        #Iterating through both object group and object group type lists simultaneously
        for og, typ in zip(og_list, og_typ):
            flag = 0
            for acl in acl_list:
                #flag indicates whether og was found in an access list
                for rule in acl:
                    if og in rule:
                        flag = 1
                        break
                #If found, continue to the next object group
                if flag:
                    break
            #If not found in any of the access lists, delete from object group list
            #and add to dictionary
            if not flag:
                if empty:
                    empty = False
                #If key has been created already, add og to key
                if typ in ret.keys():
                    ret[typ].append(og)
                #Else, create key and append og
                else:
                    ret[typ] = [og]
                del root.devices.device[box].config.asa__object_group[typ][og]

        try:
            t.apply()
            stat = "Success"
        #Provides error message if there is a problem removing an OG
        except:
            stat = "Error Removing"

        #Provides an error message if there are no object groups to be removed for a device
        if empty:
            stat = "No Object Groups to Remove"
    return ret, stat



def flag_ogs_in_box_test(box):
    """
    A function that returns a dictionary of the object groups that are not found
    in any of the inputted device's access lists, organized by object group type.
    """

    #Initializing python lists and flags
    og_list = []
    og_typ = []
    acl_list = []
    ret = {}
    empty = True

    #Creating transaction and setting root to access NSO
    with ncs.maapi.single_read_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)
        #Adding all of the object groups and their types to python lists
        for ogtyp in root.devices.device[box].config.asa__object_group:
            for og in root.devices.device[box].config.asa__object_group[ogtyp]:
                og_list.append(og.id)
                og_typ.append(str(og))      #str(og) is the object group type

        #Adding each access list's rules to a python list (temp_rul_list) and
        #then adding those lists as elements of another python list (acl_list)
        for acl in root.devices.device[box].config.asa__access_list.access_list_id:
            temp_rul_list = []
            for rul in root.devices.device[box].config.asa__access_list.access_list_id[acl.id].rule:
                if "object-group" in rul.id:
                    temp_rul_list.append(rul.id)
            acl_list.append(temp_rul_list)

    #Iterating through both object group and object group type lists simultaneously
    for og, typ in zip(og_list, og_typ):
        #flag indicates whether og was found in an access list
        flag = 0
        for acl in acl_list:
            #Iterates through the rules of an acl list
            for rule in acl:
                if og in rule:
                    flag = 1
                    break
            #flag = banish(og, acl)
            #If found, continue to the next object group
            if flag:
                break
        #If not found in any of the access lists, add to the dictionary
        if not flag:
            if empty:
                empty = False
            #If key has been created already, add og to key
            if typ in ret.keys():
                ret[typ].append(og)
            #Else, create key and append og
            else:
                ret[typ] = [og]

    if empty:
        stat = "No Orphaned Object Groups"
    else:
        stat = "Success"

    return ret, stat

def banish(og, acl):
    """
    A function that iterates through the rules of an acl list checking for the
    object group name within the rule. If found, the function returns true. If
    not found, function returns false.
    """
    for rule in acl:
        if og in rule:
            return True
    return False

def remove_ogs(obj_groups):
    """
    A function that removes the object group from the object group list using
    the arguments passed: device name, object group name, and object group type.
    """
    with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin']) as t:
        root = ncs.maagic.get_root(t)

        for obj in obj_groups:
            
        del root.devices.device[box].config.asa__object_group[og_type][og_id]
        try:
            t.apply()
            stat = "Success"
        except:
            stat = "Error Removing"

    return stat


def no_ogs_error(box):
    """
    This function prints an error message if there are no object groups to be removed for a device.
    """
    print "Error: There are no object groups that need to be removed for device ",box,"."
