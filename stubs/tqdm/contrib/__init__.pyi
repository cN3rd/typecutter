from ..utils import ObjectWrapper
from typing import Any

class DummyTqdmFile(ObjectWrapper):
    def __init__(self, wrapped) -> None: ...
    def write(self, x, nolock: bool = ...) -> None: ...
    def __del__(self) -> None: ...

def tenumerate(iterable, start: int = ..., total: Any | None = ..., tqdm_class=..., **tqdm_kwargs): ...
def tzip(iter1, *iter2plus, **tqdm_kwargs) -> None: ...
def tmap(function, *sequences, **tqdm_kwargs) -> None: ...
