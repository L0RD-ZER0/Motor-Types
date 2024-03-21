import datetime
from asyncio import AbstractEventLoop
from os import SEEK_SET as _SEEK_SET
from types import TracebackType
from typing import IO, Any, Iterable, List, Mapping, NoReturn, Optional, Type, Union

from bson import ObjectId
from gridfs.grid_file import DEFAULT_CHUNK_SIZE, GridIn, GridOut
from pymongo import read_preferences as _read_preferences
from pymongo.client_session import ClientSession
from pymongo.write_concern import WriteConcern
from typing_extensions import Literal, Self

from .core import (
    AgnosticClientSession,
    AgnosticCollection,
    AgnosticCursor,
    AgnosticDatabase,
)
from .metaprogramming import ReadOnlyProperty

_IO_Loop = AbstractEventLoop
_Handler = Any  # Replace it with tornado.web.RequestHandler
_ReadPreferences = Union[
    _read_preferences.Primary,
    _read_preferences.PrimaryPreferred,
    _read_preferences.Secondary,
    _read_preferences.SecondaryPreferred,
    _read_preferences.Nearest,
]
_Session = Union[ClientSession, AgnosticClientSession]

class MotorGridOutProperty(ReadOnlyProperty):
    pass

class AgnosticGridOutCursor(AgnosticCursor):
    def next_object(self) -> Optional[AgnosticGridOut]: ...

    async def __aenter__(self) -> "AgnosticGridOutCursor": ...

class AgnosticGridOut(object):
    _id: Any
    aliases: Optional[List[str]]
    chunk_size: int
    content_type: Optional[str]
    filename: Optional[str]
    length: int
    metadata: Optional[Mapping[str, Any]]
    name: Optional[str]
    upload_date: datetime.datetime

    def __init__(
        self,
        root_collection: AgnosticCollection,
        file_id: Optional[int] = None,
        file_document: Optional[Any] = None,
        delegate: Optional[GridOut] = None,
        session: Optional[ClientSession] = None,
        **kwargs: Any,
    ) -> None: ...
    async def __aiter__(self) -> Self: ...
    async def __anext__(self) -> bytes: ...
    def __getattr__(self, name: str) -> Any: ...
    async def _ensure_file(self) -> None: ...
    async def close(self) -> None: ...
    def get_io_loop(self) -> _IO_Loop: ...
    async def open(self) -> Self: ...
    async def read(self, size: int = -1) -> bytes: ...
    def readable(self) -> Literal[True]: ...
    async def readchunk(self) -> bytes: ...
    async def readline(self, size: int = -1) -> bytes: ...
    def seek(self, pos: int, whence: int = _SEEK_SET) -> int: ...
    def tell(self) -> int: ...
    def seekable(self) -> Literal[True]: ...
    async def write(self, data: Any) -> None: ...
    async def stream_to_handler(self, request_handler: _Handler) -> None: ...

class AgnosticGridIn(object):
    _id: Any
    chunk_size: int
    closed: bool
    content_type: Optional[str]
    filename: Optional[str]
    length: int
    md5: Optional[str]
    name: Optional[str]
    upload_date: datetime.datetime

    def __init__(
        self,
        root_collection: AgnosticCollection,
        delegate: Optional[GridIn] = None,
        session: Optional[ClientSession] = None,
        **kwargs: Any,
    ) -> None: ...
    async def __aenter__(self) -> Self: ...
    async def __aexit__(
        self,
        exc_type: Optional[Type[Exception]] = None,
        exc_val: Optional[Exception] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    async def _exit(
        self,
        exc_type: Optional[Type[Exception]] = None,
        exc_val: Optional[Exception] = None,
        exc_tb: Optional[TracebackType] = None,
    ) -> None: ...
    async def abort(self) -> None: ...
    async def close(self) -> None: ...
    def get_io_loop(self) -> _IO_Loop: ...
    def read(self, size: int = -1) -> NoReturn: ...
    def readable(self) -> Literal[False]: ...
    def seekable(self) -> Literal[False]: ...
    async def write(self, data: Any) -> None: ...
    async def writelines(self, sequence: Iterable[Any]) -> None: ...
    def writeable(self) -> Literal[True]: ...
    async def set(self, name: str, value: Any) -> None: ...

class AgnosticGridFSBucket(object):
    collection: AgnosticCollection
    def __init__(
        self,
        database: AgnosticDatabase,
        bucket_name: str = 'fs',
        chunk_size_bytes: int = DEFAULT_CHUNK_SIZE,
        write_concern: Optional[WriteConcern] = None,
        read_preference: Optional[_ReadPreferences] = None,
        collection: Optional[AgnosticCollection] = None,
    ) -> None: ...
    async def delete(
        self, file_id: Any, session: Optional[_Session] = None
    ) -> None: ...
    async def download_to_stream(
        self,
        file_id: Any,
        destination: IO,
        session: Optional[_Session] = None,
    ) -> None: ...
    async def download_to_stream_by_name(
        self,
        filename: str,
        destination: IO,
        revision: int = -1,
        session: Optional[_Session] = None,
    ) -> None: ...
    def find(
        self,
        filter: Optional[Mapping[str, Any]] = None,
        skip: int = 0,
        limit: int = 0,
        no_cursor_timeout: bool = False,
        sort: Optional[Any] = None,
        batch_size: int = 0,
        session: Optional[_Session] = None,
    ) -> AgnosticGridOutCursor: ...
    async def get_io_loop(self) -> _IO_Loop: ...
    async def open_download_stream(
        self, file_id: Any, session: Optional[_Session] = None
    ) -> AgnosticGridOut: ...
    async def open_download_stream_by_name(
        self, filename: str, revision: int = -1, session: Optional[_Session] = None
    ) -> AgnosticGridOut: ...
    def open_upload_stream(
        self, file_id: Any, session: Optional[_Session] = None
    ) -> AgnosticGridIn: ...
    def open_upload_stream_with_id(
        self,
        file_id: Any,
        filename: str,
        chunk_size_bytes: Optional[int] = None,
        metadata: Optional[Mapping[str, Any]] = None,
        session: Optional[_Session] = None,
    ) -> AgnosticGridIn: ...
    async def rename(
        self,
        file_id: Any,
        new_filename: str,
        session: Optional[_Session] = None,
    ) -> None: ...
    async def upload_from_stream(
        self,
        filename: str,
        source: Any,
        chunk_size_bytes: Optional[int] = None,
        metadata: Optional[Mapping[str, Any]] = None,
        session: Optional[_Session] = None,
    ) -> ObjectId: ...
    async def upload_from_stream_with_id(
        self,
        file_id: Any,
        filename: str,
        source: Any,
        chunk_size_bytes: Optional[int] = None,
        metadata: Optional[Mapping[str, Any]] = None,
        session: Optional[_Session] = None,
    ) -> None: ...
