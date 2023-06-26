from attrs import define


@define
class SearchResult:
    total_hits: int
    page: int
    per_page: int
    results: list[dict[str, any]]

@define
class Error:
    status: str
    reason: str
    context: dict[str, any] | None