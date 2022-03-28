import fastapi
import interview_app.core.deps as deps
import sqlalchemy.orm
import interview_app.schemas as schemas
import interview_app.crud as crud
import typing
from datetime import datetime

router = fastapi.APIRouter()


@router.get(
    "", responses={404: {"description": "Not found"}}, response_model=typing.List[schemas.CityMetadata]
)
def get_cities(db_session: sqlalchemy.orm.Session = fastapi.Depends(deps.get_db)) -> typing.Any:
    return crud.city.get_multi(db_session)


@router.get("/top/{n}", response_model=typing.List[schemas.TopNCity])
def get_top_n_cities(
    n: int,
    date_start: datetime,
    date_end: typing.Optional[datetime] = None,
    db_session: sqlalchemy.orm.Session = fastapi.Depends(deps.get_db),
):

    list_of_top_n_cities = crud.temperature.get_top_n_cities_with_highest_temperature(
        db_session, date_start, date_end, n
    )
    return [schemas.TopNCity.parse_obj(obj) for obj in list_of_top_n_cities]


@router.get("/{id}", responses={404: {"description": "Not found"}}, response_model=schemas.City)
def get_city(id: int, db_session: sqlalchemy.orm.Session = fastapi.Depends(deps.get_db)) -> typing.Any:
    return crud.city.get(db_session, id=id)


@router.post(
    "/{id}/temperature",
    responses={201: {"description": "Resource Created"}},
    status_code=fastapi.status.HTTP_201_CREATED,
    response_model=schemas.Temperature,
)
def create_temperature(
    id: int,
    temperature_in: schemas.TemperatureIn,
    db_session: sqlalchemy.orm.Session = fastapi.Depends(deps.get_db),
) -> typing.Any:
    obj = crud.temperature.create_by_city(db_session, obj_in=temperature_in, city_id=id)
    return obj


@router.put(
    "/{id}/temperature",
    responses={
        404: {"description": "Not found"},
    },
    response_model=schemas.Temperature,
)
def update_temperature(
    id: int,
    temperature_in: schemas.TemperatureIn,
    db_session: sqlalchemy.orm.Session = fastapi.Depends(deps.get_db),
) -> typing.Any:
    temperature_db_obj = crud.temperature.get_by_city(db_session, city_id=id, dt=temperature_in.dt)
    obj = crud.temperature.update(db_session, db_obj=temperature_db_obj, obj_in=temperature_in)
    return obj
