import typing
import sqlalchemy.orm
import interview_app.models as models
import interview_app.schemas as schemas
import interview_app.core.crud_base as crud_base
import pydantic
import datetime

city = crud_base.CRUDBase(models.City)


class TemperatureCRUD(crud_base.CRUDBase):
    def create_by_city(
        self, db_session: sqlalchemy.orm.Session, obj_in: schemas.Temperature, city_id: int
    ) -> models.Temperature:
        db_obj = models.Temperature(**obj_in.dict(), city_id=city_id)
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def get_by_city(
        self, db_session: sqlalchemy.orm.Session, city_id: int, dt: datetime
    ) -> models.Temperature:
        return (
            db_session.query(models.Temperature)
            .filter(models.Temperature.city_id == city_id, models.Temperature.dt == dt)
            .first()
        )

    def get_top_n_cities_with_highest_temperature(
        self,
        db_session: sqlalchemy.orm.Session,
        date_start: datetime = None,
        date_end: datetime = None,
        top_n: int = 1,
    ) -> typing.List[models.Temperature]:

        subquery = (
            db_session.query(sqlalchemy.func.max(models.Temperature.average_temperature))
            .filter(models.Temperature.dt > date_start)
            .group_by(models.Temperature.city_id)
        )

        if date_end is not None:
            subquery = (
                db_session.query(sqlalchemy.func.max(models.Temperature.average_temperature))
                .filter(models.Temperature.dt.between(date_start, date_end))
                .group_by(models.Temperature.city_id)
            )

        query = (
            db_session.query(models.Temperature)
            .filter(models.Temperature.average_temperature.in_(subquery))
            .order_by(models.Temperature.average_temperature.desc())
            .limit(top_n)
        )

        return query.all()


temperature = TemperatureCRUD(models.Temperature)


# __all__ = ["user", "phone", "email"]
