MockDB: list[Manga] = {
    "Chainsaw Man": Manga(
        title="Chainsaw Man",
        last_chapter=123-1,
        roles_to_notify=[1087136295807099032, ],
    ),
    "My hero academia": Manga(
        title="My hero academia",
        last_chapter=382-1,
        roles_to_notify=[1087136295807099032, ],
        users_to_notify=[209770215163035658, ],
    ),
    "blue box": Manga(
        title="blue box",
        last_chapter=92,
        roles_to_notify=[],
        users_to_notify=[],
    ),
    "akane banashi": Manga(
        title="akane banashi",
        last_chapter=53,
        roles_to_notify=[],
        users_to_notify=[],
    ),
}


class DB:
    def __init__(self):
        self.series: list[Manga] = None

        self.series = MockDB

    def update_chapter(self, title: str, chapter: int) -> bool:
        """
        Update the last chapter of a manga.
        Return True if the manga was found and updated, False otherwise.
        """
        for manga in self.series:
            if manga.title == title:
                manga.last_chapter = chapter
                return True
        return False

    def get_manga(self, title: str) -> Manga:
        for manga in self.series:
            if manga.title == title:
                return manga
        raise ValueError(f"manga {title} not found")

    def get_mangas(self) -> list[Manga]:
        return self.series

    def cleanup(self):
        pass


class DBContext:
    def __enter__(self):
        self.db_obj = DB()
        return self.db_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db_obj.cleanup()


# def update_chapter(title: str, chapter: int) -> bool:
#     """ 
#     Update the last chapter of a manga. 
#     Return True if the manga was found and updated, False otherwise.
#     """
#     for manga in SERIES:
#         if manga.title == title:
#             manga.last_chapter = chapter
#             return True
#     return False


# def get_manga(title: str) -> Manga:
#     for manga in SERIES:
#         if manga.title == title:
#             return manga
#     raise ValueError(f"manga {title} not found")


# def get_mangas() -> list[Manga]:
#     return SERIES

