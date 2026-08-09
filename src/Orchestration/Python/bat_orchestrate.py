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
server_ip = "192.168.1.155"
manager_port = "15882"

#Configuration for plugins including channel links  
Bat_Cap = cif_orchestration_base.plugin("Bat_Cap", "Battery_Capacity_Plugin", "1.0.0")
Measure_Power = cif_orchestration_base.plugin("Measure_Power", "NI_RM26999_Plugin", "1.0.1")
fifo1 = cif_orchestration_base.fifo_instance("add", "Measure_Power.V_I Waveform", "0", "0", "0", "")
link1 = cif_orchestration_base.channel_link("Measure_Power.V_I Waveform", "Bat_Cap.V_I_Waveform", "")
Measure_Power_config1 = '{"Common":{"Period (s)":0.20000000000000001,"Offset (us)":0,"Priority":100,"Processor":-2,"External Clock":{"ClockID":0,"Clock Name":"","Publish Clock":false,"Convert Data Timestamps":false,"Plugin Timing Source":false}},"Device Name":"PXI1Slot2","Device Connector":0,"Sample Rate (Hz)":1000000,"Samples per Channel":100000,"Channel Configuration":[{"Max Voltage (V)":2000,"Current Sensor":{"Current Sensor":2,"Max Current (A)":599.999999999999999,"Custom Sensor Scaling":{"Input":0,"Output":0,"Output Units":0,"Shunt Resistor (Ohms)":0}}},{"Max Voltage (V)":2000,"Current Sensor":{"Current Sensor":2,"Max Current (A)":599.999999999999999,"Custom Sensor Scaling":{"Input":0,"Output":0,"Output Units":0,"Shunt Resistor (Ohms)":0}}},{"Max Voltage (V)":2000,"Current Sensor":{"Current Sensor":2,"Max Current (A)":599.999999999999999,"Custom Sensor Scaling":{"Input":0,"Output":0,"Output Units":0,"Shunt Resistor (Ohms)":0}}},{"Max Voltage (V)":2000,"Current Sensor":{"Current Sensor":2,"Max Current (A)":599.999999999999999,"Custom Sensor Scaling":{"Input":0,"Output":0,"Output Units":0,"Shunt Resistor (Ohms)":0}}}]}'

#Create connection to the CIF manager
cif_manager = cif_orchestration_base.cif_manager(server_ip, manager_port)

#Business logic (Load plugins, link channel, configure plugins, change state, etc)
cif_manager.load(Bat_Cap)
cif_manager.load(Measure_Power)
Measure_Power.create_fifo_instance(fifo1)
Bat_Cap.connect_channel(link1)
Measure_Power.update_config(Measure_Power_config1)
Measure_Power.run(wait_running=False)
Bat_Cap.run(wait_running=False)
print("-------------- Orchestration Complete --------------")