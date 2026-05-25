import cif_common_pb2 as _cif_common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ModelState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOT_LOADED: _ClassVar[ModelState]
    UNINITIALIZED: _ClassVar[ModelState]
    RUNNING: _ClassVar[ModelState]
NOT_LOADED: ModelState
UNINITIALIZED: ModelState
RUNNING: ModelState

class Statistics(_message.Message):
    __slots__ = ("iterations", "load_ctr")
    ITERATIONS_FIELD_NUMBER: _ClassVar[int]
    LOAD_CTR_FIELD_NUMBER: _ClassVar[int]
    iterations: int
    load_ctr: int
    def __init__(self, iterations: _Optional[int] = ..., load_ctr: _Optional[int] = ...) -> None: ...

class ModelList(_message.Message):
    __slots__ = ("model_files",)
    MODEL_FILES_FIELD_NUMBER: _ClassVar[int]
    model_files: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, model_files: _Optional[_Iterable[str]] = ...) -> None: ...

class ModelStateResponse(_message.Message):
    __slots__ = ("model_state",)
    MODEL_STATE_FIELD_NUMBER: _ClassVar[int]
    model_state: ModelState
    def __init__(self, model_state: _Optional[_Union[ModelState, str]] = ...) -> None: ...

class Channels(_message.Message):
    __slots__ = ("channels", "status")
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedScalarFieldContainer[str]
    status: _cif_common_pb2.Status
    def __init__(self, channels: _Optional[_Iterable[str]] = ..., status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class ChannelRequest(_message.Message):
    __slots__ = ("channels",)
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, channels: _Optional[_Iterable[str]] = ...) -> None: ...

class Values(_message.Message):
    __slots__ = ("values", "status")
    VALUES_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedScalarFieldContainer[float]
    status: _cif_common_pb2.Status
    def __init__(self, values: _Optional[_Iterable[float]] = ..., status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class Parameters(_message.Message):
    __slots__ = ("parameters", "status")
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    parameters: _containers.RepeatedCompositeFieldContainer[Parameter]
    status: _cif_common_pb2.Status
    def __init__(self, parameters: _Optional[_Iterable[_Union[Parameter, _Mapping]]] = ..., status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class SetParameterRequest(_message.Message):
    __slots__ = ("parameter_name", "parameter_value")
    PARAMETER_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_VALUE_FIELD_NUMBER: _ClassVar[int]
    parameter_name: str
    parameter_value: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, parameter_name: _Optional[str] = ..., parameter_value: _Optional[_Iterable[float]] = ...) -> None: ...

class GetParameterRequest(_message.Message):
    __slots__ = ("parameter_name",)
    PARAMETER_NAME_FIELD_NUMBER: _ClassVar[int]
    parameter_name: str
    def __init__(self, parameter_name: _Optional[str] = ...) -> None: ...

class MonitoredData(_message.Message):
    __slots__ = ("monitored_data", "status")
    MONITORED_DATA_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    monitored_data: _containers.RepeatedScalarFieldContainer[float]
    status: _cif_common_pb2.Status
    def __init__(self, monitored_data: _Optional[_Iterable[float]] = ..., status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class GetSignalResponse(_message.Message):
    __slots__ = ("signals", "status")
    SIGNALS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    signals: _containers.RepeatedCompositeFieldContainer[Signal]
    status: _cif_common_pb2.Status
    def __init__(self, signals: _Optional[_Iterable[_Union[Signal, _Mapping]]] = ..., status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class Signals(_message.Message):
    __slots__ = ("signal_names",)
    SIGNAL_NAMES_FIELD_NUMBER: _ClassVar[int]
    signal_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, signal_names: _Optional[_Iterable[str]] = ...) -> None: ...

class Signal(_message.Message):
    __slots__ = ("name", "dimension_1", "dimension_2", "port")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_1_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_2_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    name: str
    dimension_1: int
    dimension_2: int
    port: int
    def __init__(self, name: _Optional[str] = ..., dimension_1: _Optional[int] = ..., dimension_2: _Optional[int] = ..., port: _Optional[int] = ...) -> None: ...

class Parameter(_message.Message):
    __slots__ = ("name", "dimension_1", "dimension_2")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_1_FIELD_NUMBER: _ClassVar[int]
    DIMENSION_2_FIELD_NUMBER: _ClassVar[int]
    name: str
    dimension_1: int
    dimension_2: int
    def __init__(self, name: _Optional[str] = ..., dimension_1: _Optional[int] = ..., dimension_2: _Optional[int] = ...) -> None: ...
