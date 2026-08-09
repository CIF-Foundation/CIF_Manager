from enum import Enum
import grpc
import time
import re
import cif_manager_pb2
import cif_manager_pb2_grpc
import cif_plugin_core_pb2
import cif_plugin_core_pb2_grpc
import cif_channel_core_pb2
import cif_channel_core_pb2_grpc
import cif_common_pb2
import cif_common_pb2_grpc
import cif_tag_monitor_plugin_pb2
import cif_tag_monitor_plugin_pb2_grpc
import struct

class cif_manager():
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.manager_address = self.address + ":" + self.port
        self.stub = cif_manager_pb2_grpc.ManagerStub(grpc.insecure_channel(self.manager_address))

    def load(self, plugin):
        # Check if plugin with this name is already loaded
        exists = self.check(plugin.name)
        if exists == False:           
            # Not loaded.  Load the plugin on the system
            result_info = self.stub.LoadPlugin(cif_manager_pb2.PluginConfig(plugin_type=plugin.type, plugin_name=plugin.name, version=plugin.version))
            res = check_error(result_info)
            if res == 0:
                plugin.address = self.address
                plugin.connection = plugin_connection.NOT_CONNECTED
                plugin.cif_manager = self
                return plugin
        else:
            #Loaded.  Populate the plugin connection information
            result_info = self.stub.QueryPlugin(cif_manager_pb2.PluginName(plugin_name=plugin.name))
            plugin.address = self.address
            plugin.connection = plugin_connection.NOT_CONNECTED
            plugin.cif_manager = self
            if result_info.plugin_info.grpc_port != -1:
                plugin.plugin_address = plugin.address + ":" + str(result_info.plugin_info.grpc_port)
                plugin.stub = cif_plugin_core_pb2_grpc.PluginCoreStub(grpc.insecure_channel(plugin.plugin_address))
                plugin.stub_channel = cif_channel_core_pb2_grpc.ChannelCoreStub(grpc.insecure_channel(plugin.plugin_address))
                plugin.connection = plugin_connection.CONNECTED
            return plugin

    def check(self, plugin_name):
        result_info = self.stub.QueryPluginInfo(cif_manager_pb2.PluginName())
        exists = any(p.plugin_name == plugin_name for p in result_info.plugin_info)
        return exists

class plugin_connection(Enum):
    UNLOADED = 1
    NOT_CONNECTED = 2
    CONNECTED = 3

class plugin_state(Enum):
    NULL = 0
    CREATING = 1
    LISTENING = 2
    RUNNING = 3
    CLEANINGUP = 4
    DESTROYING = 5

class plugin():
    def __init__(self, name, type, version):
        self.name = name
        self.type = type
        self.version = version
        self.port = "unset"
        self.address = "unset"
        self.plugin_address = "unset"
        self.connection = plugin_connection.UNLOADED
        self.state = plugin_state.NULL

    def check_loaded(self):
        if self.connection == plugin_connection.UNLOADED:
            print(f"{bcolors.WARNING}Plugin {self.name} has not been loaded. {bcolors.ENDC}")
            return self
        if self.connection == plugin_connection.NOT_CONNECTED:
            i = 0
            while i < 20:
              result_info = self.cif_manager.stub.QueryPlugin(cif_manager_pb2.PluginName(plugin_name=self.name))
              res = check_error(result_info.status)
              if res != 0:
                return self
              if result_info.plugin_info.grpc_port != -1:
                self.plugin_address = self.address + ":" + str(result_info.plugin_info.grpc_port)
                self.stub = cif_plugin_core_pb2_grpc.PluginCoreStub(grpc.insecure_channel(self.plugin_address))
                self.stub_channel = cif_channel_core_pb2_grpc.ChannelCoreStub(grpc.insecure_channel(self.plugin_address))
                self.connection = plugin_connection.CONNECTED
                return self
              time.sleep (0.25)
              i += 1
              if i == 20:
                print(f"{bcolors.WARNING}Plugin {plugin.name} did not load before timeout. {bcolors.ENDC}")
                return self
        return self  

    def run(self, wait_running=False):
        self = self.check_loaded()
        result_info = self.stub.Start(cif_common_pb2.Status())
        check_error(result_info)
        if wait_running == True:
            self = self.wait_on_running()
        return self
    
    def update_config(self, json):
        self = self.check_loaded()
        result_info = self.stub.UpdateConfig(cif_plugin_core_pb2.Configuration(json_config=json))
        check_error(result_info)
        return self
    
    def connect_channel(self, channel_link):
        self = self.check_loaded()
        result_info = self.stub_channel.SetConnection(cif_channel_core_pb2.ConnectSubscriber(subscriber_name=channel_link.subscriber, publisher_name=channel_link.publisher, custom_connect=channel_link.custom_data))
        check_error(result_info)
        return self
    
    def create_fifo_instance(self, fifo_instance):
        self = self.check_loaded()
        test_value = 0
        result_info = self.stub_channel.CreateFIFOInstance(cif_channel_core_pb2.FIFOInstance(
            publisher_name=fifo_instance.channel, retry_on_timeout=fifo_instance.backpressure,
            message_per_fifo_override=fifo_instance.msg_per_fifo, custom_data=fifo_instance.custom_data))
        check_error(result_info.status)
        return self
    
    def status(self):
        self = self.check_loaded()
        result_info = self.stub.GetStatusData(cif_common_pb2.Empty())
        self.state = plugin_state(result_info.state)
        return self
    
    def wait_on_running(self, timeout_ms=2000):
        self = self.check_loaded()
        if self.connection == plugin_connection.NOT_CONNECTED:
            return self
        if self.connection == plugin_connection.CONNECTED:
            max_iteration = timeout_ms / 250
            i = 0
            while i < max_iteration:
              self = self.status()
              if self.state==plugin_state.RUNNING:
                return self
              time.sleep (0.25)
              i += 1
              if i == max_iteration:
                print(f"{bcolors.WARNING}Plugin {plugin.name} did not change to running state before timeout. {bcolors.ENDC}")
                return self

    def force_channel_double(self, channel_name, force, force_data):
        self = self.check_loaded()
        double_bytes = struct.pack('>d', force_data)
        # print(f"Sending bytes: {double_bytes.hex()}")
        result_info = self.stub_channel.SetForce(cif_channel_core_pb2.ForceChannel(channel_name=channel_name, force=force, force_data=double_bytes))
        check_error(result_info)
        return self        
    
    def force_channel_i64(self, channel_name, force, force_data):
        self = self.check_loaded()
        i64_bytes = struct.pack('>q', force_data)
        # print(f"Sending bytes: {i64_bytes.hex()}")
        result_info = self.stub_channel.SetForce(cif_channel_core_pb2.ForceChannel(channel_name=channel_name, force=force, force_data=i64_bytes))
        check_error(result_info)
        return self  
    
    def force_channel_u64(self, channel_name, force, force_data):
        self = self.check_loaded()
        u64_bytes = struct.pack('>Q', force_data)
        # print(f"Sending bytes: {u64_bytes.hex()}")
        result_info = self.stub_channel.SetForce(cif_channel_core_pb2.ForceChannel(channel_name=channel_name, force=force, force_data=u64_bytes_bytes))
        check_error(result_info)
        return self 
    
    def monitor_tag(self, tag_list):
        self = self.check_loaded()
        self.stub_tagmon = cif_tag_monitor_plugin_pb2_grpc.TagMonitorStub(grpc.insecure_channel(self.plugin_address))
        result_info = self.stub_tagmon.GetDoubleTagValues(cif_tag_monitor_plugin_pb2.TagValueRequest (tags=tag_list))
        # print(result_info.tag_values[0])
        return result_info 
    
class channel_link():
    def __init__(self, publisher, subscriber, custom_data):
        self.subscriber = subscriber
        self.publisher = publisher
        self.custom_data = bytes.fromhex(custom_data)  

class fifo_instance():
    def __init__(self, direction, channel, backpressure, bytes_per_msg, msg_per_fifo, custom_data):
        self.direction = direction
        self.channel = channel
        self.backpressure = int(backpressure)
        self.bytes_per_msg = int(bytes_per_msg)
        self.msg_per_fifo = int(msg_per_fifo)
        self.custom_data = bytes.fromhex(custom_data)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class result_error():
    message: str
    code: int

def check_error(result_error):
      if result_error.code != 0:
        print(f"{bcolors.FAIL} {result_error.message} {bcolors.ENDC}")
        return 1
      else:
        return 0