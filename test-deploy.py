import ncs
import sys
with ncs.maapi.Maapi() as m:
       with ncs.maapi.Session(m, 'gitlab-runner', 'python', ['ncsadmin'], src_ip='127.0.0.1', src_port=0, proto=ncs.PROTO_TCP, vendor=None, product=None, version=None, client_id=None):
           root = ncs.maagic.get_root(m)
           for package in (root.packages.reload().reload_result):
               print package.package, " ", package.result
               if package.result == False:
                   message = package.package + " Failed to reload. Build Failed."
                   sys.exit(message)
