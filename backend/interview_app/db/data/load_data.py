import pandas as pd
import interview_app.db.session as db
import interview_app.core.config as settings
import interview_app.models as models
import sqlalchemy.orm
import psycopg2
import logging

logger = logging.getLogger(__name__)


def load_data(db_session: sqlalchemy.orm.Session) -> None:
    file_path = "interview_app/db/data/GlobalLandTemperaturesByCity.csv"

    cols = models.Temperature.__table__.columns.keys()[1:] + models.City.__table__.columns.keys()[1:]
    cols.remove("city_id")

    df = pd.read_csv(file_path, parse_dates=["dt"], header=0, names=cols)

    # use foreign key to normalize the table
    df_city = pd.DataFrame(df.groupby(models.City.__table__.columns.keys()[1:]).city.count())
    df_city.columns = ["count"]
    df_city = df_city.reset_index().drop("count", axis=1)
    df_city.index.name = "city_id"

    df_temperature = df.merge(df_city.reset_index())[models.Temperature.__table__.columns.keys()[1:]]

    df_city.index.name = "id"
    df_city.to_sql(name=models.City.__tablename__, con=db.engine, if_exists="append", index_label="id")

    df_temperature.to_sql(
        name=models.Temperature.__tablename__, con=db.engine, if_exists="append", chunksize=10000, index=False
    )


if __name__ == "__main__":
    db_session = db.SessionLocal()
    models.Base.metadata.create_all(db.engine)
    load_data(db_session)
    logger.info("Loading data complete..")

    print(db_session.query(models.Temperature).first())
