import cif_orchestration_base
import time

#Set the IP address and port of the CIF manager on the target
server_ip = "localhost"
manager_port = "15882"

#Configuration for plugins including channel links  
RW_Example = cif_orchestration_base.plugin("RW_Example", "TagRW_Example_Plugin", "1.4.1")
DMMM = cif_orchestration_base.plugin("DMMM", "NI_DMM_Plugin", "1.2.1")
Monitor = cif_orchestration_base.plugin("Monitor", "Tag_Monitor_Plugin", "1.1.1")
Zenoh = cif_orchestration_base.plugin("Zenoh", "Zenoh_Plugin", "1.0.0")
link4 = cif_orchestration_base.channel_link("RW_Example.doubleout", "RW_Example.doublein2", "")

#Create connection to the CIF manager
cif_manager = cif_orchestration_base.cif_manager(server_ip, manager_port)

#Business logic (Load plugins, link channel, configure plugins, change state, etc)
cif_manager.load(RW_Example)
cif_manager.load(DMMM)
cif_manager.load(Monitor)
cif_manager.load(Zenoh)
RW_Example.connect_channel(link4)
RW_Example.run(wait_running=False)
print("-------------- Orchestration Complete --------------")