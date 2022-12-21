import typing
from asyncio import AbstractEventLoop
from types import ModuleType

import bson
import pymongo
import pymongo.client_session
import pymongo.collation
import pymongo.database
import pymongo.read_concern
import pymongo.topology_description
import pymongo.typings

HAS_SSL: bool
ssl: ModuleType

_Type = typing.TypeVar('_Type', bound=typing.Type)
_Cursor = typing.TypeVar('_Cursor', bound=AgnosticBaseCursor)

_Database = typing.Union[pymongo.database.Database, AgnosticDatabase]
_Session = typing.Union[pymongo.client_session.ClientSession, AgnosticClientSession]
_ReadPreferences = typing.Union[
    pymongo.read_preferences.Primary,
    pymongo.read_preferences.PrimaryPreferred,
    pymongo.read_preferences.Secondary,
    pymongo.read_preferences.SecondaryPreferred,
    pymongo.read_preferences.Nearest,
]
_IO_Loop = AbstractEventLoop

class AgnosticBase(object):
    def __init__(self, delegate: _Type) -> None: ...

class AgnosticBaseProperties(AgnosticBase):
    codec_options: bson.codec_options.CodecOptions
    read_preference: _ReadPreferences
    read_concern: pymongo.read_concern.ReadConcern
    write_concern: pymongo.write_concern.WriteConcern

class AgnosticClient(AgnosticBaseProperties):
    HOST: str
    PORT: int
    address: typing.Optional[typing.Tuple[str, int]]
    arbiters: typing.Set[typing.Tuple[str, int]]
    is_mongos: bool
    is_primary: bool
    io_loop: _IO_Loop
    nodes: typing.FrozenSet[str, typing.Optional[int]]
    options: pymongo.mongo_client.ClientOptions
    primary: typing.Optional[typing.Tuple[str, int]]
    secondaries: typing.Set[typing.Tuple[str, int]]
    topology_description: pymongo.topology_description.TopologyDescription

    def __getitem__(self, item: str) -> AgnosticDatabase: ...
    def __getattr__(self, item: str) -> AgnosticDatabase: ...
    def __init__(
        self,
        host: typing.Optional[typing.Union[str, typing.Sequence[str]]] = None,
        port: typing.Optional[int] = None,
        document_class: typing.Optional[
            typing.Type[typing.Mapping[str, typing.Any]]
        ] = None,
        tz_aware: typing.Optional[bool] = None,
        connect: typing.Optional[bool] = None,
        type_registry: typing.Optional[bson.codec_options.TypeRegistry] = None,
        **kwargs: typing.Any,
    ) -> None: ...
    def close(self) -> None: ...
    async def drop_database(
        self,
        name_or_database: typing.Union[str, _Database],
        session: typing.Optional[_Session],
        comment: typing.Optional[typing.Any],
    ) -> None: ...
    def get_database(
        self,
        name: typing.Optional[str],
        codec_options: typing.Optional[bson.codec_options.CodecOptions],
        read_preferences: typing.Optional[_ReadPreferences],
        write_concern: typing.Optional[pymongo.write_concern.WriteConcern],
        read_concern: typing.Optional[pymongo.read_concern.ReadConcern],
    ) -> AgnosticDatabase: ...
    def get_default_database(
        self,
        default: typing.Optional[str],
        codec_options: typing.Optional[bson.codec_options.CodecOptions],
        read_preferences: typing.Optional[_ReadPreferences],
        write_concern: typing.Optional[pymongo.write_concern.WriteConcern],
        read_concern: typing.Optional[pymongo.read_concern.ReadConcern],
        comment: typing.Optional[typing.Any],
    ) -> AgnosticDatabase: ...
    def get_io_loop(self) -> _IO_Loop: ...
    async def list_database_names(
        self,
        session: typing.Optional[_Session],
        comment: typing.Optional[typing.Any],
    ) -> list[str]: ...
    async def list_databases(
        self,
        session: typing.Optional[_Session],
        comment: typing.Optional[typing.Any],
        **kwargs: typing.Any,
    ) -> AgnosticCommandCursor: ...
    async def server_info(
        self,
        session: typing.Optional[_Session],
    ) -> typing.Dict[str, typing.Any]: ...
    async def start_session(
        self,
        casual_consistency: typing.Optional[bool],
        default_transaction_options: typing.Optional[
            pymongo.client_session.TransactionOptions
        ] = None,
    ) -> AgnosticClientSession: ...
    def watch(
        self,
        pipeline: typing.Optional[
            typing.Sequence[typing.Mapping[str, typing.Any]]
        ] = None,
        full_document: typing.Optional[str] = None,
        resume_after: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        max_await_time_ms: typing.Optional[int] = None,
        batch_size: typing.Optional[int] = None,
        collation: typing.Optional[
            typing.Union[typing.Mapping[str, typing.Any], pymongo.collation.Collation]
        ] = None,
        start_at_operation_time: typing.Optional[bson.timestamp.Timestamp] = None,
        session: typing.Optional[_Session] = None,
        start_after: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
        full_document_before_change: typing.Optional[str] = None,
    ) -> AgnosticChangeStream: ...

class AgnosticClientSession(AgnosticBase): ...
class AgnosticDatabase(AgnosticBaseProperties): ...
class AgnosticCollection(AgnosticBaseProperties): ...
class AgnosticBaseCursor(AgnosticBase): ...
class AgnosticCursor(AgnosticBaseCursor): ...
class AgnosticRawBatchCursor(AgnosticCursor): ...
class AgnosticCommandCursor(AgnosticBaseCursor): ...
class AgnosticRawBatchCommandCursor(AgnosticCommandCursor): ...
class AgnosticLatentCommandCursor(AgnosticCommandCursor): ...
class AgnosticChangeStream(AgnosticBase): ...
class AgnosticClientEncryption(AgnosticBase): ...
