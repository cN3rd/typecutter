from typing import NamedTuple, Optional


# typehint for cuts
class Cut(NamedTuple):
    start: int
    end: int
    name: Optional[str]

    def __str__(self) -> str:
        name_str = ', "' + self.name if self.name else '"'
        return "(" + str(self.start) + ", " + str(self.end) + name_str + ")"
