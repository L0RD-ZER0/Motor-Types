import typing

import bson
import bson.codec_options
import bson.timestamp
import gridfs
import gridfs.grid_file
import pymongo.client_session
import pymongo.collation
import pymongo.collection
import pymongo.command_cursor
import pymongo.cursor
import pymongo.read_concern
import pymongo.read_preferences
import pymongo.write_concern

from . import core, motor_gridfs

_Collation = typing.Union[typing.Mapping[str, typing.Any], pymongo.collation.Collation]
_Document = typing.Dict[str, typing.Any]
_Pipeline = typing.Sequence[typing.Mapping[str, typing.Any]]
_Session = typing.Union[pymongo.client_session.ClientSession, AsyncIOMotorClientSession]
_ReadPreferences = typing.Union[
    pymongo.read_preferences.Primary,
    pymongo.read_preferences.PrimaryPreferred,
    pymongo.read_preferences.Secondary,
    pymongo.read_preferences.SecondaryPreferred,
    pymongo.read_preferences.Nearest,
]

def create_asyncio_class(cls: typing.Type) -> typing.Type: ...

class AsyncIOMotorClient(core.AgnosticClient):
    def __getitem__(self, item: str) -> AsyncIOMotorDatabase: ...
    def __getattr__(self, item: str) -> AsyncIOMotorDatabase: ...
    def get_database(
        self,
        name: typing.Optional[str] = None,
        codec_options: typing.Optional[
            bson.codec_options.CodecOptions[typing.Any]
        ] = None,
        read_preference: typing.Optional[_ReadPreferences] = None,
        write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
        read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
    ) -> AsyncIOMotorDatabase: ...
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
    ) -> AsyncIOMotorDatabase: ...
    async def list_databases(
        self,
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> AsyncIOMotorCommandCursor: ...
    async def start_session(
        self,
        causal_consistency: typing.Optional[bool] = None,
        default_transaction_options: typing.Optional[
            pymongo.client_session.TransactionOptions
        ] = None,
    ) -> AsyncIOMotorClientSession: ...
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
    ) -> AsyncIOMotorChangeStream: ...

class AsyncIOMotorClientSession(core.AgnosticClientSession):
    client: AsyncIOMotorClient

class AsyncIOMotorDatabase(core.AgnosticDatabase):
    client: AsyncIOMotorClient
    def __getitem__(self, item: str) -> AsyncIOMotorCollection: ...
    def __getattr__(self, item: str) -> AsyncIOMotorCollection: ...
    def __init__(self, client: AsyncIOMotorClient, name: str, **kwargs: typing.Any): ...
    def aggregate(
        self, pipeline: _Pipeline, *args: typing.Any, **kwargs: typing.Any
    ) -> AsyncIOMotorLatentCommandCursor: ...
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
    ) -> AsyncIOMotorCollection: ...
    def get_collection(
        self,
        name: str,
        codec_options: typing.Optional[
            bson.codec_options.CodecOptions[typing.Any]
        ] = None,
        read_preference: typing.Optional[_ReadPreferences] = None,
        write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
        read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
    ) -> AsyncIOMotorCollection: ...
    async def list_collections(
        self,
        session: typing.Optional[_Session] = None,
        filter: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        comment: typing.Optional[typing.Any] = None,
        **kwargs: typing.Any,
    ) -> AsyncIOMotorCommandCursor: ...
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
    ) -> AsyncIOMotorChangeStream: ...

class AsyncIOMotorCollection(core.AgnosticCollection):
    def __init__(
        self,
        database: AsyncIOMotorDatabase,
        name: str,
        codec_options: typing.Optional[
            bson.codec_options.CodecOptions[typing.Any]
        ] = None,
        read_preference: typing.Optional[_ReadPreferences] = None,
        write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
        read_concern: typing.Optional[pymongo.read_concern.ReadConcern] = None,
        _delegate: typing.Optional[pymongo.collection.Collection[typing.Any]] = None,
    ): ...
    def aggregate(
        self,
        pipeline: _Pipeline,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> AsyncIOMotorLatentCommandCursor: ...
    def aggregate_raw_batches(
        self,
        pipeline: _Pipeline,
        **kwargs: typing.Any,
    ) -> AsyncIOMotorLatentCommandCursor: ...
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
    ) -> AsyncIOMotorCursor: ...
    def list_indexes(
        self,
        session: typing.Optional[_Session] = None,
        comment: typing.Optional[typing.Any] = None,
    ) -> AsyncIOMotorLatentCommandCursor: ...
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
    ) -> AsyncIOMotorChangeStream: ...

class AsyncIOMotorCursor(core.AgnosticCursor):
    session: AsyncIOMotorClientSession
    def __init__(
        self,
        cursor: pymongo.cursor.Cursor[_Document],
        collection: AsyncIOMotorCollection,
    ) -> None: ...

    async def __aenter__(self) -> "AsyncIOMotorCursor": ...

class AsyncIOMotorCommandCursor(core.AgnosticCommandCursor):
    session: AsyncIOMotorClientSession
    def __init__(
        self,
        cursor: pymongo.cursor.Cursor[_Document],
        collection: AsyncIOMotorCollection,
    ) -> None: ...

    async def __aenter__(self) -> "AsyncIOMotorCommandCursor": ...

class AsyncIOMotorLatentCommandCursor(core.AgnosticLatentCommandCursor):
    session: AsyncIOMotorClientSession

    def __init__(
        self,
        collection: AsyncIOMotorCollection,
        start: typing.Optional[
            typing.Callable[
                [typing.Any], pymongo.command_cursor.CommandCursor[_Document]
            ]
        ] = None,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> None: ...

    async def __aenter__(self) -> "AsyncIOMotorLatentCommandCursor": ...

class AsyncIOMotorChangeStream(core.AgnosticChangeStream):
    def __init__(
        self,
        target: typing.Union[
            AsyncIOMotorClient,
            AsyncIOMotorDatabase,
            AsyncIOMotorCollection,
        ],
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

class AsyncIOMotorGridFSBucket(motor_gridfs.AgnosticGridFSBucket):
    collection: AsyncIOMotorCollection
    def __init__(
        self,
        database: AsyncIOMotorDatabase,
        bucket_name: str = 'fs',
        chunk_size_bytes: int = gridfs.DEFAULT_CHUNK_SIZE,
        write_concern: typing.Optional[pymongo.write_concern.WriteConcern] = None,
        read_preference: typing.Optional[_ReadPreferences] = None,
        collection: typing.Optional[AsyncIOMotorCollection] = None,
    ) -> None: ...
    def find(
        self,
        filter: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        skip: int = 0,
        limit: int = 0,
        no_cursor_timeout: bool = False,
        sort: typing.Optional[typing.Any] = None,
        batch_size: int = 0,
        session: typing.Optional[_Session] = None,
    ) -> AsyncIOMotorGridOutCursor: ...
    async def open_download_stream(
        self, file_id: typing.Any, session: typing.Optional[_Session] = None
    ) -> AsyncIOMotorGridOut: ...
    async def open_download_stream_by_name(
        self,
        filename: str,
        revision: int = -1,
        session: typing.Optional[_Session] = None,
    ) -> AsyncIOMotorGridOut: ...
    def open_upload_stream(
        self, file_id: typing.Any, session: typing.Optional[_Session] = None
    ) -> AsyncIOMotorGridIn: ...
    def open_upload_stream_with_id(
        self,
        file_id: typing.Any,
        filename: str,
        chunk_size_bytes: typing.Optional[int] = None,
        metadata: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        session: typing.Optional[_Session] = None,
    ) -> AsyncIOMotorGridIn: ...

class AsyncIOMotorGridIn(motor_gridfs.AgnosticGridIn):
    def __init__(
        self,
        root_collection: AsyncIOMotorCollection,
        delegate: gridfs.grid_file.GridIn,
        session: pymongo.client_session.ClientSession,
        **kwargs: typing.Any,
    ) -> None: ...

class AsyncIOMotorGridOut(motor_gridfs.AgnosticGridOut):
    def __init__(
        self,
        root_collection: AsyncIOMotorCollection,
        file_id: typing.Optional[int] = None,
        file_document: typing.Optional[typing.Any] = None,
        delegate: typing.Optional[gridfs.grid_file.GridOut] = None,
        session: typing.Optional[pymongo.client_session.ClientSession] = None,
        **kwargs: typing.Any,
    ) -> None: ...

class AsyncIOMotorGridOutCursor(motor_gridfs.AgnosticGridOutCursor):
    def next_object(self) -> typing.Optional[AsyncIOMotorGridOut]: ...

    async def __aenter__(self) -> "AsyncIOMotorGridOutCursor": ...

class AsyncIOMotorClientEncryption(core.AgnosticClientEncryption):
    def __init__(
        self,
        kms_providers: typing.Mapping[str, typing.Any],
        key_vault_namespace: str,
        key_vault_client: AsyncIOMotorClient,
        codec_options: bson.codec_options.CodecOptions[typing.Any],
        kms_tls_options: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    ) -> None: ...
    async def get_keys(self) -> AsyncIOMotorCursor: ...
