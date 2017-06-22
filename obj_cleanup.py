#UNTESTED CODE

import ncs
import socket

with ncs.maapi.Maapi() as m:
       with ncs.maapi.Session(m, 'admin', 'python', ['ncsadmin'], src_ip='127.0.0.1', src_port=0, proto=ncs.PROTO_TCP, vendor=None, product=None, version=None, client_id=None):
           root = ncs.maagic.get_root(m)
           for box in (root.devices.device):                                                       #iterate through devices
               print (device.name, ": ", device.platform.model)
               for obj in root.devices.device[box.name].config._object-group:                       #iterate through object list
                   for acl in root.devices.device[box.name].config.ip.access_list.extended.ext_named_acl:  #look in access list
                        print (acl.name)
                        if obj not in acl:
                            del obj
