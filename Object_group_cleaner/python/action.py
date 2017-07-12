"""
NCS Action Package example.

Implements a package with actions
(C) 2015 Tail-f Systems
Permission to use this code as a starting point hereby granted

See the README file for more information
"""
from __future__ import print_function
import sys

# import your_audit_name_here # Copy and change this to the name of your Python File
import ncs
from datetime import datetime
import time
import _ncs
import _ncs.dp
from ncs.dp import Action
from ncs.application import Application
from _namespaces.Object_group_cleaner_ns import ns
import helpers
import obj_cleanup #make sure to put this in the python folder

DATE_FORMAT = "%H:%M:%S.%f"

class ActionHandler(Action):
    """This class implements the dp.Action class."""

    @Action.action
    def cb_action(self, uinfo, name, kp, input, output):
        """Called when the actionpoint is invoked.

        The function is called with:
            uinfo -- a UserInfo object
            name -- the tailf:action name (string)
            kp -- the keypath of the action (HKeypathRef)
            input -- input node (maagic.Node)
            output -- output node (maagic.Node)
        """
        #TODO determine logging standards
        self.log.info(uinfo.addr)
        self.log.info(uinfo.usid)
        self.log.info(uinfo.username)
        self.log.info("name: ", name)
        self.log.info("keypath: ", str(kp))

        start = (datetime.strptime(str(datetime.now().time()), DATE_FORMAT))
        output.start_time = time.strftime("%H:%M:%S")

        if name == "search_and_delete":
            count = 0
            devices = helpers.build_device_list(input)
            for device in devices:
                og_for_removal = obj_cleanup.search_and_destroy(device)
                for key in og_for_removal:
                    count = len(og_for_removal[key])
                self.log.info(count)
                for key, value in og_for_removal.items():
                    for og in value:
                        result = output.deleted_object_groups.create()
                        result.object_group = og
                        result.og_type = key
                        result.device = device
            output.number_of_ogs_deleted = count
            output.stat = "Success"

        elif name == "search":
            devices = helpers.build_device_list(input)
            #device = 'svl-gem-joe-asa-fw1.cisco.com'
            for device in devices:
                og_for_removal = obj_cleanup.flag_ogs_in_box_test(device)
                #og_for_removal = mock()
                for key, value in og_for_removal.items():
                    for og in value:
                        result = output.orphaned_object_groups.create()
                        result.object_group = og
                        result.og_type = key
                        result.device = device

        elif name == "remove":
            obj_groups = helpers.build_og_list(input)
            for obj in obj_groups:
                #obj[1] = "asa:" + obj[1]
                self.log.info(obj[1])
                obj_cleanup.remove_ogs(obj[0], obj[1], obj[2])
                result = output.deleted_object_groups.create()
                result.device = obj[0]
                result.og_type = obj[1]
                result.object_group = obj[2]
            output.stat = "Success"


        else:
            # Log & return general failures
            self.log.debug("got bad operation: {0}".format(name))
            return _ncs.CONFD_ERR

        end = (datetime.strptime(str(datetime.now().time()), DATE_FORMAT))
        output.end_time = time.strftime("%H:%M:%S")
        output.run_time = str(end-start)
        #



# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------


class Action(Application):
    """This class is referred to from the package-meta-data.xml."""
    # DO NOT CHANGE THIS INFORMATION

    def setup(self):
        """
        Setting up the action callback.
        This is used internally by NSO when NSO is re-started or packages a reloaded by NSO.
        """
        self.log.debug('action app start')
        self.register_action('Object_group_cleaner', ActionHandler, [])


def mock():
    """
    This is a mock function that returns a dictionary (or use a two dimensional list that has the og type
    and the og name). Use this function instead of our algorithm to perfect input and output on the web UI
    """
    mock_og = {}
    mock_og["icmp-type"] = []
    mock_og["network"] = ['GEM-OG:voip_hong_kong_ucce_tftp',
            'HOST:alli-prd-29.cisco.com',
            'gem_og_itst_prd_ports',
            'GHOST:nqs-hkg-h01-p.cisco.com',
            'HOST:rcdn-core2.cisco.com',
            'HOST:nqs-sjc-h06-p.cisco.com',
            'HOST:nqs-sjc-h06-p.cisco.com',
            'GEM-OG:tacacs',
            'common_host_1',
            'HOST:mfgtde-dev.cisco.com',
            'HOST:ees-singapore.cisco.com',
            'eman_networks-global-1']
    mock_og["service"] = ['GEM-OG:bts-view_servers',
            'HOST:wwwin-sso-prod3.cisco.com',
            'HOST:mail-aln.cisco.com',
            'HOST:alli-prd-27.cisco.com',
            'HOST:nqs-blr-h01-p.cisco.com',
            'HOST:sj5autotrack.cisco.com',
            'NDCS-OG:dmz_networks-sjc-1',
            'GEM-OG:intellectual_property',
            'GEM-OG:voip_rtp_campus_cucm',
            'gem_og_itst_prd_ports']
    mock_og["user"] = []

    return mock_og
