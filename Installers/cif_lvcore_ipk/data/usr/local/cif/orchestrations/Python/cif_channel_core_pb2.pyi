import cif_common_pb2 as _cif_common_pb2
import cif_management_common_pb2 as _cif_management_common_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetChannelsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetChannelsResponse(_message.Message):
    __slots__ = ("channels",)
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    channels: _cif_management_common_pb2.Channels
    def __init__(self, channels: _Optional[_Union[_cif_management_common_pb2.Channels, _Mapping]] = ...) -> None: ...

class SetConnectionRequest(_message.Message):
    __slots__ = ("subscriber_name", "publisher_name", "custom_connect")
    SUBSCRIBER_NAME_FIELD_NUMBER: _ClassVar[int]
    PUBLISHER_NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CONNECT_FIELD_NUMBER: _ClassVar[int]
    subscriber_name: str
    publisher_name: str
    custom_connect: bytes
    def __init__(self, subscriber_name: _Optional[str] = ..., publisher_name: _Optional[str] = ..., custom_connect: _Optional[bytes] = ...) -> None: ...

class SetConnectionResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class CreateFIFOInstanceRequest(_message.Message):
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

class CreateFIFOInstanceResponse(_message.Message):
    __slots__ = ("fifo_reference", "status")
    FIFO_REFERENCE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    fifo_reference: FIFOReference
    status: _cif_common_pb2.Status
    def __init__(self, fifo_reference: _Optional[_Union[FIFOReference, _Mapping]] = ..., status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class FIFOReference(_message.Message):
    __slots__ = ("publisher_instance_name", "custom_connect")
    PUBLISHER_INSTANCE_NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CONNECT_FIELD_NUMBER: _ClassVar[int]
    publisher_instance_name: str
    custom_connect: bytes
    def __init__(self, publisher_instance_name: _Optional[str] = ..., custom_connect: _Optional[bytes] = ...) -> None: ...

class DestroyFIFOInstanceRequest(_message.Message):
    __slots__ = ("publisher_instance_name",)
    PUBLISHER_INSTANCE_NAME_FIELD_NUMBER: _ClassVar[int]
    publisher_instance_name: str
    def __init__(self, publisher_instance_name: _Optional[str] = ...) -> None: ...

class DestroyFIFOInstanceResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...

class SetForceRequest(_message.Message):
    __slots__ = ("channel_name", "force", "force_data")
    CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    FORCE_DATA_FIELD_NUMBER: _ClassVar[int]
    channel_name: str
    force: bool
    force_data: bytes
    def __init__(self, channel_name: _Optional[str] = ..., force: bool = ..., force_data: _Optional[bytes] = ...) -> None: ...

class SetForceResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: _cif_common_pb2.Status
    def __init__(self, status: _Optional[_Union[_cif_common_pb2.Status, _Mapping]] = ...) -> None: ...
