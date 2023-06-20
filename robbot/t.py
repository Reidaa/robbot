from attrs import frozen, field


@frozen
class S_Manga:
    title: str = field(eq=str.lower)
    last_chapter: int


@frozen
class S_MangaChapter:
    title: str
    number: int
    link: str | None = field(default=None)


@frozen
class S_Channel:
    channel_id: int
    mangas: list[S_Manga] = field(factory=list)
