from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Manga:
    title: str
    last_chapter: int


@dataclass(frozen=True)
class MangaChapter:
    title: str
    number: int
    link: Optional[str] = field(default=None)


@dataclass(frozen=True)
class SearchMangaResult:
    title: str
    chapter: int
    link: Optional[str] = field(default=None)
