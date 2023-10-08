from attrs import define, field, Factory, frozen


### Generic models

@frozen
class ListResult:
    page: int
    perPage: int
    totalPages: int
    totalItems: int
    items: list[dict[str, str]]


@frozen
class ErrorResponse:
    code: int
    message: str
    data: dict[str, any]


@define
class RecordResponse:
    # Base fields
    id: str
    created: str
    updated: str
    collectionId: str
    collectionName: str

    # Collection and/or Query related fields
    expand: dict[str, any] = Factory(dict)
    fields: dict[str, any] = field(init=False)

    def __init__(self, id: str, collectionId: str, collectionName: str, created: str, updated: str,
                 expand: dict[str, any] | None = None, **kwargs):
        self.__attrs_init__(id, collectionId, collectionName, created, updated)
        self.expand = expand
        self.fields = kwargs


### Specialised models

@frozen
class Manga:
    id: str
    name: str = field(eq=str.lower)
    last_chapter: int
    cover_url: str | None = field(default=None)
    channel_record_ids: list[str] = field(factory=list)


@frozen
class Channel:
    id: str
    channel_id: int
    manga_record_ids: list[str] = field(factory=list)


### Errors

class PocketbaseError(Exception):
    def __init__(self, code: int, message: str, data: dict[str, any] | None = None):
        self.response = ErrorResponse(code, message, data)

    def __str__(self):
        return f"Pocketbase: {self.response.message}"


class BackendError(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"Pocketbase: {self.message}"