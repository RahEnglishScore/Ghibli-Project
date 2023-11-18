import asyncio
from unittest.mock import MagicMock, patch

import httpx
import pytest
from django.core.cache import cache
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APIClient

from api.data_processing import combine_film_and_actors
from api.ghibli_api import fetch_actor_details, fetch_films
from api.models import Actor, Film


def test_fetch_films():
    with patch("api.ghibli_api.httpx.Client") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "id": "1",
                "title": "Film 1",
                "original_title": "Original Title",
                "original_title_romanised": "Original Title Romanised",
                "image": "http://example.com/image.jpg",
                "movie_banner": "http://example.com/banner.jpg",
                "description": "Description",
                "director": "Director",
                "producer": "Producer",
                "release_date": "2023",
                "running_time": "120",
                "rt_score": "90",
                "people": [],
                "species": [],
                "locations": [],
                "vehicles": [],
                "url": "http://example.com/film",
            }
        ]
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response

        films = fetch_films()
        assert len(films) == 1
        assert films[0].id == "1"


@pytest.mark.asyncio
async def test_fetch_actor_details():
    with patch("api.ghibli_api.httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                "id": "1",
                "name": "Actor 1",
                "species": "http://example.com/species",
                "url": "http://example.com/actor",
            }
        ]
        mock_client.return_value.__aenter__.return_value.get.return_value = (
            mock_response
        )

        actors = await fetch_actor_details("http://example.com")
        assert len(actors) == 1
        assert actors[0].id == "1"


@pytest.mark.asyncio
async def test_combine_film_and_actors():
    films = [
        Film.model_validate(
            {
                "id": "1",
                "title": "Film 1",
                "original_title": "Original Title",
                "original_title_romanised": "Original Title Romanised",
                "image": "http://example.com/image.jpg",
                "movie_banner": "http://example.com/banner.jpg",
                "description": "Description",
                "director": "Director",
                "producer": "Producer",
                "release_date": "2023",
                "running_time": "120",
                "rt_score": "90",
                "people": ["http://example.com/actor"],
                "species": [],
                "locations": [],
                "vehicles": [],
                "url": "http://example.com/film",
            }
        )
    ]

    actor = [
        Actor.model_validate(
            {
                "id": "1",
                "name": "Actor 1",
                "species": "http://example.com/species",
                "url": "http://example.com/actor",
            }
        )
    ]

    with patch("api.data_processing.fetch_actor_details", return_value=actor):
        combined_films = await combine_film_and_actors(films)
        assert len(combined_films) == 1
        assert combined_films[0]["actors"][0]["id"] == "1"


@pytest.mark.django_db
def test_auth():
    client = APIClient()
    url = reverse("movie-list")
    response = client.get(url, HTTP_GHIBLIKEY="Random")
    assert response.status_code == 403


@pytest.mark.django_db
def test_movie_list_endpoint():
    client = APIClient()
    url = reverse("movie-list")

    with patch("api.views.fetch_films") as mock_fetch_films, patch(
        "api.views.combine_film_and_actors"
    ) as mock_combine:
        mock_fetch_films.return_value = []
        mock_combine.return_value = []

        response = client.get(url, HTTP_GHIBLIKEY=settings.GHIBLI_API_KEY)

        assert response.status_code == 200
        mock_fetch_films.assert_called_once()
        mock_combine.assert_called_once()


def test_caching_in_fetch_actor_details():
    url = "http://example.com"
    actor_data = [
        {
            "id": "1",
            "name": "Actor 1",
            "species": "http://example.com/species",
            "url": "http://example.com/actor",
        }
    ]
    cache.set(url, actor_data)

    actors = asyncio.run(fetch_actor_details(url))
    assert len(actors) == 1
    assert actors[0].id == "1"


def test_fetch_films_api_error():
    with patch("api.ghibli_api.httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.side_effect = (
            httpx.HTTPError("API down")
        )

        with pytest.raises(httpx.HTTPError):
            fetch_films()
