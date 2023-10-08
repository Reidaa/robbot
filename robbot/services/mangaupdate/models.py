from attrs import define

### Data models for MangaUpdate service

@define
class SearchResult:
    total_hits: int
    page: int
    per_page: int
    results: list[dict[str, any]]

@define
class SeriesRecord:
    anime: dict[str, str]
    associated: list[dict[str, any]]
    authors: list[dict[str, any]]
    bayesian_rating: int
    categories: list[dict[str, any]]
    category_recommendations: list[dict[str, any]]
    completed: bool
    description: str
    forum_id: int
    genres: list[dict[str, any]]
    image: dict[str, any]
    last_updated: dict[str, any]
    latest_chapter: int
    licensed: bool
    publications: list[dict[str, any]]
    publishers: list[dict[str, any]]
    rank: dict[str, any]
    rating_votes: int
    recommendations: list[dict[str, any]]
    related_series: list[dict[str, str | int]]
    series_id: int
    status: str
    title: str
    type: str
    url: str
    year: str

### Custom exceptions for MangaUpdate service

class MangaupdateError(Exception):
    def __init__(self, status: str, reason: str, context: dict[str, any] | None = None):
        self.status = status
        self.reason = reason
        self.context = context