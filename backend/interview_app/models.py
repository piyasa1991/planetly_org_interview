import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

Base = sqlalchemy.ext.declarative.declarative_base()


class Temperature(Base):
    __tablename__ = "temperature"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    dt = sqlalchemy.Column(sqlalchemy.DateTime)
    average_temperature = sqlalchemy.Column(sqlalchemy.Float)
    average_temperature_uncertainty = sqlalchemy.Column(sqlalchemy.Float)
    city_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("city.id"))


class City(Base):
    __tablename__ = "city"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    city = sqlalchemy.Column(sqlalchemy.Text)
    country = sqlalchemy.Column(sqlalchemy.Text)
    latitude = sqlalchemy.Column(sqlalchemy.Text)
    longitude = sqlalchemy.Column(sqlalchemy.Text)

    temperatures = sqlalchemy.orm.relationship("Temperature", backref="city", uselist=True)
