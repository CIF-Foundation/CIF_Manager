import cif_common_pb2 as _cif_common_pb2
import cif_management_common_pb2 as _cif_management_common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrchestrationLanguage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ORCHESTRATIONLANGUAGE_UNKNOWN: _ClassVar[OrchestrationLanguage]
    ORCHESTRATIONLANGUAGE_PYTHON: _ClassVar[OrchestrationLanguage]
ORCHESTRATIONLANGUAGE_UNKNOWN: OrchestrationLanguage
ORCHESTRATIONLANGUAGE_PYTHON: OrchestrationLanguage

class LoadPluginRequest(_message.Message):
    __slots__ = ("plugin_type", "plugin_name", "version", "loader_process")
    PLUGIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    LOADER_PROCESS_FIELD_NUMBER: _ClassVar[int]
    plugin_type: str
    plugin_name: str
    version: str
    loader_process: str
    def __init__(self, plugin_type: _Optional[str] = ..., plugin_name: _Optional[str] = ..., version: _Optional[str] = ..., loader_process: _Optional[str] = ...) -> None: ...

class LoadPluginResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class RegisterPluginRequest(_message.Message):
    __slots__ = ("plugin_name", "grpc_port", "plugin_version")
    PLUGIN_NAME_FIELD_NUMBER: _ClassVar[int]
    GRPC_PORT_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_VERSION_FIELD_NUMBER: _ClassVar[int]
    plugin_name: str
    grpc_port: int
    plugin_version: _cif_common_pb2.ShortVersion
    def __init__(self, plugin_name: _Optional[str] = ..., grpc_port: _Optional[int] = ..., plugin_version: _Optional[_Union[_cif_common_pb2.ShortVersion, _Mapping]] = ...) -> None: ...

class RegisterPluginResponse(_message.Message):
    __slots__ = ("loader_name",)
    LOADER_NAME_FIELD_NUMBER: _ClassVar[int]
    loader_name: str
    def __init__(self, loader_name: _Optional[str] = ...) -> None: ...

class UnregisterPluginRequest(_message.Message):
    __slots__ = ("plugin_name", "unregister_channels")
    PLUGIN_NAME_FIELD_NUMBER: _ClassVar[int]
    UNREGISTER_CHANNELS_FIELD_NUMBER: _ClassVar[int]
    plugin_name: str
    unregister_channels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, plugin_name: _Optional[str] = ..., unregister_channels: _Optional[_Iterable[str]] = ...) -> None: ...

class UnregisterPluginResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryPluginTypesRequest(_message.Message):
    __slots__ = ("reload",)
    RELOAD_FIELD_NUMBER: _ClassVar[int]
    reload: bool
    def __init__(self, reload: bool = ...) -> None: ...

class QueryPluginTypesResponse(_message.Message):
    __slots__ = ("plugin_types",)
    PLUGIN_TYPES_FIELD_NUMBER: _ClassVar[int]
    plugin_types: _containers.RepeatedCompositeFieldContainer[PluginType]
    def __init__(self, plugin_types: _Optional[_Iterable[_Union[PluginType, _Mapping]]] = ...) -> None: ...

class AbortPluginRequest(_message.Message):
    __slots__ = ("plugin_name",)
    PLUGIN_NAME_FIELD_NUMBER: _ClassVar[int]
    plugin_name: str
    def __init__(self, plugin_name: _Optional[str] = ...) -> None: ...

class AbortPluginResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class AbortAllPluginsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class AbortAllPluginsResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class DestroyRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DestroyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PingRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PingResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class QueryErrorsRequest(_message.Message):
    __slots__ = ("query_settings",)
    QUERY_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    query_settings: QuerySettings
    def __init__(self, query_settings: _Optional[_Union[QuerySettings, _Mapping]] = ...) -> None: ...

class QueryErrorsResponse(_message.Message):
    __slots__ = ("error_info_list",)
    ERROR_INFO_LIST_FIELD_NUMBER: _ClassVar[int]
    error_info_list: ErrorInfoList
    def __init__(self, error_info_list: _Optional[_Union[ErrorInfoList, _Mapping]] = ...) -> None: ...

class QueryConfigRequest(_message.Message):
    __slots__ = ("query_settings",)
    QUERY_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    query_settings: QuerySettings
    def __init__(self, query_settings: _Optional[_Union[QuerySettings, _Mapping]] = ...) -> None: ...

class QueryConfigResponse(_message.Message):
    __slots__ = ("file_data",)
    FILE_DATA_FIELD_NUMBER: _ClassVar[int]
    file_data: FileData
    def __init__(self, file_data: _Optional[_Union[FileData, _Mapping]] = ...) -> None: ...

class QueryInfoRequest(_message.Message):
    __slots__ = ("query_settings",)
    QUERY_SETTINGS_FIELD_NUMBER: _ClassVar[int]
    query_settings: QuerySettings
    def __init__(self, query_settings: _Optional[_Union[QuerySettings, _Mapping]] = ...) -> None: ...

class QueryInfoResponse(_message.Message):
    __slots__ = ("file_data",)
    FILE_DATA_FIELD_NUMBER: _ClassVar[int]
    file_data: FileData
    def __init__(self, file_data: _Optional[_Union[FileData, _Mapping]] = ...) -> None: ...

class ResetErrorIndexRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResetErrorIndexResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class ResetConfigIndexRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResetConfigIndexResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class ResetInfoIndexRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResetInfoIndexResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class QueryPluginInfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryPluginInfoResponse(_message.Message):
    __slots__ = ("plugin_info_array",)
    PLUGIN_INFO_ARRAY_FIELD_NUMBER: _ClassVar[int]
    plugin_info_array: PluginInfoArray
    def __init__(self, plugin_info_array: _Optional[_Union[PluginInfoArray, _Mapping]] = ...) -> None: ...

class QueryPluginRequest(_message.Message):
    __slots__ = ("plugin_name",)
    PLUGIN_NAME_FIELD_NUMBER: _ClassVar[int]
    plugin_name: str
    def __init__(self, plugin_name: _Optional[str] = ...) -> None: ...

class QueryPluginResponse(_message.Message):
    __slots__ = ("plugin_info", "status")
    PLUGIN_INFO_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    plugin_info: PluginInfo
    status: _cif_common_pb2.Status
    def __init__(self, plugin_info: _Optional[_Union[PluginInfo, _Mapping]] = ..., status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class QuerySystemStatusRequest(_message.Message):
    __slots__ = ("plugin_status",)
    PLUGIN_STATUS_FIELD_NUMBER: _ClassVar[int]
    plugin_status: PluginStatus
    def __init__(self, plugin_status: _Optional[_Union[PluginStatus, _Mapping]] = ...) -> None: ...

class QuerySystemStatusResponse(_message.Message):
    __slots__ = ("system_status",)
    SYSTEM_STATUS_FIELD_NUMBER: _ClassVar[int]
    system_status: SystemStatus
    def __init__(self, system_status: _Optional[_Union[SystemStatus, _Mapping]] = ...) -> None: ...

class UpdateClockRequest(_message.Message):
    __slots__ = ("clock_id", "timestamp_pair", "reinit", "clock_name")
    CLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_PAIR_FIELD_NUMBER: _ClassVar[int]
    REINIT_FIELD_NUMBER: _ClassVar[int]
    CLOCK_NAME_FIELD_NUMBER: _ClassVar[int]
    clock_id: int
    timestamp_pair: TimePair
    reinit: bool
    clock_name: str
    def __init__(self, clock_id: _Optional[int] = ..., timestamp_pair: _Optional[_Union[TimePair, _Mapping]] = ..., reinit: bool = ..., clock_name: _Optional[str] = ...) -> None: ...

class UpdateClockResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class CreateOrchRequest(_message.Message):
    __slots__ = ("start_timestamp", "create_file", "orchestration_language", "filename", "default_ip")
    START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CREATE_FILE_FIELD_NUMBER: _ClassVar[int]
    ORCHESTRATION_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_IP_FIELD_NUMBER: _ClassVar[int]
    start_timestamp: int
    create_file: bool
    orchestration_language: OrchestrationLanguage
    filename: str
    default_ip: str
    def __init__(self, start_timestamp: _Optional[int] = ..., create_file: bool = ..., orchestration_language: _Optional[_Union[OrchestrationLanguage, str]] = ..., filename: _Optional[str] = ..., default_ip: _Optional[str] = ...) -> None: ...

class CreateOrchResponse(_message.Message):
    __slots__ = ("orchestration_script", "status")
    ORCHESTRATION_SCRIPT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    orchestration_script: str
    status: _cif_common_pb2.Status
    def __init__(self, orchestration_script: _Optional[str] = ..., status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class QueryClockStatusRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryClockStatusResponse(_message.Message):
    __slots__ = ("clock_status_array",)
    CLOCK_STATUS_ARRAY_FIELD_NUMBER: _ClassVar[int]
    clock_status_array: ClockStatusArray
    def __init__(self, clock_status_array: _Optional[_Union[ClockStatusArray, _Mapping]] = ...) -> None: ...

class QueryAllChannelsRequest(_message.Message):
    __slots__ = ("channel_filter",)
    CHANNEL_FILTER_FIELD_NUMBER: _ClassVar[int]
    channel_filter: _cif_management_common_pb2.ChannelFilter
    def __init__(self, channel_filter: _Optional[_Union[_cif_management_common_pb2.ChannelFilter, _Mapping]] = ...) -> None: ...

class QueryAllChannelsResponse(_message.Message):
    __slots__ = ("channels",)
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    channels: _cif_management_common_pb2.Channels
    def __init__(self, channels: _Optional[_Union[_cif_management_common_pb2.Channels, _Mapping]] = ...) -> None: ...

class RegisterPluginLoaderRequest(_message.Message):
    __slots__ = ("loader_info",)
    LOADER_INFO_FIELD_NUMBER: _ClassVar[int]
    loader_info: _cif_management_common_pb2.LoaderInfoFull
    def __init__(self, loader_info: _Optional[_Union[_cif_management_common_pb2.LoaderInfoFull, _Mapping]] = ...) -> None: ...

class RegisterPluginLoaderResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CreatePluginLoaderRequest(_message.Message):
    __slots__ = ("loader_info",)
    LOADER_INFO_FIELD_NUMBER: _ClassVar[int]
    loader_info: _cif_management_common_pb2.LoaderInfo
    def __init__(self, loader_info: _Optional[_Union[_cif_management_common_pb2.LoaderInfo, _Mapping]] = ...) -> None: ...

class CreatePluginLoaderResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class DestroyPluginLoaderRequest(_message.Message):
    __slots__ = ("loader_name",)
    LOADER_NAME_FIELD_NUMBER: _ClassVar[int]
    loader_name: str
    def __init__(self, loader_name: _Optional[str] = ...) -> None: ...

class DestroyPluginLoaderResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class UnregisterPluginLoaderRequest(_message.Message):
    __slots__ = ("loader_name",)
    LOADER_NAME_FIELD_NUMBER: _ClassVar[int]
    loader_name: str
    def __init__(self, loader_name: _Optional[str] = ...) -> None: ...

class UnregisterPluginLoaderResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryPluginLoadersRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class QueryPluginLoadersResponse(_message.Message):
    __slots__ = ("plugin_loaders_info",)
    PLUGIN_LOADERS_INFO_FIELD_NUMBER: _ClassVar[int]
    plugin_loaders_info: _containers.RepeatedCompositeFieldContainer[_cif_management_common_pb2.LoaderInfoFull]
    def __init__(self, plugin_loaders_info: _Optional[_Iterable[_Union[_cif_management_common_pb2.LoaderInfoFull, _Mapping]]] = ...) -> None: ...

class PluginType(_message.Message):
    __slots__ = ("plugin_type", "plugin_version", "plugin_metadata", "relative_path")
    PLUGIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_VERSION_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_METADATA_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_PATH_FIELD_NUMBER: _ClassVar[int]
    plugin_type: str
    plugin_version: _cif_common_pb2.ShortVersion
    plugin_metadata: _cif_management_common_pb2.PluginMetadata
    relative_path: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, plugin_type: _Optional[str] = ..., plugin_version: _Optional[_Union[_cif_common_pb2.ShortVersion, _Mapping]] = ..., plugin_metadata: _Optional[_Union[_cif_management_common_pb2.PluginMetadata, _Mapping]] = ..., relative_path: _Optional[_Iterable[str]] = ...) -> None: ...

class ErrorInfoList(_message.Message):
    __slots__ = ("error_info",)
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    error_info: _containers.RepeatedCompositeFieldContainer[ErrorInfo]
    def __init__(self, error_info: _Optional[_Iterable[_Union[ErrorInfo, _Mapping]]] = ...) -> None: ...

class ErrorInfo(_message.Message):
    __slots__ = ("error_status", "error_code", "plugin", "time", "message", "location")
    ERROR_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    error_status: bool
    error_code: int
    plugin: str
    time: str
    message: str
    location: str
    def __init__(self, error_status: bool = ..., error_code: _Optional[int] = ..., plugin: _Optional[str] = ..., time: _Optional[str] = ..., message: _Optional[str] = ..., location: _Optional[str] = ...) -> None: ...

class QuerySettings(_message.Message):
    __slots__ = ("query_all",)
    QUERY_ALL_FIELD_NUMBER: _ClassVar[int]
    query_all: bool
    def __init__(self, query_all: bool = ...) -> None: ...

class FileData(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: str
    def __init__(self, data: _Optional[str] = ...) -> None: ...

class PluginInfo(_message.Message):
    __slots__ = ("plugin_name", "plugin_type", "grpc_port", "plugin_version", "status", "loader_info")
    PLUGIN_NAME_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    GRPC_PORT_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_VERSION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LOADER_INFO_FIELD_NUMBER: _ClassVar[int]
    plugin_name: str
    plugin_type: str
    grpc_port: int
    plugin_version: _cif_common_pb2.ShortVersion
    status: _cif_management_common_pb2.PluginStatusData
    loader_info: _cif_management_common_pb2.LoaderInfo
    def __init__(self, plugin_name: _Optional[str] = ..., plugin_type: _Optional[str] = ..., grpc_port: _Optional[int] = ..., plugin_version: _Optional[_Union[_cif_common_pb2.ShortVersion, _Mapping]] = ..., status: _Optional[_Union[_cif_management_common_pb2.PluginStatusData, _Mapping]] = ..., loader_info: _Optional[_Union[_cif_management_common_pb2.LoaderInfo, _Mapping]] = ...) -> None: ...

class PluginInfoArray(_message.Message):
    __slots__ = ("plugin_info",)
    PLUGIN_INFO_FIELD_NUMBER: _ClassVar[int]
    plugin_info: _containers.RepeatedCompositeFieldContainer[PluginInfo]
    def __init__(self, plugin_info: _Optional[_Iterable[_Union[PluginInfo, _Mapping]]] = ...) -> None: ...

class PluginStatus(_message.Message):
    __slots__ = ("pluginname", "status", "channels")
    PLUGINNAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    pluginname: str
    status: _cif_management_common_pb2.PluginStatusData
    channels: _cif_management_common_pb2.Channels
    def __init__(self, pluginname: _Optional[str] = ..., status: _Optional[_Union[_cif_management_common_pb2.PluginStatusData, _Mapping]] = ..., channels: _Optional[_Union[_cif_management_common_pb2.Channels, _Mapping]] = ...) -> None: ...

class TimePair(_message.Message):
    __slots__ = ("system_time", "external_time")
    SYSTEM_TIME_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_TIME_FIELD_NUMBER: _ClassVar[int]
    system_time: int
    external_time: int
    def __init__(self, system_time: _Optional[int] = ..., external_time: _Optional[int] = ...) -> None: ...

class ClockConversion(_message.Message):
    __slots__ = ("clock_id", "last_reset", "slope", "offset_pair", "clock_name")
    CLOCK_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_RESET_FIELD_NUMBER: _ClassVar[int]
    SLOPE_FIELD_NUMBER: _ClassVar[int]
    OFFSET_PAIR_FIELD_NUMBER: _ClassVar[int]
    CLOCK_NAME_FIELD_NUMBER: _ClassVar[int]
    clock_id: int
    last_reset: int
    slope: float
    offset_pair: TimePair
    clock_name: str
    def __init__(self, clock_id: _Optional[int] = ..., last_reset: _Optional[int] = ..., slope: _Optional[float] = ..., offset_pair: _Optional[_Union[TimePair, _Mapping]] = ..., clock_name: _Optional[str] = ...) -> None: ...

class ClockConversionArray(_message.Message):
    __slots__ = ("clock_conversions",)
    CLOCK_CONVERSIONS_FIELD_NUMBER: _ClassVar[int]
    clock_conversions: _containers.RepeatedCompositeFieldContainer[ClockConversion]
    def __init__(self, clock_conversions: _Optional[_Iterable[_Union[ClockConversion, _Mapping]]] = ...) -> None: ...

class SystemStatus(_message.Message):
    __slots__ = ("clock_conversion_array",)
    CLOCK_CONVERSION_ARRAY_FIELD_NUMBER: _ClassVar[int]
    clock_conversion_array: ClockConversionArray
    def __init__(self, clock_conversion_array: _Optional[_Union[ClockConversionArray, _Mapping]] = ...) -> None: ...

class ClockStatusArray(_message.Message):
    __slots__ = ("clocks_status",)
    CLOCKS_STATUS_FIELD_NUMBER: _ClassVar[int]
    clocks_status: _containers.RepeatedCompositeFieldContainer[ClockStatus]
    def __init__(self, clocks_status: _Optional[_Iterable[_Union[ClockStatus, _Mapping]]] = ...) -> None: ...

class ClockStatus(_message.Message):
    __slots__ = ("clock_conversion", "error_mean", "error_std_dev")
    CLOCK_CONVERSION_FIELD_NUMBER: _ClassVar[int]
    ERROR_MEAN_FIELD_NUMBER: _ClassVar[int]
    ERROR_STD_DEV_FIELD_NUMBER: _ClassVar[int]
    clock_conversion: ClockConversion
    error_mean: int
    error_std_dev: int
    def __init__(self, clock_conversion: _Optional[_Union[ClockConversion, _Mapping]] = ..., error_mean: _Optional[int] = ..., error_std_dev: _Optional[int] = ...) -> None: ...
