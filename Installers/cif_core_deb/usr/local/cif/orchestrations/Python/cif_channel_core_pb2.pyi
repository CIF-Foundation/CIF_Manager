import cif_common_pb2 as _cif_common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Direction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PUBLISHER: _ClassVar[Direction]
    SUBSCRIBER: _ClassVar[Direction]

class PATTERN(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[PATTERN]
    TAG: _ClassVar[PATTERN]
    FIFO: _ClassVar[PATTERN]
    MULTIFIFO: _ClassVar[PATTERN]
    BACKPRESSUREFIFO: _ClassVar[PATTERN]
PUBLISHER: Direction
SUBSCRIBER: Direction
UNKNOWN: PATTERN
TAG: PATTERN
FIFO: PATTERN
MULTIFIFO: PATTERN
BACKPRESSUREFIFO: PATTERN

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
    direction: Direction
    type: str
    custom_config: bytes
    connected: bool
    connected_name: str
    forced: bool
    channel_pattern: PATTERN
    def __init__(self, name: _Optional[str] = ..., direction: _Optional[_Union[Direction, str]] = ..., type: _Optional[str] = ..., custom_config: _Optional[bytes] = ..., connected: bool = ..., connected_name: _Optional[str] = ..., forced: bool = ..., channel_pattern: _Optional[_Union[PATTERN, str]] = ...) -> None: ...

class ChannelFilter(_message.Message):
    __slots__ = ("name_regex", "direction", "direction_filter", "type_regex", "forced", "forced_filter")
    NAME_REGEX_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FILTER_FIELD_NUMBER: _ClassVar[int]
    TYPE_REGEX_FIELD_NUMBER: _ClassVar[int]
    FORCED_FIELD_NUMBER: _ClassVar[int]
    FORCED_FILTER_FIELD_NUMBER: _ClassVar[int]
    name_regex: str
    direction: Direction
    direction_filter: bool
    type_regex: str
    forced: bool
    forced_filter: bool
    def __init__(self, name_regex: _Optional[str] = ..., direction: _Optional[_Union[Direction, str]] = ..., direction_filter: bool = ..., type_regex: _Optional[str] = ..., forced: bool = ..., forced_filter: bool = ...) -> None: ...

class Channels(_message.Message):
    __slots__ = ("channels",)
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    channels: _containers.RepeatedCompositeFieldContainer[Channel]
    def __init__(self, channels: _Optional[_Iterable[_Union[Channel, _Mapping]]] = ...) -> None: ...

class ConnectSubscriber(_message.Message):
    __slots__ = ("subscriber_name", "publisher_name", "custom_connect")
    SUBSCRIBER_NAME_FIELD_NUMBER: _ClassVar[int]
    PUBLISHER_NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CONNECT_FIELD_NUMBER: _ClassVar[int]
    subscriber_name: str
    publisher_name: str
    custom_connect: bytes
    def __init__(self, subscriber_name: _Optional[str] = ..., publisher_name: _Optional[str] = ..., custom_connect: _Optional[bytes] = ...) -> None: ...

class FIFOInstance(_message.Message):
    __slots__ = ("publisher_name", "retry_on_timeout", "bytes_per_message_override", "message_per_fifo_override", "custom_data")
    PUBLISHER_NAME_FIELD_NUMBER: _ClassVar[int]
    RETRY_ON_TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    BYTES_PER_MESSAGE_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_PER_FIFO_OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_DATA_FIELD_NUMBER: _ClassVar[int]
    publisher_name: str
    retry_on_timeout: bool
    bytes_per_message_override: int
    message_per_fifo_override: int
    custom_data: bytes
    def __init__(self, publisher_name: _Optional[str] = ..., retry_on_timeout: bool = ..., bytes_per_message_override: _Optional[int] = ..., message_per_fifo_override: _Optional[int] = ..., custom_data: _Optional[bytes] = ...) -> None: ...

class FIFOReference(_message.Message):
    __slots__ = ("publisher_instance_name", "custom_connect", "status")
    PUBLISHER_INSTANCE_NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CONNECT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    publisher_instance_name: str
    custom_connect: bytes
    status: _cif_common_pb2.Status
    def __init__(self, publisher_instance_name: _Optional[str] = ..., custom_connect: _Optional[bytes] = ..., status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class FIFOInstanceName(_message.Message):
    __slots__ = ("publisher_instance_name",)
    PUBLISHER_INSTANCE_NAME_FIELD_NUMBER: _ClassVar[int]
    publisher_instance_name: str
    def __init__(self, publisher_instance_name: _Optional[str] = ...) -> None: ...

class ForceChannel(_message.Message):
    __slots__ = ("channel_name", "force", "force_data")
    CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    FORCE_DATA_FIELD_NUMBER: _ClassVar[int]
    channel_name: str
    force: bool
    force_data: bytes
    def __init__(self, channel_name: _Optional[str] = ..., force: bool = ..., force_data: _Optional[bytes] = ...) -> None: ...
