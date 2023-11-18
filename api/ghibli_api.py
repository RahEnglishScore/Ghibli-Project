from typing import List

import httpx
from django.core.cache import cache

from pydantic import HttpUrl
from api.models import Actor, Film

FILMS_URL = "https://ghibli.rest/films"


def fetch_films() -> List[Film]:
    """
    Fetches the films from the Ghibli API and returns a list of Film objects.

    Returns:
        List[Film]: A list of Film objects
    """
    with httpx.Client() as client:
        response = client.get(FILMS_URL)
        response.raise_for_status()
        return [Film.model_validate(film) for film in response.json()]


async def fetch_actor_details(actor_url: HttpUrl) -> List[Actor]:
    """
    Fetches the actor details from the Ghibli API and returns a list of Actor objects.

    Args:
        actor_url (HttpUrl): The URL of the actor details.

    Returns:
        List[Actor]: A list of Actor objects.
    """

    url_str = str(actor_url)  # Convert Pydantic HttpUrl to string

    # Check if the actor details are in the cache
    cached_data = cache.get(url_str)
    if cached_data:
        return [Actor.model_validate(actor) for actor in cached_data]

    # If not in cache, fetch the data
    async with httpx.AsyncClient() as client:
        response = await client.get(url_str)
        response.raise_for_status()
        actor_data = response.json()

        # Cache the data
        # This is useful for when the same actor appears in multiple films
        cache.set(url_str, actor_data)

        if isinstance(actor_data, list):
            return [Actor.model_validate(actor) for actor in actor_data]
        else:
            return [Actor.model_validate(actor_data)]
