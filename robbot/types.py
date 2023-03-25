from typing import Optional
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Manga:
    title: str
    last_chapter: int
    roles_to_notify: list[int] = field(default_factory=list)
    users_to_notify: list[int] = field(default_factory=list)


@dataclass(frozen=True)
class SearchMangaResult:
    title: str
    chapter: int
    link: Optional[str] = None
