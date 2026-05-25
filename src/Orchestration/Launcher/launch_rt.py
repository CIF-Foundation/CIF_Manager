#!/usr/bin/env python3
import re
import os

os.system("/etc/init.d/nilvrt stop")
file = open("/etc/natinst/share/lvrt.conf")
content = file.read()
# Check if the keys are present and if so update the values
content = re.sub('RTTarget.LaunchAppAtBoot=.+', 'RTTarget.LaunchAppAtBoot=True', content)
content = re.sub('RTTarget.ApplicationPath=.+', 'RTTarget.ApplicationPath=/usr/local/cif/manager/cif_startup.rtexe', content)
# Check if the keys are not present.  If missing add to the end
look = content.find("RTTarget.LaunchAppAtBoot=True")
if look == -1:
    content = content + "RTTarget.LaunchAppAtBoot=True\n"
look = content.find("RTTarget.ApplicationPath=/usr/local/cif/manager/cif_startup.rtexe")
if look == -1:
    content = content + "RTTarget.ApplicationPath=/usr/local/cif/manager/cif_startup.rtexe\n"
file.close()
# Write the data to the conf file
file = open("/etc/natinst/share/lvrt.conf", 'w')
file.write(content)
file.close()
os.system("/etc/init.d/nilvrt start")