from attrs import frozen, field


@frozen
class MangaChapter:
    manga_title: str
    number: int
    title: str | None = field(default=None)
    link: str | None = field(default=None)
