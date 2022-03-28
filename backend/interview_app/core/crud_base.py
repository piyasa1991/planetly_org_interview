import typing
import pydantic
import sqlalchemy.orm
import interview_app.models as models
import fastapi.encoders
import fastapi

ModelType = typing.TypeVar("ModelType", bound=models.Base)
SchemaInType = typing.TypeVar("SchemaInType", bound=pydantic.BaseModel)


class CRUDBase:
    def __init__(self, model_cls: typing.Type[ModelType]):
        self.model_cls = model_cls

    def get_multi(self, db_session: sqlalchemy.orm.Session) -> typing.List[ModelType]:
        return db_session.query(self.model_cls).all()

    def get(self, db_session: sqlalchemy.orm.Session, id: int) -> ModelType:
        obj = db_session.query(self.model_cls).filter(self.model_cls.id == id).first()
        if not obj:
            raise fastapi.exceptions.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND, detail="Not found"
            )
        return obj

    def create(self, db_session: sqlalchemy.orm.Session, obj_in: SchemaInType) -> int:
        obj_data = obj_in.dict()
        db_obj = self.model_cls(**obj_data)
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def update(self, db_session: sqlalchemy.orm.Session, db_obj: ModelType, obj_in: SchemaInType) -> int:
        obj_data = obj_in.dict()

        for field in obj_data:
            if field in fastapi.encoders.jsonable_encoder(db_obj):
                setattr(db_obj, field, obj_data[field])

        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def delete(self, db_session: sqlalchemy.orm.Session, id: int) -> None:
        obj = self.get(db_session, id)
        db_session.delete(obj)
        db_session.commit()
