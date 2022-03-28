import pydantic
import typing
from datetime import datetime
import fastapi.encoders
import interview_app.models as models


class TemperatureIn(pydantic.BaseModel):
    dt: datetime
    average_temperature: typing.Optional[float]
    average_temperature_uncertainty: typing.Optional[float]


class Temperature(TemperatureIn):
    id: int

    class Config:
        orm_mode = True


class CityIn(pydantic.BaseModel):
    city: str
    country: str
    latitude: str
    longitude: str


class CityMetadata(CityIn):
    id: int

    class Config:
        orm_mode = True


class City(CityMetadata):
    temperatures: typing.List[Temperature]

    class Config:
        orm_mode = True


class TopNCity(CityIn):
    id: int
    temperature: Temperature

    @classmethod
    def parse_obj(cls, obj: models.Temperature):
        return cls(
            id=obj.city.id,
            city=obj.city.city,
            country=obj.city.country,
            latitude=obj.city.latitude,
            longitude=obj.city.longitude,
            temperature=Temperature(**fastapi.encoders.jsonable_encoder(obj)),
        )
