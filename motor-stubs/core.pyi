import typing
from asyncio import AbstractEventLoop
from collections import deque as _deque
from types import ModuleType, TracebackType

import bson
import bson.binary
import bson.code
import bson.codec_options
import bson.dbref
import bson.raw_bson
import bson.timestamp
import pymongo
import pymongo.client_session
import pymongo.collation
import pymongo.collection
import pymongo.command_cursor
import pymongo.cursor
import pymongo.database
import pymongo.encryption
import pymongo.mongo_client
import pymongo.operations
import pymongo.read_concern
import pymongo.read_preferences
import pymongo.results
import pymongo.topology_description
import pymongo.typings
import pymongo.write_concern
from typing_extensions import Self

HAS_SSL: bool
ssl: ModuleType

_Self = typing.TypeVar('_Self')

_Value = typing.TypeVar('_Value')
# _Document = typing.TypeVar('_Document', bound=typing.Mapping[str, typing.Any])
_Type = typing.TypeVar('_Type', bound=typing.Type)
_Cursor = typing.TypeVar('_Cursor', bound=AgnosticBaseCursor)

_Document = dict[str, typing.Any]
_Collation = typing.Union[typing.Mapping[str, typing.Any], pymongo.collation.Collation]
_Collection = typing.Union[
    pymongo.collection.Collection[_Document], AgnosticCollection
]
_Database = typing.Union[pymongo.database.Database[_Document], AgnosticDatabase]
_Pipeline = list[dict[str, typing.Any]]
_Session = typing.Union[pymongo.client_session.ClientSession, AgnosticClientSession]
_ReadPreferences = typing.Union[
    pymongo.read_preferences.Primary,
    pymongo.read_preferences.PrimaryPreferred,
    pymongo.read_preferences.Secondary,
    pymongo.read_preferences.SecondaryPreferred,
    pymongo.read_preferences.Nearest,
]
_Operation = typing.Union[
    pymongo.operations.InsertOne[_Document],
    pymongo.operations.DeleteOne,
    pymongo.operations.DeleteMany,
    pymongo.operations.ReplaceOne[_Document],
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
    codec_options: bson.codec_options.CodecOptions[typing.Any]
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
    nodes: typing.FrozenSet[typing.Tuple[str, typing.Optional[int]]]
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
            session: typing.Optional[_Session] = None,
            comment: typing.Optional[typing.Any] = None,
    ) -> None: ...

    def get_database(
            self,
            name: typing.Optional[str] = None,
            codec_options: typing.Optional[
                bson.codec_options.CodecOptions[typing.Any]
            ] = None,
            read_preference: typing.Optional[_ReadPreferences] = None,
            write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
            read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
    ) -> AgnosticDatabase: ...

    def get_default_database(
            self,
            default: typing.Optional[str] = None,
            codec_options: typing.Optional[
                bson.codec_options.CodecOptions[typing.Any]
            ] = None,
            read_preference: typing.Optional[_ReadPreferences] = None,
            write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
            read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
            comment: typing.Optional[typing.Any] = None,
    ) -> AgnosticDatabase: ...

    def get_io_loop(self) -> _IO_Loop: ...

    async def list_database_names(
            self,
            session: typing.Optional[_Session] = None,
            comment: typing.Optional[typing.Any] = None,
    ) -> list[str]: ...

    async def list_databases(
            self,
            session: typing.Optional[_Session] = None,
            comment: typing.Optional[typing.Any] = None,
            **kwargs: typing.Any,
    ) -> AgnosticCommandCursor: ...

    async def server_info(
            self,
            session: typing.Optional[_Session] = None,
    ) -> typing.Dict[str, typing.Any]: ...

    async def start_session(
            self,
            causal_consistency: typing.Optional[bool] = None,
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

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
            self,
            exc_type: typing.Optional[typing.Type[Exception]] = None,
            exc_val: typing.Optional[Exception] = None,
            exc_tb: typing.Optional[TracebackType] = None,
    ) -> None: ...


class AgnosticClientSession(AgnosticBase):
    client: AgnosticClient
    cluster_time: typing.Optional[typing.Mapping[str, typing.Any]]
    has_ended: bool
    in_transaction: bool
    options: pymongo.client_session.SessionOptions
    operation_time: typing.Optional[bson.timestamp.Timestamp]
    session_id: typing.Mapping[str, typing.Any]

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
            self,
            exc_type: typing.Optional[typing.Type[Exception]] = None,
            exc_val: typing.Optional[Exception] = None,
            exc_tb: typing.Optional[TracebackType] = None,
    ) -> None: ...

    def __enter__(self) -> typing.NoReturn: ...

    def __exit__(
            self,
            exc_type: typing.Optional[typing.Type[Exception]] = None,
            exc_val: typing.Optional[Exception] = None,
            exc_tb: typing.Optional[TracebackType] = None,
    ) -> None: ...

    def advance_cluster_time(
            self, cluster_time: typing.Mapping[str, typing.Any]
    ) -> None: ...

    def advance_operation_time(
            self, operation_time: bson.timestamp.Timestamp
    ) -> None: ...

    async def abort_transaction(self) -> None: ...

    async def commit_transaction(self) -> None: ...

    async def end_session(self) -> None: ...

    def get_io_loop(self) -> _IO_Loop: ...

    def start_transaction(
            self,
            read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
            write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
            read_preference: typing.Optional[_ReadPreferences] = None,
            max_commit_time_ms: typing.Optional[int] = None,
    ) -> _MotorTransactionContext: ...

    async def with_transaction(
            self,
            coro: typing.Callable[[Self], typing.Awaitable[_Value]],
            read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
            write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
            read_preference: typing.Optional[_ReadPreferences] = None,
            max_commit_time_ms: typing.Optional[int] = None,
    ) -> _Value: ...


class AgnosticDatabase(AgnosticBaseProperties):
    name: str
    client: AgnosticClient

    def __bool__(self) -> typing.NoReturn: ...

    def __getitem__(self, item: str) -> AgnosticCollection: ...

    def __getattr__(self, item: str) -> AgnosticCollection: ...

    def __hash__(self) -> int: ...

    def __init__(
            self, client: AgnosticClient, name: str, **kwargs: typing.Any
    ) -> None: ...

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
            codec_options: typing.Optional[
                bson.codec_options.CodecOptions[typing.Any]
            ] = None,
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
            session: typing.Optional[_Session] = None,
            comment: typing.Optional[typing.Any] = None,
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
            codec_options: typing.Optional[
                bson.codec_options.CodecOptions[typing.Any]
            ] = None,
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
            codec_options: typing.Optional[
                bson.codec_options.CodecOptions[typing.Any]
            ] = None,
            read_preference: typing.Optional[_ReadPreferences] = None,
            write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
            read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
    ) -> Self: ...


class AgnosticCollection(AgnosticBaseProperties):
    name: str
    full_name: str

    def __hash__(self) -> int: ...

    def __bool__(self) -> typing.NoReturn: ...

    def __getitem__(self, item: str) -> Self: ...

    def __getattr__(self, item: str) -> Self: ...

    def __init__(
            self,
            database: AgnosticDatabase,
            name: str,
            codec_options: typing.Optional[
                bson.codec_options.CodecOptions[typing.Any]
            ] = None,
            read_preference: typing.Optional[_ReadPreferences] = None,
            write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
            read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
            _delegate: typing.Optional[pymongo.collection.Collection[_Document]] = None,
    ) -> None: ...

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
            let: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    ) -> pymongo.results.BulkWriteResult: ...

    async def count_documents(
            self,
            filter: typing.Mapping[str, typing.Any],
            session: typing.Optional[_Session] = None,
            comment: typing.Optional[typing.Any] = None,
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
    ) -> typing.List[typing.Any]: ...

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
    ) -> typing.List[typing.Any]: ...

    async def drop(
            self,
            session: typing.Optional[_Session] = None,
            comment: typing.Optional[typing.Any] = None,
            encrypted_fields: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    ) -> None: ...

    async def drop_index(
            self,
            index_or_name: _Key_or_Index,
            session: typing.Optional[_Session] = None,
            comment: typing.Optional[typing.Any] = None,
            **kwargs: typing.Any,
    ) -> None: ...

    async def drop_indexes(
            self,
            session: typing.Optional[_Session] = None,
            comment: typing.Optional[typing.Any] = None,
            **kwargs: typing.Any,
    ) -> None: ...

    async def estimated_document_count(
            self,
            comment: typing.Optional[typing.Any] = None,
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
            # ``find_one`` can convert non-mapping types to a filter that looks like ``{"_id": <value>}``.
            filter: typing.Optional[
                typing.Union[typing.Mapping[str, typing.Any], typing.Any]
            ] = None,
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
            self: _Self,
            codec_options: typing.Optional[
                bson.codec_options.CodecOptions[typing.Any]
            ] = None,
            read_preference: typing.Optional[_ReadPreferences] = None,
            write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
            read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
    ) -> _Self: ...


class AgnosticBaseCursor(AgnosticBase):
    address: typing.Optional[typing.Tuple[str, typing.Any]]
    alive: bool
    cursor_id: typing.Optional[int]
    fetch_next: typing.Awaitable[typing.Union[bool, int]]
    session: typing.Optional[AgnosticClientSession]

    def __init__(
            self, cursor: pymongo.cursor.Cursor[_Document], collection: AgnosticCollection
    ) -> None: ...

    def __aiter__(self: _Self) -> _Self: ...

    async def __anext__(self) -> _Document: ...

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
            self,
            exc_type: typing.Optional[typing.Type[Exception]] = None,
            exc_val: typing.Optional[Exception] = None,
            exc_tb: typing.Optional[TracebackType] = None,
    ) -> None: ...

    async def _async_close(self) -> None: ...

    def _buffer_size(self) -> int: ...

    def _data(self) -> typing.NoReturn: ...

    def _killed(self) -> typing.NoReturn: ...

    def _query_flags(self) -> typing.NoReturn: ...

    async def _refresh(self) -> int: ...

    def batch_size(self, batch_size: int) -> Self: ...

    async def close(self) -> None: ...

    def each(
            self,
            callback: typing.Optional[
                typing.Callable[
                    [typing.Optional[_Document], typing.Optional[Exception]], typing.Any
                ]
            ] = None,
    ) -> None: ...

    def get_io_loop(self) -> _IO_Loop: ...

    async def next(self) -> _Document: ...

    def next_object(self) -> _Document: ...

    async def to_list(self, length: typing.Optional[int]) -> typing.List[_Document]: ...


class AgnosticCursor(AgnosticBaseCursor):
    def __copy__(self) -> Self: ...

    def __deepcopy__(
            self, memodict: typing.Optional[typing.Dict[str, typing.Any]] = None
    ) -> Self: ...

    async def _Cursor__die(self, synchronous: bool = False) -> None: ...

    def _data(self) -> _deque: ...

    def _killed(self) -> bool: ...

    def _query_flags(self) -> int: ...

    def allow_disk_use(self, allow_disk_use: bool) -> Self: ...

    def add_option(self, mask: int) -> Self: ...

    def clone(self) -> Self: ...

    def collation(self, collation: _Collation) -> Self: ...

    def comment(self, comment: typing.Any) -> Self: ...

    async def distinct(self, key: str) -> typing.List[typing.Any]: ...

    async def explain(self) -> _Document: ...

    def hint(self, index: typing.Optional[_Index]) -> Self: ...

    def limit(self: _Self, limit: int) -> _Self: ...

    def max(self, spec: _Index) -> Self: ...

    def max_await_time_ms(self, max_await_time_ms: typing.Optional[int]) -> Self: ...

    def max_scan(self, max_scan: typing.Optional[int]) -> Self: ...

    def max_time_ms(self, max_time_ms: typing.Optional[int]) -> Self: ...

    def min(self, spec: _Index) -> Self: ...

    def remove_option(self, mask: int) -> Self: ...

    def rewind(self) -> Self: ...

    def skip(self, skip: int) -> "AgnosticCursor": ...

    def sort(
            self,
            key_or_list: _Key_or_Index,
            direction: typing.Optional[typing.Union[int, str]] = None,
    ) -> "AgnosticCursor": ...

    def where(self, code: typing.Union[str, bson.code.Code]) -> Self: ...

    def batch_size(self, batch_size: int) -> "AgnosticCursor": ...


class AgnosticRawBatchCursor(AgnosticCursor):
    pass


class AgnosticCommandCursor(AgnosticBaseCursor):
    async def _Cursor__die(self, synchronous: bool = False) -> None: ...

    def _data(self) -> _deque: ...

    def _killed(self) -> bool: ...

    def _query_flags(self) -> typing.Literal[0]: ...


class AgnosticRawBatchCommandCursor(AgnosticCommandCursor):
    pass


class AgnosticLatentCommandCursor(AgnosticCommandCursor):
    args: typing.Optional[typing.Tuple[typing.Any]]
    kwargs: typing.Optional[typing.Dict[str, typing.Any]]
    start: typing.Optional[
        typing.Callable[[typing.Any], pymongo.command_cursor.CommandCursor[_Document]]
    ]

    def __init__(
            self,
            collection: AgnosticCollection,
            start: typing.Optional[
                typing.Callable[
                    [typing.Any], pymongo.command_cursor.CommandCursor[_Document]
                ]
            ] = None,
            *args: typing.Any,
            **kwargs: typing.Any,
    ) -> None: ...


class AgnosticChangeStream(AgnosticBase):
    alive: bool
    resume_token: typing.Optional[typing.Mapping[str, typing.Any]]

    def __init__(
            self,
            target: typing.Union[AgnosticClient, AgnosticDatabase, AgnosticCollection],
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
    ) -> None: ...

    def __aiter__(self) -> Self: ...

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
            self,
            exc_type: typing.Optional[typing.Type[Exception]] = None,
            exc_val: typing.Optional[Exception] = None,
            exc_tb: typing.Optional[TracebackType] = None,
    ) -> None: ...

    async def __anext__(self) -> _Document: ...

    def __enter__(self) -> typing.NoReturn: ...

    def __exit__(
            self,
            exc_type: typing.Optional[typing.Type[Exception]] = None,
            exc_val: typing.Optional[Exception] = None,
            exc_tb: typing.Optional[TracebackType] = None,
    ) -> None: ...

    def _lazy_init(self) -> None: ...

    def _try_next(self) -> typing.Optional[_Document]: ...

    async def _close(self) -> None: ...

    async def close(self) -> None: ...

    def get_io_loop(self) -> _IO_Loop: ...

    async def next(self) -> _Document: ...

    async def try_next(self) -> typing.Optional[_Document]: ...


class AgnosticClientEncryption(AgnosticBase):
    io_loop: _IO_Loop

    def __init__(
            self,
            kms_providers: typing.Mapping[str, typing.Any],
            key_vault_namespace: str,
            key_vault_client: AgnosticClient,
            codec_options: bson.codec_options.CodecOptions[typing.Any],
            kms_tls_options: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    ) -> None: ...

    async def __aenter__(self) -> Self: ...

    async def __aexit__(
            self,
            exc_type: typing.Optional[typing.Type[Exception]] = None,
            exc_val: typing.Optional[Exception] = None,
            exc_tb: typing.Optional[TracebackType] = None,
    ) -> None: ...

    def __enter__(self) -> typing.NoReturn: ...

    def __exit__(
            self,
            exc_type: typing.Optional[typing.Type[Exception]] = None,
            exc_val: typing.Optional[Exception] = None,
            exc_tb: typing.Optional[TracebackType] = None,
    ) -> None: ...

    async def add_key_alt_name(
            self, id: bson.binary.Binary, key_alt_name: str
    ) -> typing.Any: ...

    async def create_data_key(
            self,
            kms_provider: str,
            master_key: typing.Optional[typing.Mapping[str, typing.Any]] = None,
            key_alt_names: typing.Optional[typing.Sequence[str]] = None,
            key_material: typing.Optional[bytes] = None,
    ) -> bson.binary.Binary: ...

    async def close(self) -> None: ...

    async def delete_key(
            self, id: bson.binary.Binary
    ) -> pymongo.results.DeleteResult: ...

    async def decrypt(self, value: bson.binary.Binary) -> typing.Any: ...

    async def encrypt(
            self,
            value: typing.Any,
            algorithm: str,
            key_id: typing.Optional[bson.binary.Binary] = None,
            key_alt_name: typing.Optional[str] = None,
            query_type: typing.Optional[str] = None,
            contention_factor: typing.Optional[int] = None,
    ) -> bson.binary.Binary: ...

    async def get_key(
            self, id: bson.binary.Binary
    ) -> typing.Optional[bson.raw_bson.RawBSONDocument]: ...

    async def get_keys(self) -> AgnosticCursor: ...

    async def get_key_by_alt_name(
            self, key_alt_name: str
    ) -> typing.Optional[bson.raw_bson.RawBSONDocument]: ...

    async def remove_key_alt_name(
            self, id: bson.binary.Binary, key_alt_name: str
    ) -> typing.Optional[bson.raw_bson.RawBSONDocument]: ...

    async def rewrap_many_data_key(
            self,
            filter: typing.Mapping[str, typing.Any],
            provider: typing.Optional[str] = None,
            master_key: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    ) -> pymongo.encryption.RewrapManyDataKeyResult: ...

    def get_io_loop(self) -> _IO_Loop: ...
