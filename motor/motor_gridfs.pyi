import datetime
from asyncio import AbstractEventLoop
from os import SEEK_SET as _SEEK_SET
from types import TracebackType
from typing import (
    Any,
    Awaitable,
    Dict,
    Iterable,
    List,
    Mapping,
    NoReturn,
    Optional,
    Type,
    Union,
)

from gridfs.grid_file import GridIn, GridOut
from pymongo.client_session import ClientSession
from typing_extensions import Literal, Protocol, Self

from .core import AgnosticCollection, AgnosticCursor
from .metaprogramming import ReadOnlyProperty

_IO_Loop = AbstractEventLoop
_Handler = Any  # Replace it with tornado.web.RequestHandler

class MotorGridOutProperty(ReadOnlyProperty):
    pass

class AgnosticGridOutCursor(AgnosticCursor):
    def next_object(self) -> Optional[AgnosticGridOut]: ...

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
        delegate: GridOut = None,
        session: ClientSession = None,
        **kwargs: Any,
    ) -> None: ...
    async def __aiter__(self) -> Self: ...
    async def __anext__(self) -> bytes: ...
    def __getattr__(self, name: str) -> Any: ...
    async def _ensure_file(self) -> None: ...
    async def close(self) -> None: ...
    def get_io_loop(self) -> _IO_Loop: ...
    async def open(self) -> Self: ...
    def read(self, size: int = -1) -> bytes: ...
    def readable(self) -> Literal[True]: ...
    async def readchunk(self) -> bytes: ...
    def readline(self, size: int = -1) -> bytes: ...
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
        delegate: GridIn = None,
        session: ClientSession = None,
        **kwargs: Any,
    ): ...
    async def __aenter__(self) -> Self: ...
    async def __aexit__(
        self,
        exc_type: Optional[Type[Exception]],
        exc_val: Optional[Exception],
        exc_tb: Optional[TracebackType],
    ) -> None: ...
    def __getattr__(self, name: str) -> Any: ...
    async def _exit(
        self,
        exc_type: Optional[Type[Exception]],
        exc_val: Optional[Exception],
        exc_tb: Optional[TracebackType],
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

class AgnosticGridFSBucket(object): ...
