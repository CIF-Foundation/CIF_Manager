# Import CIF orchestration helpers.
# RT install: postinst writes /usr/local/cif/orchestrations/Python into a python3
#   site-packages .pth file (cif_orchestration.pth), so imports work without sys.path.
# Windows install: use the default Public Documents path below when .pth is not present.
try:
    import cif_orchestration_base
except ImportError:
    import sys
    sys.path.append(r"C:\Users\Public\Documents\CIF\orchestrations\Python")
    import cif_orchestration_base

import time

#Set the IP address and port of the CIF manager on the target
server_ip = "192.168.1.160"
manager_port = "15882"

#Configuration for plugins including channel links  
tagmon = cif_orchestration_base.plugin("tagmon", "Tag_Monitor_Plugin", "")
tagrw = cif_orchestration_base.plugin("tagrw", "TagRW_Example_Plugin", "")
tagrw2 = cif_orchestration_base.plugin("tagrw2", "TagRW_Example_Plugin", "")
fifo1 = cif_orchestration_base.fifo_instance("add", "tagrw2.u8array_out", "0", "0", "0", "01234506")
link1 = cif_orchestration_base.channel_link("tagrw2.u8array_out", "tagrw.u8array_in", "")
tagrw_config1 = '{"Common":{"Period (s)":0.001,"Offset (us)":0,"ClockID":0,"Priority":100,"Processor":-2},"Step":100}'

#Create connection to the CIF manager
cif_manager = cif_orchestration_base.cif_manager(server_ip, manager_port)

#Business logic (Load plugins, link channel, configure plugins, change state, etc)

cif_manager.load(tagmon)

cif_manager.load(tagrw)
cif_manager.load(tagrw2)
tagrw.force_channel_double("tagrw.doublein1", True, 1.1)
tagrw.force_channel_double("tagrw.doublein2", True, 2)
# temp2.create_fifo_instance(fifo1)
# temp1.connect_channel(link1)
tagrw.run(wait_running=True)
tagmon.run(wait_running=True)
value = tagmon.monitor_tag(["tagrw.doubleout"])
print (value.tag_values[0])


# tagrw.update_config(tagrw_config1)
print("-------------- Mischief Managed --------------")