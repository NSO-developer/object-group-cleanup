#!/bin/bash
source /etc/profile.d/ncs.sh
ncs-netsim create-network /var/opt/ncs/packages/cisco-ios 3 IOS-
ncs-netsim add-to-network /var/opt/ncs/packages/cisco-asa 2 ASA-
#ncs-setup --netsim-dir ./netsim --dest .
ncs-netsim start
/etc/init.d/ncs start
echo "Please enter your username again:"
read user
usermod -a -G ncsadmin $user
su - $user -c "python /ncs-app/packages_reload.py"
sleep 25
ncs --mergexmlfiles /ncs-app/devices_load.xml
passwd $user
su - $user -c "source /etc/profile.d/ncs.sh"
su - $user -c "ncs_cli -C"
/bin/bash
