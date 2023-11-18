import asyncio
from typing import List

from pydantic import HttpUrl

from api.models import Actor, Film
from .ghibli_api import fetch_actor_details


async def combine_film_and_actors(films: List[Film]) -> List[Film]:
    """
    Combines the film and actor details into a single list of Film objects.

    Args:
        films (List[Film]): A list of Film objects.

    Returns:
        List[Film]: A list of Film objects with the actors added (and people removed).
    """

    async def get_actors_for_film(actor_urls: List[HttpUrl]) -> List[Actor]:
        tasks = [fetch_actor_details(str(url)) for url in actor_urls if url]
        actors_lists = await asyncio.gather(*tasks)
        # Flatten list of lists to a single list of actors
        return [actor for sublist in actors_lists for actor in sublist]

    for film in films:
        actor_urls = film.people
        actors = await get_actors_for_film(actor_urls)
        film.actors = actors

    return [film.model_dump(mode="json", exclude={"people"}) for film in films]
