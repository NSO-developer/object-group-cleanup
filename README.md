# NSO Object Clean Up Project

> Devloped by: NWS Interns Team

---
### Project Description
Our objective for this project is to write a script to remove unused object groups within network devices on NSO for use by Extranet. Our approach to solve this problem is by looking at the object groups per device and checking if each object group is present in access list. We will be using NSO's maapi python API to achieve this.

### Project Status
Project is currently in a 3 week sprint and development stage.
The main activities to be completed are:
1. Log the tools run-time trends and analytics
2. Optimize algorithm to run under 120 seconds
3. Develop a predefined set of test suites

### Brief Explanation
A tool that takes a device or device group as an input. It checks each of the device's object groups against the inputted device's access lists and removes the unused object groups. Each device will now only have the object groups that appear in the access lists.

---
## Dependencies
- NSO 4.4
- Python Libraries: ncs, socket, time

### Python Code
The python code inside our `obj_cleanup.py` handles multiple functions with multiple for loops that deletes the object groups from the device's object group list that are not found in any of the inputted device's access lists

```python
    for og, typ in zip(og_list, og_typ):
        for acl in acl_list:
            flag = banish(og, acl)
            if flag:
                break
        if not flag:
            if typ in ret.keys():
                ret[typ].append(og)
            else:
                ret[typ] = [og]
            del root.devices.device[box].config.asa__object_group[typ][og]
    t.apply()
return ret

```

### Yang model
The YANG model is the mapping brain behind the service. The YANG model defines what parameters will be used for the configuration. It also includes relevant service meta data and details for service operation.
The model has the following variables (leafs):
1. `Devices` (String) The ASAs to have the configuration applied to.
2. `start_time` (String): The time at which the tool was configured.
3. `end_time` (String): The time at which tool finished its configuration.
4. `run_time` (String): The total run time of the too to finish its configuration
5. `og_type` (String): Type of object_group outputted that will be removed from the devices object group list. Enumeration of the type can be icmp_type, network, service, or user.
6. `object_group` (String): Existing id of the object group being removed from the obejct group list.
7. `number_of_ogs_deleted` (int64): Total number of object groups removed from the object group list.
8. `stat` (int64): Generated from python. Number of object groups.
9. `device_name` (string) Name of the device

## Instructions
1. Clone this package (Object_group_cleaner) into your NSO server's or project's packages directory.
2. In your NSO's command line (ncs_cli -C), perform a packages reload.
3. Now the package will appear in the modules menu as Object_group_cleaner in your NSO's native web UI.
4. Choose one of the three tools: cleanup, search, or remove. Each have description pop ups when you hover your mouse over them.
5. Each of the above options will require device/device_group name, object_group type, and/or the object_group name as an additional input.

### Postman

---
### Outline
```
create a session with NSO
  get the NCS root object
    iterate through the devices
      iterate through the object groups(need to think about the type situation)
        iterate through access list
           check if obj group is in the access list
```
---
![meme](https://s-media-cache-ak0.pinimg.com/originals/1a/0e/75/1a0e758c3fcf69cfc12754edf4439bb4.jpg)
---
### Project Team Members
Brandon Black
Divyani Rao <br  />
Alyssa Sandore <br />
Rob Gonzalez <br />
Axel Perez
