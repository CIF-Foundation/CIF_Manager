from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TimingStats(_message.Message):
    __slots__ = ("max", "min", "avg")
    MAX_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    AVG_FIELD_NUMBER: _ClassVar[int]
    max: int
    min: int
    avg: float
    def __init__(self, max: _Optional[int] = ..., min: _Optional[int] = ..., avg: _Optional[float] = ...) -> None: ...

class Version(_message.Message):
    __slots__ = ("major", "minor", "fix", "build")
    MAJOR_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    FIX_FIELD_NUMBER: _ClassVar[int]
    BUILD_FIELD_NUMBER: _ClassVar[int]
    major: int
    minor: int
    fix: int
    build: int
    def __init__(self, major: _Optional[int] = ..., minor: _Optional[int] = ..., fix: _Optional[int] = ..., build: _Optional[int] = ...) -> None: ...

class ShortVersion(_message.Message):
    __slots__ = ("major", "minor", "fix")
    MAJOR_FIELD_NUMBER: _ClassVar[int]
    MINOR_FIELD_NUMBER: _ClassVar[int]
    FIX_FIELD_NUMBER: _ClassVar[int]
    major: int
    minor: int
    fix: int
    def __init__(self, major: _Optional[int] = ..., minor: _Optional[int] = ..., fix: _Optional[int] = ...) -> None: ...

class PluginNames(_message.Message):
    __slots__ = ("plugin_name", "plugin_type", "loader_name")
    PLUGIN_NAME_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_TYPE_FIELD_NUMBER: _ClassVar[int]
    LOADER_NAME_FIELD_NUMBER: _ClassVar[int]
    plugin_name: str
    plugin_type: str
    loader_name: str
    def __init__(self, plugin_name: _Optional[str] = ..., plugin_type: _Optional[str] = ..., loader_name: _Optional[str] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ("code", "message")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: int
    message: str
    def __init__(self, code: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
