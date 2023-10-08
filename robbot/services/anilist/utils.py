from robbot.services.anilist.AsyncClient import send_query


async def get_synonyms(title: str) -> list[str]:
    query = """
    query ($title: String) {
        Media(search: $title, type: MANGA) {
            title {
                romaji
                english
                native
            }
            synonyms
        }
    }
    """

    variables = {
        "title": title
    }

    response = await send_query(query, variables)

    return response["Media"]["synonyms"]


async def get_titles(title: str) -> list[str]:
    query = """
    query ($title: String) {
        Media(search: $title, type: MANGA) {
            title {
                romaji
                english
                native
            }
            synonyms
        }
    }
    """

    variables = {
        "title": title
    }

    response = await send_query(query, variables)

    titles = []
    if response["Media"]["title"]["english"]:
        titles.append(response["Media"]["title"]["english"])

    return titles


async def get_manga_info(title: str) -> dict[str, any]:
    query = """
    query ($title: String) {
      Media(search: $title, type: MANGA) {
        title {
          romaji
          english
          native
        }
        description
        startDate {
          year
        }
        coverImage {
          extraLarge
          large
          medium
        }
        status
      }
    }
    """

    variables = {
        "title": title
    }

    response = await send_query(query, variables)
    return response["Media"]