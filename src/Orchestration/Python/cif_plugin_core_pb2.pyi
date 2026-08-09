import cif_common_pb2 as _cif_common_pb2
import cif_management_common_pb2 as _cif_management_common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StartRequest(_message.Message):
    __slots__ = ("start_fte",)
    START_FTE_FIELD_NUMBER: _ClassVar[int]
    start_fte: int
    def __init__(self, start_fte: _Optional[int] = ...) -> None: ...

class StartResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class PrepareRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PrepareResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class PauseRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class PauseResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class StopRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StopResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class RefreshStatisticsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RefreshStatisticsResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class GetStatusDataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetStatusDataResponse(_message.Message):
    __slots__ = ("status_data",)
    STATUS_DATA_FIELD_NUMBER: _ClassVar[int]
    status_data: _cif_management_common_pb2.PluginStatusData
    def __init__(self, status_data: _Optional[_Union[_cif_management_common_pb2.PluginStatusData, _Mapping]] = ...) -> None: ...

class UpdateConfigRequest(_message.Message):
    __slots__ = ("configuration",)
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    configuration: Configuration
    def __init__(self, configuration: _Optional[_Union[Configuration, _Mapping]] = ...) -> None: ...

class UpdateConfigResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class GetVersionRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetVersionResponse(_message.Message):
    __slots__ = ("version",)
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: _cif_common_pb2.Version
    def __init__(self, version: _Optional[_Union[_cif_common_pb2.Version, _Mapping]] = ...) -> None: ...

class GetConfigRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetConfigResponse(_message.Message):
    __slots__ = ("configuration",)
    CONFIGURATION_FIELD_NUMBER: _ClassVar[int]
    configuration: Configuration
    def __init__(self, configuration: _Optional[_Union[Configuration, _Mapping]] = ...) -> None: ...

class GetOverridesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetOverridesResponse(_message.Message):
    __slots__ = ("plugin_overrides",)
    PLUGIN_OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    plugin_overrides: PluginOverrides
    def __init__(self, plugin_overrides: _Optional[_Union[PluginOverrides, _Mapping]] = ...) -> None: ...

class GetNamesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetNamesResponse(_message.Message):
    __slots__ = ("plugin_names",)
    PLUGIN_NAMES_FIELD_NUMBER: _ClassVar[int]
    plugin_names: _cif_common_pb2.PluginNames
    def __init__(self, plugin_names: _Optional[_Union[_cif_common_pb2.PluginNames, _Mapping]] = ...) -> None: ...

class Configuration(_message.Message):
    __slots__ = ("json_config",)
    JSON_CONFIG_FIELD_NUMBER: _ClassVar[int]
    json_config: str
    def __init__(self, json_config: _Optional[str] = ...) -> None: ...

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
