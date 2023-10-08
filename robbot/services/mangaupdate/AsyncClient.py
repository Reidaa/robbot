import httpx

from services.mangaupdate.models import SearchResult, MangaupdateError, SeriesRecord

username = "Reidaas"
password = "QkRy5N#Jfwce!G"


class MangaUpdatesAuth(httpx.Auth):

    def __init__(self, base_url: str, username: str, password: str):
        super().__init__()
        self.requires_response_body = True
        self._base_url = base_url
        self.__username = username
        self.__password = password
        self.__token: str | None = None

    def _get_session_token(self):
        response = httpx.put(
            f"{self._base_url}/account/login",
            json={"username": self.__username, "password": self.__password}
        )
        response_dict = response.json()

        match response.status_code:
            case 400:
                raise MangaupdateError(**response_dict)
            case 200:
                self.__token = response_dict["context"]["session_token"]
            case _:
                raise Exception("Unknown error")

    def auth_flow(self, request):
        request.headers["Authorization"] = f"Bearer {self.__token}"
        response = yield request

        if response.status_code == 401:
            # If the server issues a 401 response, then issue a request to refresh tokens, and resend the request.
            self._get_session_token()
            request.headers["Authorization"] = f"Bearer {self.__token}"
            yield request


class AsyncMangaUpdateClient:

    def __init__(self):
        self._base_url = "https://api.mangaupdates.com/v1"
        self.auth = MangaUpdatesAuth(self._base_url, username, password)

    async def search_series(self, title: str, body_params: dict | None = None) -> SearchResult:
        if body_params is None:
            body_params = {}

        async with httpx.AsyncClient(base_url=self._base_url) as client:
            response = await client.post(
                "/series/search", json={"search": title, **body_params}, auth=self.auth)

        response_dict = response.json()

        match response.status_code:
            case 400:
                raise MangaupdateError(**response_dict)
            case 200:
                return SearchResult(**response_dict)

    async def get_series(self, series_id: str) -> SeriesRecord:
        async with httpx.AsyncClient(base_url=self._base_url) as client:
            response = await client.get(f"/series/{series_id}", auth=self.auth)

        response_dict = response.json()

        match response.status_code:
            case 400:
                raise MangaupdateError(**response_dict)
            case 200:
                return SeriesRecord(**response_dict)


client = AsyncMangaUpdateClient()
