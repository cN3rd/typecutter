from .asyncio import tqdm as asyncio_tqdm
from .autonotebook import tqdm as notebook_tqdm

class tqdm(notebook_tqdm, asyncio_tqdm): ...
tqdm = asyncio_tqdm

def trange(*args, **kwargs): ...
