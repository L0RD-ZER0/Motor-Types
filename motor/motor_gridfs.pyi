import datetime
from asyncio import AbstractEventLoop
from types import TracebackType
from typing import Any, Iterable, NoReturn, Optional, Type

from gridfs.grid_file import GridIn
from pymongo.client_session import ClientSession
from typing_extensions import Literal, Self

from .core import AgnosticCollection, AgnosticCursor
from .metaprogramming import ReadOnlyProperty

_IO_Loop = AbstractEventLoop

class MotorGridOutProperty(ReadOnlyProperty):
    pass

class AgnosticGridOutCursor(AgnosticCursor):
    def next_object(self) -> Optional[AgnosticGridOut]: ...

class AgnosticGridOut(object): ...

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
