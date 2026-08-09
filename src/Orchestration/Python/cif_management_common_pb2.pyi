import cif_common_pb2 as _cif_common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChannelDirection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHANNELDIRECTION_UNKNOWN: _ClassVar[ChannelDirection]
    CHANNELDIRECTION_PUBLISHER: _ClassVar[ChannelDirection]
    CHANNELDIRECTION_SUBSCRIBER: _ClassVar[ChannelDirection]

class ChannelPattern(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CHANNELPATTERN_UNKNOWN: _ClassVar[ChannelPattern]
    CHANNELPATTERN_TAG: _ClassVar[ChannelPattern]
    CHANNELPATTERN_FIFO: _ClassVar[ChannelPattern]
    CHANNELPATTERN_MULTIFIFO: _ClassVar[ChannelPattern]
    CHANNELPATTERN_BACKPRESSUREFIFO: _ClassVar[ChannelPattern]

class LoaderType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOADERTYPE_UNKNOWN: _ClassVar[LoaderType]
    LOADERTYPE_LABVIEW: _ClassVar[LoaderType]
CHANNELDIRECTION_UNKNOWN: ChannelDirection
CHANNELDIRECTION_PUBLISHER: ChannelDirection
CHANNELDIRECTION_SUBSCRIBER: ChannelDirection
CHANNELPATTERN_UNKNOWN: ChannelPattern
CHANNELPATTERN_TAG: ChannelPattern
CHANNELPATTERN_FIFO: ChannelPattern
CHANNELPATTERN_MULTIFIFO: ChannelPattern
CHANNELPATTERN_BACKPRESSUREFIFO: ChannelPattern
LOADERTYPE_UNKNOWN: LoaderType
LOADERTYPE_LABVIEW: LoaderType

class PluginMetadata(_message.Message):
    __slots__ = ("description", "history", "author")
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    description: str
    history: str
    author: str
    def __init__(self, description: _Optional[str] = ..., history: _Optional[str] = ..., author: _Optional[str] = ...) -> None: ...

class Channels(_message.Message):
    __slots__ = ("channels",)
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedCompositeFieldContainer[Channel]
    def __init__(self, channels: _Optional[_Iterable[_Union[Channel, _Mapping]]] = ...) -> None: ...

class Channel(_message.Message):
    __slots__ = ("name", "direction", "type", "custom_config", "connected", "connected_name", "forced", "channel_pattern")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CONFIG_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_NAME_FIELD_NUMBER: _ClassVar[int]
    FORCED_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_PATTERN_FIELD_NUMBER: _ClassVar[int]
    name: str
    direction: ChannelDirection
    type: str
    custom_config: bytes
    connected: bool
    connected_name: str
    forced: bool
    channel_pattern: ChannelPattern
    def __init__(self, name: _Optional[str] = ..., direction: _Optional[_Union[ChannelDirection, str]] = ..., type: _Optional[str] = ..., custom_config: _Optional[bytes] = ..., connected: bool = ..., connected_name: _Optional[str] = ..., forced: bool = ..., channel_pattern: _Optional[_Union[ChannelPattern, str]] = ...) -> None: ...

class ChannelFilter(_message.Message):
    __slots__ = ("name_regex", "direction", "direction_filter", "type_regex", "forced", "forced_filter")
    NAME_REGEX_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FILTER_FIELD_NUMBER: _ClassVar[int]
    TYPE_REGEX_FIELD_NUMBER: _ClassVar[int]
    FORCED_FIELD_NUMBER: _ClassVar[int]
    FORCED_FILTER_FIELD_NUMBER: _ClassVar[int]
    name_regex: str
    direction: ChannelDirection
    direction_filter: bool
    type_regex: str
    forced: bool
    forced_filter: bool
    def __init__(self, name_regex: _Optional[str] = ..., direction: _Optional[_Union[ChannelDirection, str]] = ..., direction_filter: bool = ..., type_regex: _Optional[str] = ..., forced: bool = ..., forced_filter: bool = ...) -> None: ...

class PluginStatusData(_message.Message):
    __slots__ = ("state", "timing_statistics", "fifo_statistics", "error", "monitor_doubles", "monitor_u64s", "monitor_i64s")
    class PluginState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        PLUGINSTATE_UNKNOWN: _ClassVar[PluginStatusData.PluginState]
        PLUGINSTATE_CREATING: _ClassVar[PluginStatusData.PluginState]
        PLUGINSTATE_LISTENING: _ClassVar[PluginStatusData.PluginState]
        PLUGINSTATE_RUNNING: _ClassVar[PluginStatusData.PluginState]
        PLUGINSTATE_CLEANINGUP: _ClassVar[PluginStatusData.PluginState]
        PLUGINSTATE_DESTROYING: _ClassVar[PluginStatusData.PluginState]
        PLUGINSTATE_PREPARED: _ClassVar[PluginStatusData.PluginState]
        PLUGINSTATE_FTE_RUN: _ClassVar[PluginStatusData.PluginState]
    PLUGINSTATE_UNKNOWN: PluginStatusData.PluginState
    PLUGINSTATE_CREATING: PluginStatusData.PluginState
    PLUGINSTATE_LISTENING: PluginStatusData.PluginState
    PLUGINSTATE_RUNNING: PluginStatusData.PluginState
    PLUGINSTATE_CLEANINGUP: PluginStatusData.PluginState
    PLUGINSTATE_DESTROYING: PluginStatusData.PluginState
    PLUGINSTATE_PREPARED: PluginStatusData.PluginState
    PLUGINSTATE_FTE_RUN: PluginStatusData.PluginState
    STATE_FIELD_NUMBER: _ClassVar[int]
    TIMING_STATISTICS_FIELD_NUMBER: _ClassVar[int]
    FIFO_STATISTICS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MONITOR_DOUBLES_FIELD_NUMBER: _ClassVar[int]
    MONITOR_U64S_FIELD_NUMBER: _ClassVar[int]
    MONITOR_I64S_FIELD_NUMBER: _ClassVar[int]
    state: PluginStatusData.PluginState
    timing_statistics: TimingStatistics
    fifo_statistics: FifoStatistics
    error: Error
    monitor_doubles: MonitorDoubles
    monitor_u64s: MonitorU64
    monitor_i64s: MonitorI64
    def __init__(self, state: _Optional[_Union[PluginStatusData.PluginState, str]] = ..., timing_statistics: _Optional[_Union[TimingStatistics, _Mapping]] = ..., fifo_statistics: _Optional[_Union[FifoStatistics, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ..., monitor_doubles: _Optional[_Union[MonitorDoubles, _Mapping]] = ..., monitor_u64s: _Optional[_Union[MonitorU64, _Mapping]] = ..., monitor_i64s: _Optional[_Union[MonitorI64, _Mapping]] = ...) -> None: ...

class TimingStatistics(_message.Message):
    __slots__ = ("period", "wake_error", "execute", "housekeep", "idle", "cleanup", "custom_1", "custom_2")
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    WAKE_ERROR_FIELD_NUMBER: _ClassVar[int]
    EXECUTE_FIELD_NUMBER: _ClassVar[int]
    HOUSEKEEP_FIELD_NUMBER: _ClassVar[int]
    IDLE_FIELD_NUMBER: _ClassVar[int]
    CLEANUP_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_1_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_2_FIELD_NUMBER: _ClassVar[int]
    period: _cif_common_pb2.TimingStats
    wake_error: _cif_common_pb2.TimingStats
    execute: _cif_common_pb2.TimingStats
    housekeep: _cif_common_pb2.TimingStats
    idle: _cif_common_pb2.TimingStats
    cleanup: _cif_common_pb2.TimingStats
    custom_1: _cif_common_pb2.TimingStats
    custom_2: _cif_common_pb2.TimingStats
    def __init__(self, period: _Optional[_Union[_cif_common_pb2.TimingStats, _Mapping]] = ..., wake_error: _Optional[_Union[_cif_common_pb2.TimingStats, _Mapping]] = ..., execute: _Optional[_Union[_cif_common_pb2.TimingStats, _Mapping]] = ..., housekeep: _Optional[_Union[_cif_common_pb2.TimingStats, _Mapping]] = ..., idle: _Optional[_Union[_cif_common_pb2.TimingStats, _Mapping]] = ..., cleanup: _Optional[_Union[_cif_common_pb2.TimingStats, _Mapping]] = ..., custom_1: _Optional[_Union[_cif_common_pb2.TimingStats, _Mapping]] = ..., custom_2: _Optional[_Union[_cif_common_pb2.TimingStats, _Mapping]] = ...) -> None: ...

class FifoStatistics(_message.Message):
    __slots__ = ("from_t0", "from_previous_plugin", "output_error")
    FROM_T0_FIELD_NUMBER: _ClassVar[int]
    FROM_PREVIOUS_PLUGIN_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_ERROR_FIELD_NUMBER: _ClassVar[int]
    from_t0: _cif_common_pb2.TimingStats
    from_previous_plugin: _cif_common_pb2.TimingStats
    output_error: _cif_common_pb2.TimingStats
    def __init__(self, from_t0: _Optional[_Union[_cif_common_pb2.TimingStats, _Mapping]] = ..., from_previous_plugin: _Optional[_Union[_cif_common_pb2.TimingStats, _Mapping]] = ..., output_error: _Optional[_Union[_cif_common_pb2.TimingStats, _Mapping]] = ...) -> None: ...

class MonitorDoubles(_message.Message):
    __slots__ = ("double_1", "double_2", "double_3", "double_4")
    DOUBLE_1_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_2_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_3_FIELD_NUMBER: _ClassVar[int]
    DOUBLE_4_FIELD_NUMBER: _ClassVar[int]
    double_1: float
    double_2: float
    double_3: float
    double_4: float
    def __init__(self, double_1: _Optional[float] = ..., double_2: _Optional[float] = ..., double_3: _Optional[float] = ..., double_4: _Optional[float] = ...) -> None: ...

class MonitorU64(_message.Message):
    __slots__ = ("u64_1", "u64_2", "u64_3", "u64_4")
    U64_1_FIELD_NUMBER: _ClassVar[int]
    U64_2_FIELD_NUMBER: _ClassVar[int]
    U64_3_FIELD_NUMBER: _ClassVar[int]
    U64_4_FIELD_NUMBER: _ClassVar[int]
    u64_1: int
    u64_2: int
    u64_3: int
    u64_4: int
    def __init__(self, u64_1: _Optional[int] = ..., u64_2: _Optional[int] = ..., u64_3: _Optional[int] = ..., u64_4: _Optional[int] = ...) -> None: ...

class MonitorI64(_message.Message):
    __slots__ = ("i64_1", "i64_2", "i64_3", "i64_4")
    I64_1_FIELD_NUMBER: _ClassVar[int]
    I64_2_FIELD_NUMBER: _ClassVar[int]
    I64_3_FIELD_NUMBER: _ClassVar[int]
    I64_4_FIELD_NUMBER: _ClassVar[int]
    i64_1: int
    i64_2: int
    i64_3: int
    i64_4: int
    def __init__(self, i64_1: _Optional[int] = ..., i64_2: _Optional[int] = ..., i64_3: _Optional[int] = ..., i64_4: _Optional[int] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ("status", "code")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    status: bool
    code: int
    def __init__(self, status: bool = ..., code: _Optional[int] = ...) -> None: ...

class LoaderInfo(_message.Message):
    __slots__ = ("loader_type", "loader_name")
    LOADER_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOADER_NAME_FIELD_NUMBER: _ClassVar[int]
    loader_type: LoaderType
    loader_name: str
    def __init__(self, loader_type: _Optional[_Union[LoaderType, str]] = ..., loader_name: _Optional[str] = ...) -> None: ...

class LoaderInfoFull(_message.Message):
    __slots__ = ("loader_type", "loader_name", "grpc_port", "pid")
    LOADER_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOADER_NAME_FIELD_NUMBER: _ClassVar[int]
    GRPC_PORT_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    loader_type: LoaderType
    loader_name: str
    grpc_port: int
    pid: int
    def __init__(self, loader_type: _Optional[_Union[LoaderType, str]] = ..., loader_name: _Optional[str] = ..., grpc_port: _Optional[int] = ..., pid: _Optional[int] = ...) -> None: ...
