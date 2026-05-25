import cif_orchestration_base
import time

#Set the IP address and port of the CIF manager on the target
server_ip = "localhost"
manager_port = "15882"

#Configuration for plugins including channel links  
temp1 = cif_orchestration_base.plugin("temp1", "Template_Plugin", "1.0.0", "Default_LabVIEW")
temp12 = cif_orchestration_base.plugin("temp12", "Template_Plugin", "1.0.0", "Default_LabVIEW")
temp1_config1 = '{"Common":{"Period (s)":0.01,"Offset (us)":0,"Priority":100,"Processor":-2,"External Clock":{"ClockID":0,"Clock Name":"","Clock Source":false,"Convert Data Timestamps":false,"Use for Timing":false}},"Step":100}'

#Create connection to the CIF manager
cif_manager = cif_orchestration_base.cif_manager(server_ip, manager_port)

#Business logic (Load plugins, link channel, configure plugins, change state, etc)
cif_manager.load(temp1)
cif_manager.load(temp12)
temp1.update_config(temp1_config1)
temp1.run(wait_running=False)
temp12.run(wait_running=False)
print("-------------- Orchestration Complete --------------")