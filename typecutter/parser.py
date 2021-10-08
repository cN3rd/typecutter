import re
import warnings
from typing import List, Match, Optional, Pattern

from .common import Cut

cuts_prefix: str = ":"
cuts_regex_pattern: str = (
    rf"^{cuts_prefix}"
    rf"(?P<startframe>\d+),[\s]?(?P<endframe>\d+)"
    rf"[\s]?(?P<name>[\w]*)?"
    rf"[\s]?(?P<pre_comment>[^#]+)?"
    rf"[\s]?(\#.*)?$"
)
cuts_regex: Pattern[str] = re.compile(cuts_regex_pattern)


def validate_match(m: re.Match[str]) -> re.Match[str]:
    if m.group("pre_comment"):
        warnings.warn(
            f"Cut name should contain no spaces. \"{m.group('name')}\" would be used as the cut name."
        )
    return m


def validate_cut(c: Cut) -> Cut:
    if c.start > c.end:
        raise ValueError(
            f'Start frame "{c.start}" must be smaller-equals to end frame "{c.end}".'
        )

    if c.name is not None and not c.name.isascii():
        raise ValueError(f'Cut name "{c.name}" must be in ASCII.')
    return c


def parse_cut(m: re.Match[str]) -> Cut:
    return Cut(
        start=int(m.group("startframe")),
        end=int(m.group("endframe")),
        name=m.group("name").strip() if m.group("name") else None,
    )


def parse_typecuts(input_data: str) -> List[Cut]:
    cuts: list[Cut] = []
    for line in str.splitlines(input_data):
        match: Optional[Match[str]] = cuts_regex.match(line)
        if match is None:
            continue

        validate_match(match)
        cut: Cut = parse_cut(match)
        validate_cut(cut)

        cuts.append(cut)
    return cuts
