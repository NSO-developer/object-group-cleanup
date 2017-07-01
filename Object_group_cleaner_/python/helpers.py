"""
Module to contain common use functions
"""

import ncs

def build_device_list(input):
    """
    Function to turn all inputs into a list of device names
    """
    devices = []
    for item in input.inputs:
        if item.input_type == "device_group":
            with ncs.maapi.single_write_trans('ncsadmin', 'python', groups=['ncsadmin'], db=ncs.RUNNING, ip='127.0.0.1', port=ncs.NCS_PORT, proto=ncs.PROTO_TCP) as trans:
                root = ncs.maagic.get_root(trans)
                group = root.devices.device_group[item.value].device_name
                for box in group:
                    if box not in devices:
                        devices.append(box)
        elif item.input_type == "device":
            if item.value not in devices:
                devices.append(item.value)
        elif item.input_type == "csv":
            entries = item.value.split(",")
            for entry in entries:
                if entry not in devices:
                    devices.append(entry)
    return devices
