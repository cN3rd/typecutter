from dask.callbacks import Callback
from typing import Any

class TqdmCallback(Callback):
    tqdm_class: Any
    def __init__(self, start: Any | None = ..., pretask: Any | None = ..., tqdm_class=..., **tqdm_kwargs) -> None: ...
    def display(self) -> None: ...
