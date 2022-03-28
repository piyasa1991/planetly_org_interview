import pytest
import interview_app.models as models
from datetime import datetime

CITIES_ROUTE = "/cities"


def test_top_n_citites(client, db_session):
    date_start = "2000-01-01T00:00:00.000Z"
    response = client.get(f"{CITIES_ROUTE}/top/3?date_start={date_start}")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_create_temperature(client, db_session):
    temperature_json = {
        "average_temperature": 2.5,
        "average_temperature_uncertainty": 2.5,
        "dt": datetime(2022, 3, 1).isoformat(),
    }

    response = client.post(f"{CITIES_ROUTE}/1/temperature", json=temperature_json)
    import pdb

    assert response.status_code == 201
    data = response.json()
    temperature_in_db = db_session.query(models.Temperature).filter_by(id=data["id"]).first()
    assert temperature_in_db.average_temperature == temperature_json["average_temperature"]
    assert (
        temperature_in_db.average_temperature_uncertainty
        == temperature_json["average_temperature_uncertainty"]
    )


def test_update_temperature(client, db_session):
    last_
    temperature_json = {
        "average_temperature": 0.5,
        "average_temperature_uncertainty": 2.5,
        "dt": datetime(2022, 3, 1).isoformat(),
    }
    response = client.put(f"{CITIES_ROUTE}/1/temperature", json=temperature_json)

    assert response.status_code == 200
    data = response.json()
    temperature_in_db = db_session.query(models.Temperature).filter_by(id=data["id"]).first()
    assert temperature_in_db.average_temperature == temperature_json["average_temperature"]
    assert (
        temperature_in_db.average_temperature_uncertainty
        == temperature_json["average_temperature_uncertainty"]
    )


def get_top_1_city(client, db_session):
    date_start = "2000-01-01T00:00:00.000Z"
    data = client.get(f"{CITIES_ROUTE}/top/1?date_start={date_start}").json()[0]
    return data


def test_sytem(client, db_session):
    data = get_top_1_city(client, db_session)

    city_id = int(data["id"])
    average_temperature = data["temperature"]["average_temperature"] + 0.1
    average_temperature_uncertainty = data["temperature"]["average_temperature_uncertainty"] + 0.1
    dt = datetime(2022, 3, 1).isoformat()

    temperature_json = {
        "average_temperature": average_temperature,
        "average_temperature_uncertainty": average_temperature_uncertainty,
        "dt": dt,
    }

    response = client.post(f"{CITIES_ROUTE}/{city_id}/temperature", json=temperature_json)
    import pdb

    assert response.status_code == 201
    data = response.json()
    temperature_in_db = db_session.query(models.Temperature).filter_by(id=data["id"]).first()
    assert temperature_in_db.average_temperature == temperature_json["average_temperature"]
    assert (
        temperature_in_db.average_temperature_uncertainty
        == temperature_json["average_temperature_uncertainty"]
    )

    average_temperature = temperature_in_db.average_temperature - 2.5
    average_temperature_uncertainty = temperature_in_db.average_temperature_uncertainty - 2.5
    temperature_json["average_temperature"] = average_temperature
    temperature_json["average_temperature_uncertainty"] = average_temperature_uncertainty

    response = client.put(f"{CITIES_ROUTE}/{city_id}/temperature", json=temperature_json)

    assert response.status_code == 200
    db_session.refresh(temperature_in_db)
    assert temperature_in_db.average_temperature == temperature_json["average_temperature"]
