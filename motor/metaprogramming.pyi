from types import ModuleType
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    Generator,
    Iterable,
    NoReturn,
    Optional,
    Tuple,
    Type,
    TypeVar,
)

from typing_extensions import ParamSpec, Self

_Func = TypeVar('_Func', bound=Callable)
_Args = ParamSpec('_Args')
_Ret = TypeVar('_Ret')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')

def asynchronize(
    framework: ModuleType,
    sync_method: Callable[_Args, _Ret],
    doc: str = None,
    wrap_class: Type = None,
    unwrap_class: str = None,
) -> Callable[_Args, Coroutine[Any, Any, _Ret]]: ...
def unwrap_args_session(args: Iterable[Any]) -> Generator[Any, Any, None]: ...
def unwrap_kwargs_session(kwargs: Dict[_KT, _VT]) -> Dict[_KT, _VT]: ...
def coroutine_annotation(f: _Func) -> _Func: ...

class MotorAttributeFactory(object):
    def __init__(self, doc: str = None): ...
    def create_attribute(self, cls: Type, attr_name: str) -> NoReturn: ...

class Async(MotorAttributeFactory):
    def __init__(self, attr_name: str, doc: str = None) -> None: ...
    def create_attribute(
        self, cls: Type, attr_name: str
    ) -> Coroutine[Any, Any, Any]: ...
    def wrap(self, original_class: Type) -> Self: ...
    def unwrap(self, class_name: str) -> Self: ...

class AsyncRead(Async):
    attr_name: str
    wrap_class: Optional[Type] = None
    unwrap_class: Optional[str] = None
    def __init__(self, attr_name: str = None, doc: str = None) -> None: ...

class AsyncWrite(Async):
    def __init__(self, attr_name: str = None, doc: str = None) -> None: ...

class AsyncCommand(Async):
    def __init__(self, attr_name: str = None, doc: str = None) -> None: ...

class ReadOnlyProperty(MotorAttributeFactory):
    def create_attribute(self, cls: Type, attr_name: str) -> property: ...

class DelegateMethod(ReadOnlyProperty):
    wrap_class: Optional[Type] = None
    def wrap(self, original_class: Type) -> Self: ...
    def create_attribute(
        self, cls: Type, attr_name: str
    ) -> Callable[[Any, Tuple[..., Any], Dict[str, Any]], Optional[Any]]: ...

class MotorCursorChainingMethod(MotorAttributeFactory):
    def create_attribute(
        self, cls: Type, attr_name: str
    ) -> Callable[[_Ret, Tuple[..., Any], Dict[str, Any]], _Ret]: ...

def create_class_with_framework(cls: Type, framework: ModuleType, module_name: str): ...
