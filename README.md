# NSO Object Clean Up Project

### Objective
Our objective is to write a script to remove unused object groups. Our approach to solve this problem is by looking at the object groups per device and checking if each object group is present in access list. We will be using NSO's maapi python API to achieve this.

### Brief Explanation
A tool that takes a device or device group as an input. It checks each of the device's object groups against the inputted device's access lists and removes the unused object groups. Each device will now only have the object groups that appear in the access lists.

### Dependencies
- NSO 4.4
- Python Libraries: ncs, socket, time

### Instructions
1. Clone this package (Object_group_cleaner) into your NSO server's or project's packages directory.
2. In your NSO's command line (ncs_cli -C), perform a packages reload.
3. Now the package will appear in the modules menu as Object_group_cleaner in your NSO's native web UI.
4. Choose one of the three tools: cleanup, search, or remove. Each have description pop ups when you hover your mouse over them.


### Outline
```
create a session with NSO
  get the NCS root object
    iterate through the devices
      iterate through the object groups(need to think about the type situation)
        iterate through access list
           check if obj group is in the access list
```

### Discussion

1. Is there a way to actually see these obj group lists? or sample access list?
2. Can we do better than using a O(n^3) algorithm?
3. Are they sorted in any way?
4. Do we care about runtime/ space?

### Ideas
- may be store in a more efficient data structure
- sort that structure

### Project Team Members
Divyani Rao <br  />
Alyssa Sandore <br />
Rob Gonzalez <br />
Axel Perez
