from .std import tqdm as std_tqdm
from typing import Any

class tqdm_gui(std_tqdm):
    mpl: Any
    plt: Any
    toolbar: Any
    mininterval: Any
    xdata: Any
    ydata: Any
    zdata: Any
    hspan: Any
    wasion: Any
    ax: Any
    def __init__(self, *args, **kwargs) -> None: ...
    disable: bool
    def close(self) -> None: ...
    def clear(self, *_, **__) -> None: ...
    def display(self, *_, **__) -> None: ...

def tgrange(*args, **kwargs): ...
tqdm = tqdm_gui
trange = tgrange
