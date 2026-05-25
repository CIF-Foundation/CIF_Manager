import cif_common_pb2 as _cif_common_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Configuration(_message.Message):
    __slots__ = ("json_config",)
    JSON_CONFIG_FIELD_NUMBER: _ClassVar[int]
    json_config: str
    def __init__(self, json_config: _Optional[str] = ...) -> None: ...

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

class StatusData(_message.Message):
    __slots__ = ("state", "timing_statistics", "fifo_statistics", "error", "monitor_doubles", "monitor_u64s", "monitor_i64s")
    class State(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NULL: _ClassVar[StatusData.State]
        CREATING: _ClassVar[StatusData.State]
        LISTENING: _ClassVar[StatusData.State]
        RUNNING: _ClassVar[StatusData.State]
        CLEANINGUP: _ClassVar[StatusData.State]
        DESTROYING: _ClassVar[StatusData.State]
    NULL: StatusData.State
    CREATING: StatusData.State
    LISTENING: StatusData.State
    RUNNING: StatusData.State
    CLEANINGUP: StatusData.State
    DESTROYING: StatusData.State
    STATE_FIELD_NUMBER: _ClassVar[int]
    TIMING_STATISTICS_FIELD_NUMBER: _ClassVar[int]
    FIFO_STATISTICS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MONITOR_DOUBLES_FIELD_NUMBER: _ClassVar[int]
    MONITOR_U64S_FIELD_NUMBER: _ClassVar[int]
    MONITOR_I64S_FIELD_NUMBER: _ClassVar[int]
    state: StatusData.State
    timing_statistics: TimingStatistics
    fifo_statistics: FifoStatistics
    error: Error
    monitor_doubles: MonitorDoubles
    monitor_u64s: MonitorU64
    monitor_i64s: MonitorI64
    def __init__(self, state: _Optional[_Union[StatusData.State, str]] = ..., timing_statistics: _Optional[_Union[TimingStatistics, _Mapping]] = ..., fifo_statistics: _Optional[_Union[FifoStatistics, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ..., monitor_doubles: _Optional[_Union[MonitorDoubles, _Mapping]] = ..., monitor_u64s: _Optional[_Union[MonitorU64, _Mapping]] = ..., monitor_i64s: _Optional[_Union[MonitorI64, _Mapping]] = ...) -> None: ...

class Error(_message.Message):
    __slots__ = ("status", "code")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    status: bool
    code: int
    def __init__(self, status: bool = ..., code: _Optional[int] = ...) -> None: ...

class TimingOverrides(_message.Message):
    __slots__ = ("override_timing", "skip_sleep", "period")
    OVERRIDE_TIMING_FIELD_NUMBER: _ClassVar[int]
    SKIP_SLEEP_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    override_timing: bool
    skip_sleep: bool
    period: float
    def __init__(self, override_timing: bool = ..., skip_sleep: bool = ..., period: _Optional[float] = ...) -> None: ...

class PluginOverrides(_message.Message):
    __slots__ = ("timing_overrides",)
    TIMING_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    timing_overrides: TimingOverrides
    def __init__(self, timing_overrides: _Optional[_Union[TimingOverrides, _Mapping]] = ...) -> None: ...
