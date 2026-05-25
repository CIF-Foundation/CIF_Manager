"""gRPC helpers for CIF manager, plugin core, channel core, and tag monitor services."""
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
import cif_tag_monitor_plugin_pb2
import cif_tag_monitor_plugin_pb2_grpc
import struct  # big-endian payloads for SetForce match wire format expected by LabVIEW

class cif_manager():
    """Client for the CIF Manager gRPC service (load/query plugins, loaders, etc.)."""

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.manager_address = self.address + ":" + self.port  # host:port for gRPC channel
        self.stub = cif_manager_pb2_grpc.ManagerStub(grpc.insecure_channel(self.manager_address))  # cleartext; use TLS if exposed beyond localhost

    def load(self, plugin):
        # Check if plugin with this name is already loaded
        exists = self.check(plugin.name)
        if exists == False:
            # Manager spawns the loader/plugin; loader_process names which loader host to use
            result_info = self.stub.LoadPlugin(cif_manager_pb2.LoadPluginRequest(
                plugin_type=plugin.type, plugin_name=plugin.name, version=plugin.version, loader_process=plugin.loader))
            res = check_error(result_info.status)  # cif.common.Status: code 0 == success
            if res == 0:
                plugin.address = self.address
                plugin.connection = plugin_connection.NOT_CONNECTED  # port assigned after plugin registers
                plugin.cif_manager = self
                return plugin
        else:
            # Instance already present: sync host, stubs, and connection from latest QueryPlugin snapshot
            result_info = self.stub.QueryPlugin(cif_manager_pb2.QueryPluginRequest(plugin_name=plugin.name))
            plugin.address = self.address
            plugin.connection = plugin_connection.NOT_CONNECTED
            plugin.cif_manager = self
            if result_info.plugin_info.grpc_port != -1:  # -1 == not listening yet
                plugin.plugin_address = plugin.address + ":" + str(result_info.plugin_info.grpc_port)
                plugin.stub = cif_plugin_core_pb2_grpc.PluginCoreStub(grpc.insecure_channel(plugin.plugin_address))
                plugin.stub_channel = cif_channel_core_pb2_grpc.ChannelCoreStub(grpc.insecure_channel(plugin.plugin_address))  # same TCP port, different service
                plugin.connection = plugin_connection.CONNECTED
            return plugin

    def check(self, plugin_name):
        result_info = self.stub.QueryPluginInfo(cif_manager_pb2.QueryPluginInfoRequest())  # list all loaded plugins
        exists = any(p.plugin_name == plugin_name for p in result_info.plugin_info_array.plugin_info)
        return exists

class plugin_connection(Enum):
    """Local view of whether we have gRPC routes to the plugin process."""
    UNLOADED = 1
    NOT_CONNECTED = 2
    CONNECTED = 3

class plugin_state(Enum):
    """Lifecycle values align with cif.management_common.PluginStatusData.PluginState (0 = unknown)."""
    NULL = 0
    CREATING = 1
    LISTENING = 2
    RUNNING = 3
    CLEANINGUP = 4
    DESTROYING = 5

class plugin():
    """One plugin instance: manager metadata plus stubs to PluginCore / ChannelCore on the plugin port."""

    def __init__(self, name, type, version, loader):
        self.name = name  # unique instance name on the target
        self.type = type  # plugin type / class name
        self.version = version  # semver string sent to manager for version resolution
        self.loader = loader  # loader_process string (e.g. Default_LabVIEW)
        self.port = "unset"
        self.address = "unset"  # manager host; set when added via cif_manager.load
        self.plugin_address = "unset"  # manager_host:plugin_grpc_port when connected
        self.connection = plugin_connection.UNLOADED
        self.state = plugin_state.NULL  # last known lifecycle state from GetStatusData

    def check_loaded(self):
        """Ensure plugin gRPC stubs exist; poll manager while status.code == -9014 (still registering)."""
        if self.connection == plugin_connection.UNLOADED:
            print(f"{bcolors.WARNING}Plugin {self.name} has not been loaded. {bcolors.ENDC}")
            return self
        if self.connection == plugin_connection.NOT_CONNECTED:
            i = 0
            while i < 20:
              result_info = self.cif_manager.stub.QueryPlugin(cif_manager_pb2.QueryPluginRequest(plugin_name=self.name))
              if result_info.status.code != -9014:
                # Any code other than -9014: registration finished (success or error path)
                res = check_error(result_info.status)
                if result_info.plugin_info.grpc_port != -1:
                    self.plugin_address = self.address + ":" + str(result_info.plugin_info.grpc_port)
                    self.stub = cif_plugin_core_pb2_grpc.PluginCoreStub(grpc.insecure_channel(self.plugin_address))
                    self.stub_channel = cif_channel_core_pb2_grpc.ChannelCoreStub(grpc.insecure_channel(self.plugin_address))
                    self.connection = plugin_connection.CONNECTED
                    return self
              time.sleep (0.25)  # still at -9014: keep waiting for plugin to bind its gRPC port
              i += 1
              if i == 20:
                print(f"{bcolors.WARNING}Plugin {plugin.name} did not load before timeout. {bcolors.ENDC}")
                return self
        return self  

    def run(self, wait_running=False):
        self = self.check_loaded()
        result_info = self.stub.Start(cif_plugin_core_pb2.StartRequest())  # transition toward running/listening
        check_error(result_info.status)
        if wait_running == True:
            self = self.wait_on_running()  # poll GetStatusData until RUNNING or timeout
        return self
    
    def update_config(self, json):
        self = self.check_loaded()
        result_info = self.stub.UpdateConfig(cif_plugin_core_pb2.UpdateConfigRequest(
            configuration=cif_plugin_core_pb2.Configuration(json_config=json)))  # plugin parses JSON on target
        check_error(result_info.status)
        return self
    
    def connect_channel(self, channel_link):
        self = self.check_loaded()
        result_info = self.stub_channel.SetConnection(cif_channel_core_pb2.SetConnectionRequest(
            subscriber_name=channel_link.subscriber, publisher_name=channel_link.publisher, custom_connect=channel_link.custom_data))
        check_error(result_info.status)  # e.g. link validation errors surface here
        return self
    
    def create_fifo_instance(self, fifo_instance):
        self = self.check_loaded()
        test_value = 0  # unused
        result_info = self.stub_channel.CreateFIFOInstance(cif_channel_core_pb2.CreateFIFOInstanceRequest(
            publisher_name=fifo_instance.channel, retry_on_timeout=fifo_instance.backpressure,
            bytes_per_message_override=fifo_instance.bytes_per_msg,  # 0 = use publisher default
            message_per_fifo_override=fifo_instance.msg_per_fifo,  # depth in messages; 0 = default
            custom_data=fifo_instance.custom_data))
        check_error(result_info.status)
        return self
    
    def status(self):
        self = self.check_loaded()
        result_info = self.stub.GetStatusData(cif_plugin_core_pb2.GetStatusDataRequest())
        self.state = plugin_state(result_info.status_data.state)  # enum value aligns with plugin_state
        return self
    
    def wait_on_running(self, timeout_ms=2000):
        self = self.check_loaded()
        if self.connection == plugin_connection.NOT_CONNECTED:
            return self  # cannot poll plugin without gRPC route
        if self.connection == plugin_connection.CONNECTED:
            max_iteration = timeout_ms / 250  # 250 ms poll interval
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
        double_bytes = struct.pack('>d', force_data)  # IEEE754 double, network (big) endian
        result_info = self.stub_channel.SetForce(cif_channel_core_pb2.SetForceRequest(channel_name=channel_name, force=force, force_data=double_bytes))
        check_error(result_info.status)
        return self        
    
    def force_channel_i64(self, channel_name, force, force_data):
        self = self.check_loaded()
        i64_bytes = struct.pack('>q', force_data)  # signed 64-bit big endian
        result_info = self.stub_channel.SetForce(cif_channel_core_pb2.SetForceRequest(channel_name=channel_name, force=force, force_data=i64_bytes))
        check_error(result_info.status)
        return self  
    
    def force_channel_u64(self, channel_name, force, force_data):
        self = self.check_loaded()
        u64_bytes = struct.pack('>Q', force_data)  # unsigned 64-bit big endian
        result_info = self.stub_channel.SetForce(cif_channel_core_pb2.SetForceRequest(channel_name=channel_name, force=force, force_data=u64_bytes))
        check_error(result_info.status)
        return self 
    
    def monitor_tag(self, tag_list):
        self = self.check_loaded()
        self.stub_tagmon = cif_tag_monitor_plugin_pb2_grpc.TagMonitorStub(grpc.insecure_channel(self.plugin_address))  # tag monitor is optional plugin RPC
        result_info = self.stub_tagmon.GetDoubleTagValues(cif_tag_monitor_plugin_pb2.TagValueRequest(tags=tag_list))
        return result_info 
    
class channel_link():
    """Publisher/subscriber pair plus opaque bytes for loader-specific connection metadata."""

    def __init__(self, publisher, subscriber, custom_data):
        self.subscriber = subscriber
        self.publisher = publisher
        self.custom_data = bytes.fromhex(custom_data)  # hex string from orchestration script / LV

class fifo_instance():
    """Parameters for CreateFIFOInstance (multi-writer / backpressure FIFO paths)."""

    def __init__(self, direction, channel, backpressure, bytes_per_msg, msg_per_fifo, custom_data):
        self.direction = direction  # retained for scripting symmetry; not sent on this RPC
        self.channel = channel  # publisher FIFO name on target
        self.backpressure = int(backpressure)
        self.bytes_per_msg = int(bytes_per_msg)
        self.msg_per_fifo = int(msg_per_fifo)
        self.custom_data = bytes.fromhex(custom_data)

class bcolors:
    """ANSI terminal colors for local script output (no effect in plain Windows console)."""
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
    """Typed hint only; runtime uses protobuf Status (code, message) with the same shape."""
    message: str
    code: int

def check_error(result_error):
      """Print non-zero cif.common.Status and return 1 for failure, 0 for success."""
      if result_error.code != 0:
        print(f"{bcolors.FAIL} {result_error.message} {bcolors.ENDC}")
        return 1
      else:
        return 0