from attrs import define, field, Factory


@define
class ListResult:
    page: int
    perPage: int
    totalPages: int
    totalItems: int
    items: list[dict[str, str]]


@define
class Error:
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
                 expand: dict[str, any] = None, **kwargs):
        self.__attrs_init__(id, collectionId, collectionName, created, updated)
        self.expand = expand
        self.fields = kwargs
