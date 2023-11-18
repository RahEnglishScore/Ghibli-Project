import asyncio
from datetime import datetime

from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from .data_processing import combine_film_and_actors
from .ghibli_api import fetch_films
from .authentication import GhibliApiKeyAuthentication


class MovieList(APIView):
    """
    API endpoint that returns a list of movies.

    If the data is cached, it will return the cached data.
    If the data is not cached, it will fetch the data from the Ghibli API,
    """

    authentication_classes = [GhibliApiKeyAuthentication]

    def get(self, request):
        cached_data = cache.get("processed_movies_data")
        if cached_data:
            return Response(cached_data["data"])

        films = fetch_films()
        combined_data = asyncio.run(combine_film_and_actors(films))
        processed_data = {"data": combined_data, "timestamp": datetime.now()}

        # Cache the processed data
        cache.set("processed_movies_data", processed_data)

        return Response(combined_data)
