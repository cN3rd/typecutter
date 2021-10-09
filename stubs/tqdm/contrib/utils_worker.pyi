from typing import Any

class MonoWorker:
    pool: Any
    futures: Any
    def __init__(self) -> None: ...
    def submit(self, func, *args, **kwargs): ...
