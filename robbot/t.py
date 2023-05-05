from attrs import frozen, field


@frozen
class Manga:
    title: str = field(eq=str.lower)
    last_chapter: int


@frozen
class MangaChapter:
    title: str
    number: int
    link: str | None = field(default=None)


@frozen
class Channel:
    channel_id: int
    mangas: list[Manga] = field(factory=list)
