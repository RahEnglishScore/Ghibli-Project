from typing import List, Optional, Dict, Any

from pydantic import BaseModel, HttpUrl, model_validator

from .utils import validate_http_url_fields


class Actor(BaseModel):
    id: str
    name: str
    species: Optional[HttpUrl]
    url: HttpUrl

    @model_validator(mode="before")
    def validate(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return validate_http_url_fields(values)


class Film(BaseModel):
    id: str
    title: str
    original_title: str
    original_title_romanised: str
    image: HttpUrl
    movie_banner: HttpUrl
    description: str
    director: str
    producer: str
    release_date: str
    running_time: str
    rt_score: Optional[str]
    actors: Optional[List[Actor]] = None
    people: Optional[List[HttpUrl]]
    species: Optional[List[HttpUrl]]
    locations: Optional[List[HttpUrl]]
    vehicles: Optional[List[HttpUrl]]
    url: HttpUrl

    @model_validator(mode="before")
    def validate(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        return validate_http_url_fields(values)
