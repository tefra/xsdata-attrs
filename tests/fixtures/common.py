from datetime import datetime
from typing import List

import attr


@attr.s(auto_attribs=True)
class TypeA:
    one: str
    two: float


@attr.s(auto_attribs=True)
class TypeB(TypeA):
    one: str
    three: bool = attr.ib(default=True)


@attr.s(auto_attribs=True)
class TypeC(TypeB):
    four: List[datetime] = attr.ib(factory=list, metadata={"format": "%d %B %Y %H:%M"})
    any: object = attr.ib(default=None, metadata={"type": "Wildcard"})
