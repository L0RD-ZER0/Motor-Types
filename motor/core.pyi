import typing
from asyncio import AbstractEventLoop
from collections import deque as _deque
from types import ModuleType, TracebackType

import bson
import bson.raw_bson
import pymongo
import pymongo.client_session
import pymongo.collation
import pymongo.database
import pymongo.read_concern
import pymongo.results
import pymongo.topology_description
import pymongo.typings

HAS_SSL: bool
ssl: ModuleType

_Value = typing.TypeVar('_Value')
_Document = typing.TypeVar('_Document', bound=typing.Mapping[str, typing.Any])
_Type = typing.TypeVar('_Type', bound=typing.Type)
_Cursor = typing.TypeVar('_Cursor', bound=AgnosticBaseCursor)

_Collation = typing.Union[typing.Mapping[str, typing.Any], pymongo.collation.Collation]
_Collection = typing.Union[pymongo.collection.Collection, AgnosticCollection]
_Database = typing.Union[pymongo.database.Database, AgnosticDatabase]
_Pipeline = typing.Sequence[typing.Mapping[str, typing.Any]]
_Session = typing.Union[pymongo.client_session.ClientSession, AgnosticClientSession]
_ReadPreferences = typing.Union[
    pymongo.read_preferences.Primary,
    pymongo.read_preferences.PrimaryPreferred,
    pymongo.read_preferences.Secondary,
    pymongo.read_preferences.SecondaryPreferred,
    pymongo.read_preferences.Nearest,
]
_Operation = typing.Union[
    pymongo.operations.InsertOne,
    pymongo.operations.DeleteOne,
    pymongo.operations.DeleteMany,
    pymongo.operations.ReplaceOne,
    pymongo.operations.UpdateOne,
    pymongo.operations.UpdateMany,
]
_Index = typing.Sequence[
    typing.Tuple[str, typing.Union[int, str, typing.Mapping[str, typing.Any]]]
]
_Key_or_Index = typing.Union[str, _Index]
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

class _MotorTransactionContext:
    def __init__(self, session: _Session) -> None: ...
    async def __aenter__(self) -> _MotorTransactionContext: ...
    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[Exception]],
        exc_val: typing.Optional[Exception],
        exc_tb: typing.Optional[TracebackType],
    ) -> None: ...

class AgnosticClientSession(AgnosticBase):
    client: AgnosticClient
    cluster_time: typing.Optional[typing.Mapping[str, typing.Any]]
    has_ended: bool
    in_transaction: bool
    options: pymongo.client_session.SessionOptions
    operation_time: typing.Optional[bson.timestamp.Timestamp]
    session_id: typing.Mapping[str, typing.Any]

    async def __aenter__(self) -> AgnosticClientSession: ...
    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[Exception]],
        exc_val: typing.Optional[Exception],
        exc_tb: typing.Optional[TracebackType],
    ) -> None: ...
    def __enter__(self) -> typing.NoReturn: ...
    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[Exception]],
        exc_val: typing.Optional[Exception],
        exc_tb: typing.Optional[TracebackType],
    ) -> None: ...
    def advance_cluster_time(
        self, cluster_time: typing.Mapping[str, typing.Any]
    ) -> None: ...
    def advance_operation_time(self, operation_time: bson.timestamp.Timestamp): ...
    async def abort_transaction(self) -> None: ...
    async def commit_transaction(self) -> None: ...
    async def end_session(self) -> None: ...
    def get_io_loop(self) -> _IO_Loop: ...
    def start_transaction(
        self,
        read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
        write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
        read_preference: typing.Optional[_ReadPreferences] = None,
        max_commit_time_ns: typing.Optional[int] = None,
    ) -> _MotorTransactionContext: ...
    async def with_transaction(
        self,
        coro: typing.Callable[[AgnosticClientSession], typing.Awaitable[_Value]],
        read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
        write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
        read_preference: typing.Optional[_ReadPreferences] = None,
        max_commit_time_ns: typing.Optional[int] = None,
    ) -> _Value: ...

class AgnosticDatabase(AgnosticBaseProperties):
    name: str
    client: AgnosticClient

    def __bool__(self) -> typing.NoReturn: ...
    def __getitem__(self) -> AgnosticCollection: ...
    def __getattr__(self) -> AgnosticCollection: ...
    def __hash__(self) -> int: ...
    def __init__(self, client: AgnosticClient, name: str, **kwargs: typing.Any): ...
    def aggregate(
        self, pipeline: _Pipeline, *args: typing.Any, **kwargs: typing.Any
    ) -> AgnosticLatentCommandCursor: ...
    async def command(
        self,
        command: typing.Union[str, typing.MutableMapping[str, typing.Any]],
        value: typing.Any = 1,
        check: bool = True,
        allowable_errors: typing.Optional[
            typing.Sequence[typing.Union[str, int]]
        ] = None,
        read_preference: typing.Optional[_ReadPreferences] = None,
        codec_options: typing.Optional[
            bson.codec_options.CodecOptions[_Document]
        ] = None,
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> _Document: ...
    async def create_collection(
        self,
        name: str,
        codec_options: typing.Optional[bson.codec_options.CodecOptions] = None,
        read_preference: typing.Optional[_ReadPreferences] = None,
        write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
        read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
        session: typing.Optional[_Session] = None,
        check_exists: typing.Optional[bool] = True,
        **kwargs: typing.Any,
    ) -> AgnosticCollection: ...
    async def dereference(
        self,
        dbref: bson.dbref.DBRef,
        session: typing.Optional[_Session],
        comment: typing.Optional[typing.Any],
        **kwargs: typing.Any,
    ) -> _Document: ...
    async def drop_collection(
        self,
        name_or_collection: typing.Union[str, _Collection],
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
        encrypted_fields: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    ) -> typing.Dict[str, typing.Any]: ...
    def get_collection(
        self,
        name: str,
        codec_options: typing.Optional[bson.codec_options.CodecOptions] = None,
        read_preference: typing.Optional[_ReadPreferences] = None,
        write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
        read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
    ) -> AgnosticCollection: ...
    def get_io_loop(self) -> _IO_Loop: ...
    async def list_collection_names(
        self,
        session: typing.Optional[_Session] = None,
        filter: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> typing.List[str]: ...
    async def list_collections(
        self,
        session: typing.Optional[_Session] = None,
        filter: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> AgnosticCommandCursor: ...
    async def validate_collection(
        self,
        name_or_collection: typing.Union[str, _Collection],
        scandata: bool = False,
        full: bool = False,
        session: typing.Optional[_Session] = None,
        background: typing.Optional[bool] = None,
        comment: typing.Optional[typing.Any] = None,
    ) -> typing.Dict[str, typing.Any]: ...
    def watch(
        self,
        pipeline: typing.Optional[_Pipeline] = None,
        full_document: typing.Optional[str] = None,
        resume_after: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        max_await_time_ms: typing.Optional[int] = None,
        batch_size: typing.Optional[int] = None,
        collation: typing.Optional[_Collation] = None,
        start_at_operation_time: typing.Optional[bson.timestamp.Timestamp] = None,
        session: typing.Optional[_Session] = None,
        start_after: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
        full_document_before_change: typing.Optional[str] = None,
    ) -> AgnosticChangeStream: ...
    def with_options(
        self,
        codec_options: typing.Optional[bson.codec_options.CodecOptions] = None,
        read_preference: typing.Optional[_ReadPreferences] = None,
        write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
        read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
    ) -> AgnosticDatabase: ...

class AgnosticCollection(AgnosticBaseProperties):
    name: str
    full_name: str

    def __hash__(self) -> int: ...
    def __bool__(self) -> typing.NoReturn: ...
    def __getitem__(self, item: str) -> AgnosticCollection: ...
    def __getattr__(self, item: str) -> AgnosticCollection: ...
    def __init__(
        self,
        database: AgnosticDatabase,
        name: str,
        codec_options: typing.Optional[bson.codec_options.CodecOptions] = None,
        read_preference: typing.Optional[_ReadPreferences] = None,
        write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
        read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
        _delegate: typing.Optional[pymongo.collection.Collection] = None,
    ): ...
    def aggregate(
        self,
        pipeline: _Pipeline,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> AgnosticLatentCommandCursor: ...
    def aggregate_raw_batches(
        self,
        pipeline: _Pipeline,
        **kwargs: typing.Any,
    ) -> AgnosticLatentCommandCursor: ...
    async def bulk_write(
        self,
        requests: typing.Sequence[_Operation],
        ordered: bool = True,
        bypass_document_validation: bool = False,
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
        let: typing.Optional[typing.Mapping] = None,
    ) -> pymongo.results.BulkWriteResult: ...
    async def count_documents(
        self,
        filter: typing.Mapping[str, typing.Any],
        session: typing.Optional[_Session],
        comment: typing.Optional[typing.Any],
        **kwargs: typing.Any,
    ) -> int: ...
    async def create_index(
        self,
        keys: _Key_or_Index,
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> str: ...
    async def create_indexes(
        self,
        indexes: typing.Sequence[pymongo.operations.IndexModel],
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> typing.List: ...
    async def delete_many(
        self,
        filter: typing.Mapping[str, typing.Any],
        collation: typing.Optional[_Collation] = None,
        hint: typing.Optional[_Key_or_Index] = None,
        session: typing.Optional[_Session] = None,
        let: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
    ) -> pymongo.results.DeleteResult: ...
    async def delete_one(
        self,
        filter: typing.Mapping[str, typing.Any],
        collation: typing.Optional[_Collation] = None,
        hint: typing.Optional[_Key_or_Index] = None,
        session: typing.Optional[_Session] = None,
        let: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
    ) -> pymongo.results.DeleteResult: ...
    async def distinct(
        self,
        key: str,
        filter: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> typing.List: ...
    async def drop(
        self,
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
        encrypted_fields: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    ) -> None: ...
    async def drop_index(
        self,
        index_or_name: _Key_or_Index,
        session: typing.Optional[_Session],
        comment: typing.Optional[typing.Any],
        **kwargs: typing.Any,
    ) -> None: ...
    async def drop_indexes(
        self,
        session: typing.Optional[_Session],
        comment: typing.Optional[typing.Any],
        **kwargs: typing.Any,
    ) -> None: ...
    async def estimated_document_count(
        self,
        comment: typing.Optional[typing.Any],
        **kwargs: typing.Any,
    ) -> int: ...
    def find(
        self,
        filter: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        projection: typing.Optional[
            typing.Mapping[str, typing.Any] | typing.Iterable[str]
        ] = None,
        skip: int = 0,
        limit: int = 0,
        no_cursor_timeout: bool = False,
        cursor_type: int = pymongo.cursor.CursorType.NON_TAILABLE,
        sort: typing.Optional[
            typing.Sequence[tuple[str, int | str | typing.Mapping[str, typing.Any]]]
        ] = None,
        allow_partial_results: bool = False,
        oplog_replay: bool = False,
        batch_size: int = 0,
        collation: typing.Optional[typing.Mapping[str, typing.Any] | _Collation] = None,
        hint: typing.Optional[
            str
            | typing.Sequence[tuple[str, int | str | typing.Mapping[str, typing.Any]]]
        ] = None,
        max_scan: typing.Optional[int] = None,
        max_time_ms: typing.Optional[int] = None,
        max: typing.Optional[
            typing.Sequence[tuple[str, int | str | typing.Mapping[str, typing.Any]]]
        ] = None,
        min: typing.Optional[
            typing.Sequence[tuple[str, int | str | typing.Mapping[str, typing.Any]]]
        ] = None,
        return_key: typing.Optional[bool] = None,
        show_record_id: typing.Optional[bool] = None,
        snapshot: typing.Optional[bool] = None,
        comment: typing.Optional[typing.Any] = None,
        session: typing.Optional[_Session] = None,
        allow_disk_use: typing.Optional[bool] = None,
        let: typing.Optional[bool] = None,
    ) -> AgnosticCursor: ...
    async def find_one(
        self,
        filter: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        projection: typing.Optional[
            typing.Mapping[str, typing.Any] | typing.Iterable[str]
        ] = None,
        skip: int = 0,
        limit: int = 0,  # Ignored by the driver.
        no_cursor_timeout: bool = False,
        cursor_type: int = pymongo.cursor.CursorType.NON_TAILABLE,
        sort: typing.Optional[
            typing.Sequence[tuple[str, int | str | typing.Mapping[str, typing.Any]]]
        ] = None,
        allow_partial_results: bool = False,
        oplog_replay: bool = False,
        batch_size: int = 0,
        collation: typing.Optional[typing.Mapping[str, typing.Any] | _Collation] = None,
        hint: typing.Optional[
            str
            | typing.Sequence[tuple[str, int | str | typing.Mapping[str, typing.Any]]]
        ] = None,
        max_scan: typing.Optional[int] = None,
        max_time_ms: typing.Optional[int] = None,
        max: typing.Optional[
            typing.Sequence[tuple[str, int | str | typing.Mapping[str, typing.Any]]]
        ] = None,
        min: typing.Optional[
            typing.Sequence[tuple[str, int | str | typing.Mapping[str, typing.Any]]]
        ] = None,
        return_key: typing.Optional[bool] = None,
        show_record_id: typing.Optional[bool] = None,
        snapshot: typing.Optional[bool] = None,
        comment: typing.Optional[typing.Any] = None,
        session: typing.Optional[_Session] = None,
        allow_disk_use: typing.Optional[bool] = None,
        let: typing.Optional[bool] = None,
    ) -> typing.Optional[_Document]: ...
    async def find_one_and_delete(
        self,
        filter: typing.Mapping[str, typing.Any],
        projection: typing.Optional[
            typing.Union[typing.Mapping[str, typing.Any], typing.Iterable[str]]
        ] = None,
        sort: typing.Optional[_Index] = None,
        hint: typing.Optional[_Key_or_Index] = None,
        session: typing.Optional[_Session] = None,
        let: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> _Document: ...
    async def find_one_and_replace(
        self,
        filter: typing.Mapping[str, typing.Any],
        replacement: typing.Mapping[str, typing.Any],
        projection: typing.Optional[
            typing.Union[typing.Mapping[str, typing.Any], typing.Iterable[str]]
        ] = None,
        sort: typing.Optional[_Index] = None,
        upsert: bool = False,
        return_document: bool = pymongo.collection.ReturnDocument.BEFORE,
        hint: typing.Optional[_Key_or_Index] = None,
        session: typing.Optional[_Session] = None,
        let: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> _Document: ...
    async def find_one_and_update(
        self,
        filter: typing.Mapping[str, typing.Any],
        update: typing.Union[typing.Mapping[str, typing.Any], _Pipeline],
        projection: typing.Optional[
            typing.Union[typing.Mapping[str, typing.Any], typing.Iterable[str]]
        ] = None,
        sort: typing.Optional[_Index] = None,
        upsert: bool = False,
        return_document: bool = pymongo.collection.ReturnDocument.BEFORE,
        array_filters: typing.Optional[
            typing.Sequence[typing.Mapping[str, typing.Any]]
        ] = None,
        hint: typing.Optional[_Key_or_Index] = None,
        session: typing.Optional[_Session] = None,
        let: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> _Document: ...
    def find_raw_batches(
        self,
        filter: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        projection: typing.Optional[
            typing.Mapping[str, typing.Any] | typing.Iterable[str]
        ] = None,
        skip: int = 0,
        limit: int = 0,
        no_cursor_timeout: bool = False,
        cursor_type: int = pymongo.cursor.CursorType.NON_TAILABLE,
        sort: typing.Optional[
            typing.Sequence[tuple[str, int | str | typing.Mapping[str, typing.Any]]]
        ] = None,
        allow_partial_results: bool = False,
        oplog_replay: bool = False,
        batch_size: int = 0,
        collation: typing.Optional[typing.Mapping[str, typing.Any] | _Collation] = None,
        hint: typing.Optional[
            str
            | typing.Sequence[tuple[str, int | str | typing.Mapping[str, typing.Any]]]
        ] = None,
        max_scan: typing.Optional[int] = None,
        max_time_ms: typing.Optional[int] = None,
        max: typing.Optional[
            typing.Sequence[tuple[str, int | str | typing.Mapping[str, typing.Any]]]
        ] = None,
        min: typing.Optional[
            typing.Sequence[tuple[str, int | str | typing.Mapping[str, typing.Any]]]
        ] = None,
        return_key: typing.Optional[bool] = None,
        show_record_id: typing.Optional[bool] = None,
        snapshot: typing.Optional[bool] = None,
        comment: typing.Optional[typing.Any] = None,
        session: typing.Optional[_Session] = None,
        allow_disk_use: typing.Optional[bool] = None,
        let: typing.Optional[bool] = None,
    ) -> AgnosticRawBatchCursor: ...
    def get_io_loop(self) -> _IO_Loop: ...
    async def index_information(
        self,
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
    ) -> typing.MutableMapping[str, typing.Any]: ...
    async def insert_many(
        self,
        documents: typing.Iterable[
            typing.Union[_Document, bson.raw_bson.RawBSONDocument]
        ],
        ordered: bool = True,
        bypass_document_validation: bool = False,
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
    ) -> pymongo.results.InsertManyResult: ...
    async def insert_one(
        self,
        document: typing.Union[_Document, bson.raw_bson.RawBSONDocument],
        bypass_document_validation: bool = False,
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
    ) -> pymongo.results.InsertOneResult: ...
    def list_indexes(
        self,
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
    ) -> AgnosticLatentCommandCursor: ...
    async def options(
        self,
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
    ) -> typing.MutableMapping[str, typing.Any]: ...
    async def rename(
        self,
        new_name: str,
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> typing.MutableMapping[str, typing.Any]: ...
    async def replace_one(
        self,
        filter: typing.Mapping[str, typing.Any],
        replacement: typing.Mapping[str, typing.Any],
        upsert: bool = False,
        bypass_document_validation: bool = False,
        collation: typing.Optional[_Collation] = None,
        hint: typing.Optional[_Key_or_Index] = None,
        session: typing.Optional[_Session] = None,
        let: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
    ) -> pymongo.results.UpdateResult: ...
    async def update_many(
        self,
        filter: typing.Mapping[str, typing.Any],
        update: typing.Union[typing.Mapping[str, typing.Any], _Pipeline],
        upsert: bool = False,
        array_filters: typing.Optional[
            typing.Sequence[typing.Mapping[str, typing.Any]]
        ] = None,
        bypass_document_validation: typing.Optional[bool] = None,
        collation: typing.Optional[_Collation] = None,
        hint: typing.Optional[_Key_or_Index] = None,
        session: typing.Optional[_Session] = None,
        let: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
    ) -> pymongo.results.UpdateResult: ...
    async def update_one(
        self,
        filter: typing.Mapping[str, typing.Any],
        update: typing.Union[typing.Mapping[str, typing.Any], _Pipeline],
        upsert: bool = False,
        bypass_document_validation: bool = False,
        collation: typing.Optional[_Collation] = None,
        array_filters: typing.Optional[
            typing.Sequence[typing.Mapping[str, typing.Any]]
        ] = None,
        hint: typing.Optional[_Key_or_Index] = None,
        session: typing.Optional[_Session] = None,
        let: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
    ) -> pymongo.results.UpdateResult: ...
    def watch(
        self,
        pipeline: typing.Optional[_Pipeline] = None,
        full_document: typing.Optional[str] = None,
        resume_after: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        max_await_time_ms: typing.Optional[int] = None,
        batch_size: typing.Optional[int] = None,
        collation: typing.Optional[_Collation] = None,
        start_at_operation_time: typing.Optional[bson.timestamp.Timestamp] = None,
        session: typing.Optional[_Session] = None,
        start_after: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
        full_document_before_change: typing.Optional[str] = None,
    ) -> AgnosticChangeStream: ...
    def with_options(
        self,
        codec_options: typing.Optional[bson.codec_options.CodecOptions] = None,
        read_preference: typing.Optional[_ReadPreferences] = None,
        write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
        read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
    ) -> AgnosticCollection: ...

class AgnosticBaseCursor(AgnosticBase):
    address: typing.Optional[typing.Tuple[str, typing.Any]]
    alive: bool
    cursor_id: typing.Optional[int]
    fetch_next: typing.Awaitable[typing.Union[bool, int]]
    session: typing.Optional[AgnosticClientSession]

    def __init__(
        self, cursor: pymongo.cursor.Cursor, collection: AgnosticCollection
    ) -> None: ...
    def __aiter__(self) -> AgnosticBaseCursor: ...
    async def __aenter__(self) -> AgnosticBaseCursor: ...
    async def __anext__(self) -> _Document: ...
    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[Exception]],
        exc_val: typing.Optional[Exception],
        exc_tb: typing.Optional[TracebackType],
    ) -> None: ...
    async def _async_close(self) -> None: ...
    def _buffer_size(self) -> int: ...
    def _data(self) -> typing.NoReturn: ...
    def _killed(self) -> typing.NoReturn: ...
    def _query_flags(self) -> typing.NoReturn: ...
    async def _refresh(self) -> int: ...
    def batch_size(self, batch_size: int) -> AgnosticBaseCursor: ...
    async def close(self) -> None: ...
    def each(
        self,
        callback: typing.Callable[
            [typing.Optional[_Document], typing.Optional[Exception]], typing.Any
        ],
    ): ...
    def get_io_loop(self) -> _IO_Loop: ...
    async def next(self) -> _Document: ...
    def next_object(self) -> _Document: ...
    async def to_list(self, length: int) -> typing.List[_Document]: ...

class AgnosticCursor(AgnosticBaseCursor):
    def __aiter__(self) -> AgnosticCursor: ...
    async def __aenter__(self) -> AgnosticCursor: ...
    def __copy__(self) -> AgnosticCursor: ...
    def __deepcopy__(
        self, memodict: typing.Optional[typing.Dict] = None
    ) -> AgnosticCursor: ...
    async def _Cursor__die(self, synchronous=False) -> None: ...
    def _data(self) -> _deque: ...
    def _killed(self) -> bool: ...
    def _query_flags(self) -> int: ...
    def allow_disk_use(self, allow_disk_use: bool) -> AgnosticCursor: ...
    def add_option(self, mask: int) -> AgnosticCursor: ...
    def batch_size(self, batch_size: int) -> AgnosticCursor: ...
    def clone(self) -> AgnosticCursor: ...
    def collation(self, collation: _Collation) -> AgnosticCursor: ...
    def comment(self, comment: typing.Any) -> AgnosticCursor: ...
    async def distinct(self, key: str) -> typing.List: ...
    async def explain(self) -> _Document: ...
    def hint(self, index: typing.Optional[_Index]) -> AgnosticCursor: ...
    def limit(self, limit: int) -> AgnosticCursor: ...
    def max(self, spec: _Index) -> AgnosticCursor: ...
    def max_await_time_ms(
        self, max_await_time_ms: typing.Optional[int]
    ) -> AgnosticCursor: ...
    def max_scan(self, max_scan: typing.Optional[int]) -> AgnosticCursor: ...
    def max_time_ms(self, max_time_ms: typing.Optional[int]) -> AgnosticCursor: ...
    def min(self, spec: _Index) -> AgnosticCursor: ...
    def remove_option(self, mask: int) -> AgnosticCursor: ...
    def rewind(self) -> AgnosticCursor: ...
    def skip(self, skip: int) -> AgnosticCursor: ...
    def sort(
        self,
        key_or_list: _Key_or_Index,
        direction: typing.Optional[typing.Union[int, str]] = None,
    ) -> AgnosticCursor: ...
    def where(self, code: typing.Union[str, bson.code.Code]) -> AgnosticCursor: ...

class AgnosticRawBatchCursor(AgnosticCursor):
    def __aiter__(self) -> AgnosticRawBatchCursor: ...
    async def __aenter__(self) -> AgnosticRawBatchCursor: ...
    def __copy__(self) -> AgnosticRawBatchCursor: ...
    def __deepcopy__(
        self, memodict: typing.Optional[typing.Dict] = None
    ) -> AgnosticRawBatchCursor: ...
    def allow_disk_use(self, allow_disk_use: bool) -> AgnosticRawBatchCursor: ...
    def add_option(self, mask: int) -> AgnosticRawBatchCursor: ...
    def batch_size(self, batch_size: int) -> AgnosticRawBatchCursor: ...
    def clone(self) -> AgnosticRawBatchCursor: ...
    def collation(self, collation: _Collation) -> AgnosticRawBatchCursor: ...
    def comment(self, comment: typing.Any) -> AgnosticRawBatchCursor: ...
    def hint(self, index: typing.Optional[_Index]) -> AgnosticRawBatchCursor: ...
    def limit(self, limit: int) -> AgnosticRawBatchCursor: ...
    def max(self, spec: _Index) -> AgnosticRawBatchCursor: ...
    def max_await_time_ms(
        self, max_await_time_ms: typing.Optional[int]
    ) -> AgnosticRawBatchCursor: ...
    def max_scan(self, max_scan: typing.Optional[int]) -> AgnosticRawBatchCursor: ...
    def max_time_ms(
        self, max_time_ms: typing.Optional[int]
    ) -> AgnosticRawBatchCursor: ...
    def min(self, spec: _Index) -> AgnosticRawBatchCursor: ...
    def remove_option(self, mask: int) -> AgnosticRawBatchCursor: ...
    def rewind(self) -> AgnosticRawBatchCursor: ...
    def skip(self, skip: int) -> AgnosticRawBatchCursor: ...
    def sort(
        self,
        key_or_list: _Key_or_Index,
        direction: typing.Optional[typing.Union[int, str]] = None,
    ) -> AgnosticRawBatchCursor: ...
    def where(
        self, code: typing.Union[str, bson.code.Code]
    ) -> AgnosticRawBatchCursor: ...

class AgnosticCommandCursor(AgnosticBaseCursor):
    def __aiter__(self) -> AgnosticBaseCursor: ...
    async def __aenter__(self) -> AgnosticBaseCursor: ...
    async def _Cursor__die(self, synchronous=False) -> None: ...
    def _data(self) -> _deque: ...
    def _killed(self) -> bool: ...
    def _query_flags(self) -> typing.Literal[0]: ...
    def batch_size(self, batch_size: int) -> AgnosticCommandCursor: ...

class AgnosticRawBatchCommandCursor(AgnosticCommandCursor):
    def __aiter__(self) -> AgnosticRawBatchCommandCursor: ...
    async def __aenter__(self) -> AgnosticRawBatchCommandCursor: ...
    def batch_size(self, batch_size: int) -> AgnosticRawBatchCommandCursor: ...

class AgnosticLatentCommandCursor(AgnosticCommandCursor): ...
class AgnosticChangeStream(AgnosticBase): ...
class AgnosticClientEncryption(AgnosticBase): ...
